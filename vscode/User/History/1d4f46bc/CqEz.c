#include "cgroups.h"

#include <errno.h>
#include <fcntl.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>

#include "log.h"

#define CG_ROOT "/sys/fs/cgroup"
#define CG_VIRLI "VIRLI"

/// LIMITS
#define CG_MAX_MEMORY "1G"
#define CG_MAX_CPU "1"
#define CG_MAX_PIDS "100"

#define MAX_BUF_SIZE 1024

static bool CG_INITIALIZED = false;

/// Open a file in a cgroup folder and write some data to it.
/// returns 0 on success
int cg_truncated_write(const char *cg_path, const char *fname,
                       const char *to_write) {
    int res = 0;

    if (!CG_INITIALIZED) {
        log_error("Uninitialized cgroups");
        res = 1;
        goto fail;
    }

    char path[MAX_BUF_SIZE];
    if (snprintf(path, MAX_BUF_SIZE, "%s/%s", cg_path, fname) > MAX_BUF_SIZE) {
        // Buffer too small
        log_error("Buffer too small");
        res = 1;
        goto fail;
    }

    FILE *file = fopen(path, "w");
    if (file == NULL) {
        log_error("Cannot open file in WRITE mode: `%s`: %s", path,
                  strerror(errno));
        res = 1;
        goto fail;
    }
    // Disable buffering of fputs
    setvbuf(file, NULL, _IONBF, 0);

    log_debug("writing `%s` to `%s`", to_write, path);
    if (fputs(to_write, file) < 0) {
        log_error("Cannot write to `%s`", path);
        res = 1;
        goto close_fail;
    }

close_fail:
    fclose(file);
fail:
    return res;
}

/// Add a process to a cgroup by writing to its `cgroup.procs`
int cg_add_process(const char *cg_path, const pid_t pid) {
    char pid_buf[32];
    snprintf(pid_buf, 32, "%d", pid);

    return cg_truncated_write(cg_path, "cgroup.procs", pid_buf);
}

/// Add a controller to a cgroup by writing to its `cgroup.controllers`
int cg_add_controller(const char *cg_path, const char *controller_name) {
    char controller_buf[64];
    snprintf(controller_buf, 64, "+%s", controller_name);

    return cg_truncated_write(cg_path, "cgroup.subtree_control",
                              controller_buf);
}

/// Read the `cgroup.controllers` and put it in the output buffer
int cg_get_controllers(const char *cg_path, char *output, size_t output_len) {
    int res = 0;

    if (!CG_INITIALIZED) {
        log_error("Uninitialized cgroups");
        res = 1;
        goto fail;
    }

    char path[MAX_BUF_SIZE];
    if (snprintf(path, MAX_BUF_SIZE, "%s/cgroup.controllers", cg_path)
        > MAX_BUF_SIZE) {
        // Buffer too small
        log_error("Buffer too small");
        res = 1;
        goto fail;
    }

    FILE *file = fopen(path, "r");
    if (file == NULL) {
        log_error("Cannot open file: `%s`", path);
        res = 1;
        goto fail;
    }

    size_t read = fread(output, sizeof(char), output_len, file);
    if (ferror(file)) {
        log_error("Error while reading controllers: %s", strerror(errno));
        res = 1;
    } else if (read == output_len) {
        // Buffer is too small
        log_error("Buffer too small", path);
        res = 1;
    } else {
        // Make sure the string is null terminated
        output[read] = '\0';
    }

    fclose(file);
fail:
    return res;
}

int cg_init(void) {
    char path_buf[MAX_BUF_SIZE];

    if (snprintf(path_buf, MAX_BUF_SIZE, "%s/%s", CG_ROOT, CG_VIRLI)
        > MAX_BUF_SIZE) {
        log_error("Buffer too small");
        return -1;
    }

    log_info("Initializing cgroup `%s`...", path_buf);

    // Create a directory, and expect it to fail if already existing.
    int mkdir_ret = mkdir(path_buf, 0755);
    if (mkdir_ret == -1) {
        if (errno == EEXIST) {
            log_debug("cgroup directory already existing");
        } else {
            log_error("cgroup directory creation failed: %s", strerror(errno));
            return -1;
        }
    }

    CG_INITIALIZED = true;

    // Memory controller
    log_debug("Setting memory limit to %s", CG_MAX_MEMORY);
    // Controller is not already present. Add it
    if (cg_add_controller(CG_ROOT, "memory") != 0) {
        log_error("Cannot add memory controller to cgroup");
        return -1;
    }
    if (cg_truncated_write(path_buf, "memory.max", CG_MAX_MEMORY) != 0) {
        log_error("Cannot set memory limit to cgroup");
        return -1;
    }

    // PID controller
    log_debug("Setting pids limit to %s", CG_MAX_PIDS);
    // Controller is not already present. Add it
    if (cg_add_controller(CG_ROOT, "pids") != 0) {
        log_error("Cannot add pids controller to cgroup");
        return -1;
    }
    if (cg_truncated_write(path_buf, "pids.max", CG_MAX_PIDS) != 0) {
        log_error("Cannot set pids limit to cgroup");
        return -1;
    }

    // CPU controller
    log_debug("Setting cpuset limit to %s", CG_MAX_CPU);
    // Controller is not already present. Add it
    if (cg_add_controller(CG_ROOT, "cpuset") != 0) {
        log_error("Cannot add cpu controller to cgroup");
        return -1;
    }
    if (cg_truncated_write(path_buf, "cpuset.cpus", CG_MAX_CPU) != 0) {
        log_error("Cannot set cpu limit to cgroup");
        return -1;
    }

    log_debug("cgroup successfully initialized");

    // i32 err = cg_add_process(path_buf, getpid());
    // if (err != 0) {
    //     log_error("Failed to move process to cgroup: %s", strerror(err));
    //     return 1;
    // }

    return 0;
}
