#pragma once

#include "types.h"
#include "log.h"

typedef struct moulette_opts_t {
    char *path;
    char **argv_to_run;
    u32 argc_to_run;
    u32 verbose_level;
} moulette_opts;

int parse_opts(int argc, char **argv, moulette_opts *opts);

void print_usage(char *argv0);