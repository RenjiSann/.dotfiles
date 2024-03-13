#define _POSIX_C_SOURCE 2

#include "moulette_opts.h"

#include <stdio.h>
#include <unistd.h>

int parse_opts(int argc, char **argv, moulette_opts *opts) {
    int opt;

    while ((opt = getopt(argc, argv, "I:"))) {
        switch (opt) {
        case 'I':
            opts->path = optarg;
        default:
            print_usage(argv[0]);
            return 1;
        }
    }

    return 0;
}

void print_usage(char *argv0) {
    printf("Usage: %s <-I docker-img | rootfs-path> <command> [parameters]\n",
           argv0);
}