#define _DEFAULT_SOURCE

#include "moulette_setup.h"

#include <errno.h>
#include <stdio.h>
#include <string.h>
#include <time.h>
#include <unistd.h>

#include "log.h"
#include "moulette_opts.h"

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

int moulette_set_hostname(moulette_opts *opts) {
    char md5_string[9];
    i32 err;

    snprintf(md5_string, 9, "%x", fnv32_hash(opts->path, strlen(opts->path)));
    // Compute the hostname by hashing the image name (rootfs), program
    // arguments, and current timestamp.
    // moulette_compute_hash(opts, md5_string);

    log_info("Setting hostname: %s", md5_string);
    err = sethostname(md5_string, strlen(md5_string));
    if (err != 0) {
        log_error("Failed to update hostname: %s", strerror(errno));
        return err;
    }

    return 0;
}