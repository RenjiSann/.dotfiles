#pragma once

#include "log.h"
#include "types.h"

typedef struct moulette_opts_t {
    char *path;
    char **argv_to_run;
    u32 argc_to_run;
    log_level verbose_level; /// 0 -> Error + Warn; 1 -> +Info; 2 -> +Debug
} moulette_opts;

int parse_opts(int argc, char **argv, moulette_opts *opts);

void print_usage(char *argv0);