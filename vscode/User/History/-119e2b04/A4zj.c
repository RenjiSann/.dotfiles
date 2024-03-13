#define _DEFAULT_SOURCE

#include "moulette_setup.h"

#include <errno.h>
#include <string.h>
#include <time.h>
#include <unistd.h>

#include "log.h"
#include "moulette_opts.h"
#include "utils.h"

static u32 fnv32_hash(const char *str, u64 len);

int moulette_set_hostname(moulette_opts *opts) {
    char buf[sizeof(u32) * 2 + 1];
    i32 err;
    u32 hash1 = fnv32_hash(opts->path, strlen(opts->path));
    time_t t = time(NULL);
    u32 hash2 = fnv32_hash((void *)&t, sizeof(t));

    snprintf(buf, 9, "%x", hash1 ^ hash2);

    log_info("Setting hostname: %s", buf);
    err = sethostname(buf, strlen(buf));
    if (err != 0) {
        log_error("Failed to update hostname: %s", strerror(errno));
        return err;
    }

    return 0;
}

void moulette_set_userns_mappings(pid_t pid) {
    char path[128];
    char content[128];
    uid_t uid = getuid();

    log_info("Setting user namespace mappings...");

    snprintf(path, 128, "/proc/%d/uid_map", pid);
    snprintf(content, 128, "0 %d 1\n", uid);
    if (write_to_file(path, content) != 0) {
        die(1, "Failed to set UID");
    }

    // See user_namespaces(7): One must deny the setgroups syscall before
    // writing to /proc/$pid/gid_map
    snprintf(path, 128, "/proc/%d/setgroups", pid);
    snprintf(content, 128, "deny\n");
    if (write_to_file(path, content) != 0) {
        die(1, "Failed to deny setgroups");
    }

    snprintf(path, 128, "/proc/%d/gid_map", pid);
    snprintf(content, 128, "0 %d 1\n", uid);
    if (write_to_file(path, content) != 0) {
        die(1, "Failed to set GID");
    }
}

// https://gist.github.com/sgsfak/9ba382a0049f6ee885f68621ae86079b
static u32 fnv32_hash(const char *str, u64 len) {
    unsigned char *s = (unsigned char *)str; /* unsigned string */

    /* See the FNV parameters at www.isthe.com/chongo/tech/comp/fnv/#FNV-param
     */
    const u32 FNV_32_PRIME = 0x01000193; /* 16777619 */

    u32 h = 0x811c9dc5; /* 2166136261 */
    while (len--) {
        /* xor the bottom with the current octet */
        h ^= *s++;
        /* multiply by the 32 bit FNV magic prime mod 2^32 */
        h *= FNV_32_PRIME;
    }

    return h;
}
