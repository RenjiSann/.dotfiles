#include "seccomp.h"

#include <seccomp.h>
#include <string.h>
#include <unistd.h>

#include "log.h"

int moulette_seccomp_init(void) {
    int err;
    scmp_filter_ctx ctx = seccomp_init(SCMP_ACT_ALLOW);

    err = seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(nfsservctl), 0);
    if (err != 0) {
        goto err_rule_add;
    }

    err = seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(personality), 0);
    if (err != 0) {
        goto err_rule_add;
    }

    err = seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(pivot_root), 0);
    if (err != 0) {
        goto err_rule_add;
    }

    err = seccomp_load(ctx);
    if (err != 0) {
        log_error("Failed to load seccomp context: %s", strerror(err));
        return 1;
    }

    return 0;

err_rule_add:
    log_error("Failed to add seccomp rule: %s", strerror(err));
    return 1;
}