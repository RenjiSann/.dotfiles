#define _DEFAULT_SOURCE
#define _GNU_SOURCE

#include <errno.h>
#include <linux/limits.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mount.h>
#include <sys/stat.h>
#include <sys/syscall.h>
#include <unistd.h>

#include "log.h"
#include "types.h"
#include "utils.h"


static int dir_check_or_create(const char *path, int mode);
static int mount_proc(void);
static int mount_sys(void);
static int mount_cgroup(void);
static int pivot_root_init(const char *fs_root, const char *student_dir);

int fs_init(const char *fs_root, const char *student_dir) {
    // if (chroot_init(fs_root) != 0) {
    //     log_error("chroot init failed");
    //     return 1;
    // }

    if (pivot_root_init(fs_root, student_dir) != 0) {
        log_error("pivot_root init failed");
        return 1;
    }

    mount_proc();
    mount_sys();
    mount_cgroup();
    return 0;
}

/// Mount the /proc directory into the container.
static int mount_proc(void) {
    // char *src = "none";
    // char *dst = "/proc";
    // char *fstype = "proc";
    // u64 flags = MS_NOSUID | MS_NOATIME | MS_NODEV;
    // if (mount(src, dst, fstype, flags, NULL) != 0) {
    //     log_error("Mounting /proc failed: %s", strerror(errno));
    //     return 1;
    // }

    if (dir_check_or_create("/proc", 0555) != 0)
        die(1, "Failed to mkdir proc: %m");

    if (mount("none", "/proc", "proc", MS_NOSUID | MS_NOATIME | MS_NODEV, NULL))
        log_error("Failed to mount proc: %s", strerror(errno));
        die(1, "Failed to mount proc: %m");
    return 0;
}

/// Mount the /sys directory into the container.
__attribute((unused))
static int mount_sys(void) {
    char *src = "none";
    char *dst = "/sys";
    char *fstype = "sysfs";
    u64 flags = 0;

    if (mount(src, dst, fstype, flags, NULL) != 0) {
        log_error("Mounting /sys failed: %s", strerror(errno));
        return 1;
    }

    return 0;
}

/// Mount the /sys/fs/cgroup directory into the container.
__attribute((unused))
static int mount_cgroup(void) {
    char *src = "none";
    char *dst = "/sys/fs/cgroup";
    char *fstype = "cgroup2";
    u64 flags = 0;
    char *data = "";

    if (mount(src, dst, fstype, flags, data) != 0) {
        log_error("Mounting cgroup failed: %s", strerror(errno));
        return 1;
    }

    return 0;
}

/**
 * Check if a directory existsm or try to create it.
 */
static int dir_check_or_create(const char *path, int mode) {
    struct stat sstat;
    int res;

    log_debug("Checking stats for `%s`", path);
    res = stat(path, &sstat);

    if (res == 0) {
        if (S_ISDIR(sstat.st_mode)) {
            // Directory exists, skip
            return 0;
        } else {
            // Exists but is not a directory, error.
            log_error("Exists but not a folder: `%s`", path);
            return 1;
        }
    } else if (errno == ENOENT) {
        // Directory does not exists, try to create it.
        if (mkdir(path, mode) != 0) {
            log_error("%s failed on directory creation `%s`: %s", __func__,
                      path, strerror(errno));
            return 1;
        }
        return 0;
    } else {
        // Error
        log_error("%s failed on `%s`: %s", __func__, path, strerror(errno));
        return 1;
    }
}

// This function create directories recursively. If the function fails, the
// created folders are not deleted.
static int dir_chain_check_or_create(const char *path) {
    usize len = strlen(path);
    char *owned_path = strndupa(path, len);

    if (len == 0) {
        log_error("%s failed, empty path", __func__);
        return 1;
    }

    // We will iterate on all '/' in the path and cut it to check for directory
    // existence.

    // +1 because we omit the first '/' in case of absolute path
    for (usize i = 1; i < len; ++i) {
        if (owned_path[i] != '/') {
            continue;
        }
        owned_path[i] = '\0';

        if (dir_check_or_create(owned_path, S_IRWXU) != 0) {
            return 1;
        }

        owned_path[i] = '/';
    }

    if (owned_path[len - 1] != '/'
        && dir_check_or_create(owned_path, S_IRWXU) != 0) {
        return 1;
    }

    return 0;
}

