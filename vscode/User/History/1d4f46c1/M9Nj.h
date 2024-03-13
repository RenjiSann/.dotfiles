#ifndef _VIRLI_CGROUPS_
#define _VIRLI_CGROUPS_

#include "types.h"

/// Create the VIRLI Cgroup
int cg_init(void);
void cg_clear(void);

#endif // _VIRLI_CGROUPS_