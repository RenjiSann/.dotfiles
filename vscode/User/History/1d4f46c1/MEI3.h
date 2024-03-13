#pragma once

#include <sys/types.h>
#include "types.h"

/// Create the VIRLI cgroup
int cg_init(void);

int cg_add_process(const char* cg_path, pid_t pid);