#include "cgroups.h"

#include <asm-generic/errno-base.h>
#include <errno.h>
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
#define CG_CURRENT "/proc/self/cgroup"
#define CG_VIRLI "VIRLI"
#define CG_SUBVIRLI "PROCS"

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
        log_error("Cannot open file: `%s`: %s", path, strerror(errno));
        res = 1;
        goto fail;
    }

    if (fprintf(file, "%s", to_write) < 0) {
        log_error("Cannot write to `%s`", path);
        res = 1;
        goto close_fail;
    }

    // Flush to ensure
    if (fflush(file) != 0) {
        log_error("Writing to file `%s` failed: %s", path, strerror(errno));
        res = 1;
    }

close_fail:
    fclose(file);
fail:
    return res;
}

/// Add a process to a cgroup by writing to its `cgroup.procs`
int cg_add_process(const char *cg_path, const pid_t pid) {
    char pid_buf[32];
    snprintf(pid_buf, 32, "%u", pid);

    return cg_truncated_write(cg_path, "cgroup.procs", pid_buf);
}

/// Add a controller to a cgroup by writing to its `cgroup.controllers`
int cg_add_controller(const char *cg_path, const char *controller_name) {
    // char controller_buf[64];
    // snprintf(controller_buf, 64, "+%s", controller_name);

    return cg_truncated_write(cg_path, "cgroup.controllers", controller_name);
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
            log_info("cgroup directory already existing");
        } else {
            log_error("cgroup directory creation failed: %s", strerror(errno));
            return -1;
        }
    }

    // path /= CG_SUBVIRLI;

    // Create process CGROUP
    // if (!fs::is_directory(path) && !fs::create_directory(path, err)) {
    //     std::cerr << "Cannot create directory: " << path << '\n'
    //               << "Error: " << err.message() << std::endl;
    //     return;
    // }

    CG_INITIALIZED = true;

    // Check the current controllers
    char controllers[MAX_BUF_SIZE];
    if (cg_get_controllers(path_buf, controllers, MAX_BUF_SIZE) != 0) {
        log_error("Error while reading controllers");
        return -1;
    }

    // Memory controller
    log_info("Setting memory limit to %s", CG_MAX_MEMORY);
    if (strstr(controllers, "memory") == NULL) {
        // Controller is not already present. Add it
        if (cg_add_controller(path_buf, "memory") != 0) {
            log_error("Cannot add memory controller to cgroup");
            return -1;
        }
    }
    if (cg_truncated_write(path_buf, "memory.max", CG_MAX_MEMORY) != 0) {
        log_error("Cannot set memory limit to cgroup");
        return -1;
    }

    // PID controller
    log_info("Setting pids limit to %s", CG_MAX_PIDS);
    if (strstr(controllers, "pids") == NULL) {
        // Controller is not already present. Add it
        if (cg_add_controller(path_buf, "pids") != 0) {
            log_error("Cannot add pids controller to cgroup");
            return -1;
        }
    }
    if (cg_truncated_write(path_buf, "pids.max", CG_MAX_PIDS) != 0) {
        log_error("Cannot set pids limit to cgroup");
        return -1;
    }

    // CPU controller
    log_info("Setting cpuset limit to %s", CG_MAX_CPU);
    if (strstr(controllers, "cpuset") == NULL) {
        // Controller is not already present. Add it
        if (cg_add_controller(path_buf, "cpuset") != 0) {
            log_error("Cannot add cpu controller to cgroup");
            return -1;
        }
    }
    if (cg_truncated_write(path_buf, "cpuset.cpus", CG_MAX_CPU) != 0) {
        log_error("Cannot set cpu limit to cgroup");
        return -1;
    }

    log_info("cgroup successfully initialized");
    return 0;
}

void cg_clear(void) {
    // fs::path path = fs::path(CG_ROOT) / CG_VIRLI;
    // fs::path subpath = path / CG_SUBVIRLI;
    // std::error_code err;

    // Explicitely use rmdir syscall, because fs::remove_all
    // only uses unlinkat to remove files directly.
    // if (rmdir(subpath.c_str()) == -1) {
    //     std::cerr << "Cannot remove directory: " << subpath << std::endl;
    //     return;
    // }

    // if (rmdir(path.c_str()) == -1) {
    //     std::cerr << "Cannot remove directory: " << path << std::endl;
    //     return;
    // }
}

/// Populate the given struct with current cgroup info
// void cg_get_current(cg_info *cgroup) {
//     fs::path self(CG_CURRENT);
//     std::ifstream file(self);
//     std::string buf;

//     file >> buf;
//     file.close();

//     // We assume the buffer is of the form 0::/<path>
//     buf = buf.substr(buf.find('/') + 1);
//     cgroup->path = fs::path(buf);

//     cgroup->parent = nullptr;
//     cgroup->name = "";
//     cgroup->nb_procs = 0;
// }

/// Fill the given vector withall the PIDs directly attached to the
/// given cgroup.
// void cg_list_procs(std::vector<u32> *out, cg_info *cgroup) {
//     fs::path path = cg_build_path(cgroup) / "cgroup.procs";
//     std::cout << path << std::endl;
//     u32 count = 0;

//     // Read cgroup.procs
//     std::string buf;
//     std::ifstream file(path); // TODO: Check valid
//     while (std::getline(file, buf)) {
//         out->push_back(std::stoul(buf));
//         count++;
//     }

//     file.close();
//     cgroup->nb_procs = count;
// }
