#include "seccomp.h"

#include <seccomp.h>
#include <unistd.h>

int moulette_seccomp_init(void) {
    scmp_filter_ctx ctx = seccomp_init(SCMP_ACT_ALLOW);
    seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(nfsservctl), 0);
}