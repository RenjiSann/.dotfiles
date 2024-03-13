#define _GNU_SOURCE

#include <errno.h>
#include <sched.h>
#include <stdlib.h>
#include <string.h>
#include <sys/prctl.h>
#include <sys/wait.h>
#include <unistd.h>

#include "capabilities.h"
#include "cgroups.h"
#include "docker_image.h"
#include "isolation.h"
#include "log.h"
#include "moulette_opts.h"
#include "moulette_setup.h"
#include "seccomp.h"
#include "types.h"
#include "utils.h"

// Forward declaration
static int child_main(void *data);

int main(int argc, char **argv) {
    int err;
    moulette_opts opts;
    err = parse_opts(argc, argv, &opts);
    if (err != 0) {
        return err;
    }

    log_set_level(opts.verbose_level);

    if (opts.verbose_level < LOG_WARN) {
        dump_opts(&opts);
    }

    if (check_opts(&opts) != 0) {
        return 1;
    }

    log_info("Hello GISTRE");

    err = cg_init();
    if (err != 0) {
        log_error("cgroup init failed");
        return err;
    }

    log_debug("Add parent process to VIRLI cgroup");
    if (cg_add_process(CG_VIRLI, getpid()) != 0) {
        log_error("Failed to add process to cgroup");
    }

    // if (opts.kind == MOULETTE_IMAGE) {
    //     char rootfs_path[1024];
    //     image_pull_then_init(opts.path, rootfs_path, 1024);
    // }

    // Create a pipe to be able to send data to the forked process.
    if (pipe2(opts.pipe, 0) != 0) {
        die(1, "Communication pipe creation failed");
    }

    // fork and run the argument
    int ns_flags = CLONE_NEWIPC | CLONE_NEWNS | CLONE_NEWPID | CLONE_NEWNET
        | CLONE_NEWUTS | CLONE_NEWCGROUP | CLONE_NEWUSER;

    log_info("Cloning process...");
    pid_t pid = clone(child_main, malloc(2 << 20) + (2 << 20),
                      ns_flags | SIGCHLD, &opts);
    if (pid == -1) {
        // Error during clone
        die(1, "Error when cloning: %s", strerror(errno));
    }
    // Parent process
    moulette_set_userns_mappings(pid);

    // Once setup is done, send 'OK' through the pipe so the child can go on
    if (write(opts.pipe[1], "OK", 2) == -1)

    int status;
    if (waitpid(pid, &status, 0) == -1) {
        log_error("Waitpid failed (pid = %u): %s", pid, strerror(errno));
        return 2;
    }

    int ret_val = WEXITSTATUS(status);
    if (ret_val == 0) {
        log_info("The process exited 0");
    } else {
        log_warn("The process exited %d", ret_val);
    }
}

/// The entrypoint of the cloned process
static int child_main(void *data) {
    moulette_opts *opts = data;

    // Kill the cmd process if the isolate process dies.
    if (prctl(PR_SET_PDEATHSIG, SIGKILL))
        die(1, "cannot PR_SET_PDEATHSIG for child process: %m\n");

    usleep(1000000);

    if (fs_init(opts->path, opts->student_directory) != 0) {
        die(1, "File system init failed");
    }

    log_info("Setting UID/GID to 0...");
    if (setuid(0) == -1)
        die(1, "Failed to setuid");
    if (setgid(0) == -1)
        die(1, "Failed to setgid");

    if (moulette_set_hostname(opts) != 0) {
        die(1, "Hostname init failed");
    }

    // Remove all capabilities from bound set, but CAP_NET_RAW
    log_info("Dropping capabilities...");
    if (capa_init_fork() != 0) {
        die(1, "Capabilities init failed");
    }

    // Limit syscall capabilities
    log_info("Applying Seccomp...");
    if (moulette_seccomp_init() != 0) {
        die(1, "Seccomp init failed");
    }

    log_info("Running ENTRYPOINT `%s`", opts->argv_to_run[0]);
    return execvp(opts->argv_to_run[0], &opts->argv_to_run[0]);
}
