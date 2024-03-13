#include "seccomp.h"

#include <seccomp.h>
#include <unistd.h>

#include "log.h"

int moulette_seccomp_init(void) {
    int err;
    scmp_filter_ctx ctx = seccomp_init(SCMP_ACT_ALLOW);

    err = seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(nfsservctl), 0);
    if (err != 0) {
        log_error("Failed to add seccomp rule");
    }

    err = seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(personality), 0);
    if (err != 0) {
        log_error("Failed to add seccomp rule");
    }

    err = seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(pivot_root), 0);
    if (err != 0) {
    }

    err = seccomp_load(ctx);
    if (err != 0) {

    }

err_rule_add:
    log_error("Failed to add seccomp rule");
    return 1;
}