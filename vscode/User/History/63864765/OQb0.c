#include "seccomp.h"

#include <seccomp.h>
#include <unistd.h>

int seccomp_init(void) {
    scmp_filter_ctx ctx = seccomp_init(SCMP_ACT_ALLOW);
}