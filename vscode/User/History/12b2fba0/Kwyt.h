#pragma once

#include "types.h"

/// Make sure the CAP_NET_RAW capability is put into the ambient set.
/// Return 0 on success.
int capa_init_ambient(void);

/// Adjust the capabilities for the forked process
int capa_init_fork(void);

// Print Caps of the effective set
void print_effective(void);
// Print Caps of the permitted set
void print_permitted(void);
// Print Caps of the inheritable set
void print_inheritable(void);
// Print Caps of the bounding set
void print_bounding(void);
// Print Caps of the ambient set
void print_ambient(void);
