#pragma once

#include <sys/types.h>

#define CG_ROOT "/sys/fs/cgroup"
#define CG_VIRLI "/sys/fs/cgroup/VIRLI"

/**
 * Create the VIRLI cgroup
 */
int cg_init(void);

int cg_add_process(const char *cg_path, pid_t pid);