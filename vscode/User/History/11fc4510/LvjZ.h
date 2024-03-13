#pragma once

#include "log.h"
#include "types.h"

typedef enum { MOULETTE_ROOTFS, MOULETTE_IMAGE } moulette_src_kind;

typedef struct {
    moulette_src_kind kind;
    char *path;
    char *student_directory;
    char **argv_to_run;
    u32 argc_to_run;
    log_level verbose_level;
} moulette_opts;

/**
 * Parse the CLI arguments and populate the given options struct.
 */
int parse_opts(int argc, char **argv, moulette_opts *opts);

/**
 * Dump the config in stderr.
 */
void dump_opts(moulette_opts *opts);

/**
 * Check opts arguments for illegal values
 * @return 0 on success, 1 if an illegal value is found.
 */
int check_opts(const moulette_opts *opts);