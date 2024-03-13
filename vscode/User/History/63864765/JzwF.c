#include "seccomp.h"

#include <seccomp.h>
#include <unistd.h>

#include "log.h"

int moulette_seccomp_init(void) {
    scmp_filter_ctx ctx = seccomp_init(SCMP_ACT_ALLOW);

    if (seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(nfsservctl), 0)) {
        log_error("Failed to add seccomp rule");
    }

    if (seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(personality), 0)) {
        log_error("Failed to add seccomp rule");
    }

    if (seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(pivot_root), 0)) {
        log_error("Failed to add seccomp rule");
    }
}