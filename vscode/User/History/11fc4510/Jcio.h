#pragma once

typedef struct moulette_opts_t {
    char *path;
    char **program;
} moulette_opts;

int parse_opts(int argc, char **argv, moulette_opts *opts);