#include "moulette_setup.h"

#include <md5.h>
#include <string.h>
#include "moulette_opts.h"

static void moulette_compute_hash(moulette_opts *opts) {
    MD5_CTX ctx;
    MD5Init(&ctx);

    MD5Update(&ctx, (void *)opts->path, strlen(opts->path));

    for (u32 i = 0; i < opts->argc_to_run; i++) {
        MD5Update(MD5_CTX *, const uint8_t *, size_t)
    }
}

int moulette_set_hostname(moulette_opts *opts) {

    return 0;
}