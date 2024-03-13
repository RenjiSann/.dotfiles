#include "moulette_setup.h"

#include <md5.h>
#include <string.h>

int moulette_set_hostname(moulette_opts *opts) {
    MD5_CTX ctx;
    MD5Init(&ctx);

    MD5Update(&ctx, opts->path, strlen(opts->path));

    return 0;
}