__attribute((unused)) static int chroot_init(const char *path) {
    struct stat s;
    log_debug("Chrooting to `%s`", path);

    if (stat(path, &s) != 0) {
        log_info("Create the directory");
        if (mkdir(path, 0644) != 0) {
            return -1;
        }
    } else if (!S_ISDIR(s.st_mode)) {
        log_error("The path specified is not a directory");
        return -1;
    }

    log_info("chroot to %s", path);
    if (chroot(path) != 0) {
        log_error("chroot failed: %s", strerror(errno));
        return -1;
    }

    if (chdir("/") != 0) {
        log_error("chdir failed: %s", strerror(errno));
        return -1;
    }

    return 0;
}

static int pivot_root_init(const char *path, const char *student_dir) {
    char old_path[] = "/oldpath";
    char old_path_in_newfs[PATH_MAX] = { 0 };
    char old_path_student_dir[PATH_MAX] = { 0 };

    // Get the absolute path of the student dir and prepend it with old path.
    if (student_dir != NULL) {
        if (student_dir[0] == '/') {
            snprintf(old_path_student_dir, PATH_MAX, "%s%s", old_path,
                     student_dir);
        } else {
            char cwd[PATH_MAX / 2];
            if (getcwd(cwd, PATH_MAX) == NULL) {
                log_error("get_cwd error: %s", strerror(errno));
                return 1;
            }
            snprintf(old_path_student_dir, PATH_MAX, "%s/%s/%s", old_path, cwd,
                     student_dir);
        }
    }

    /**
     * Ensure that 'new_root' and its parent mount don't have
     * shared propagation (which would cause pivot_root() to
     * return an error), and prevent propagation of mount
     * events to the initial mount namespace.
     */
    if (mount(NULL, "/", NULL, MS_REC | MS_PRIVATE, NULL) != 0) {
        log_error("mount MS-PRIVATE failed: %s", strerror(errno));
        return -1;
    }

    /* Ensure that 'new_root' is a mount point. */
    if (mount(path, path, NULL, MS_BIND, NULL) != 0) {
        log_error("mount MS-BIND failed: %s", strerror(errno));
        return -1;
    }

    /* Create directory to which old root will be pivoted. */
    snprintf(old_path_in_newfs, sizeof(old_path_in_newfs), "%s/%s", path,
             old_path);
    if (dir_check_or_create(old_path_in_newfs, 0777) != 0) {
        return -1;
    }
    log_debug("Created dir in pivot root: %s", old_path_in_newfs);

    // Call pivot_root syscall
    log_debug("path: %s, old: %s", path, old_path);
    log_info("Pivoting root to %s...", path);
    if (syscall(SYS_pivot_root, path, old_path_in_newfs) != 0) {
        log_error("Failed to pivot_root: %s", strerror(errno));
        return -1;
    }

    if (chdir("/") != 0) {
        log_error("chdir failed: %s", strerror(errno));
        return -1;
    }

    // Before unmounting old_path, bind mount student dir to /home/student
    if (student_dir != NULL) {
        if (dir_chain_check_or_create("/home/student") != 0) {
            return 1;
        }
        if (mount(old_path_student_dir, "/home/student", NULL, MS_BIND, NULL)
            != 0) {
            log_error("Failed to mount student directory: %s", strerror(errno));
            return 1;
        }
    }

    /* Unmount old root and remove mount point. */
    if (umount2(old_path, MNT_DETACH) != 0) {
        log_error("umount2 failed: %s", strerror(errno));
        return -1;
    }
    if (rmdir(old_path) != 0) {
        log_error("rmdir failed: %s", strerror(errno));
        return -1;
    }

    return 0;
}
