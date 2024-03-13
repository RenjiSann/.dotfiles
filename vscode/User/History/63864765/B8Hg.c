#include "seccomp.h"

#include <seccomp.h>
#include <unistd.h>

int moulette_seccomp_init(void) {
    scmp_filter_ctx ctx = seccomp_init();
}