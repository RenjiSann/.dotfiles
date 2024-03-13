#include "moulette_setup.h"

#include <md5.h>
#include <string.h>

#include "log.h"
#include "moulette_opts.h"

static void moulette_compute_hash(moulette_opts *opts, char *buf) {
    MD5_CTX ctx;
    u8 digest[MD5_DIGEST_LENGTH];

    MD5Init(&ctx);

    MD5Update(&ctx, (void *)opts->path, strlen(opts->path));

    for (u32 i = 0; i < opts->argc_to_run; i++) {
        MD5Update(&ctx, (void *)opts->argv_to_run[i],
                  strlen(opts->argv_to_run[i]));
    }

    MD5Final(digest, &ctx);
    MD5End(&ctx, buf);
}

int moulette_set_hostname(moulette_opts *opts) {
    char md5_string[MD5_DIGEST_STRING_LENGTH];
    moulette_compute_hash(opts);

    log_error("Result hash: %*s (size is %d)", MD5_DIGEST_LENGTH, digest, MD5_DIGEST_LENGTH);
    return 0;
}