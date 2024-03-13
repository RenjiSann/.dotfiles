#define _DEFAULT_SOURCE

#include "moulette_setup.h"

#include <errno.h>
#include <md5.h>
#include <string.h>
#include <time.h>
#include <unistd.h>

#include "log.h"
#include "moulette_opts.h"

static void moulette_compute_hash(moulette_opts *opts, char *buf) {
    MD5_CTX ctx;

    MD5Init(&ctx);

    MD5Update(&ctx, (void *)opts->path, strlen(opts->path));

    for (u32 i = 0; i < opts->argc_to_run; i++) {
        MD5Update(&ctx, (void *)opts->argv_to_run[i],
                  strlen(opts->argv_to_run[i]));
    }

    // Add a time to the hash to avoid duplicate hostnames
    time_t t = time(NULL);
    MD5Update(&ctx, (void *)&t, sizeof(time_t));

    MD5End(&ctx, buf);
}

int moulette_set_hostname(moulette_opts *opts) {
    char md5_string[MD5_DIGEST_STRING_LENGTH];
    i32 err;

    // Compute the hostname by hashing the image name (rootfs), program
    // arguments, and current timestamp.
    moulette_compute_hash(opts, md5_string);
    log_debug("Computed hostname: %s", md5_string);

    err = sethostname(md5_string, MD5_DIGEST_STRING_LENGTH);
    if (err != 0) {
        log_error("Failed to update hostname: %s", strerror(errno));
        return err;
    }

    return 0;
}