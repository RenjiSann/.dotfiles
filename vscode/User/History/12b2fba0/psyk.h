#pragma once

/**
 * Make sure the CAP_NET_RAW capability is put into the ambient set.
 * @return 0 on success.
 */
int capa_init_ambient(void);

/**
 * Adjust the capabilities for the forked process
 */
int capa_init_fork(void);

/**
 * Dump the effective, permitted, inheritable, ambient or bounding set of
 * capabilities.
 */
void print_effective(void);
void print_permitted(void);
void print_inheritable(void);
void print_ambient(void);
void print_bounding(void);
