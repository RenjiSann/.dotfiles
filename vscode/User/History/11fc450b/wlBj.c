#define _POSIX_C_SOURCE 2

#include "moulette_opts.h"

#include <stdio.h>
#include <string.h>
#include <unistd.h>

int parse_opts(int argc, char **argv, moulette_opts *opts) {
    int opt;
    int Iset = 0;

    memset(opts, 0, sizeof(moulette_opts));

    while ((opt = getopt(argc, argv, "VI:")) != -1) {
        switch (opt) {
        case 'I':
            if (Iset) {
                fprintf(stderr, "Duplicate parameter -I\n");
                print_usage(argv[0]);
                return 1;
            }
            opts->path = optarg;
            Iset = 1;
            break;
        case 'V':
            opts->verbose_level++;
            if (opts->verbose_level > 3) {
                opts->verbose_level = 3;
            }
            break;
        default:
            print_usage(argv[0]);
            return 1;
        }
    }

    if (optind >= argc) {
        print_usage(argv[0]);
        return 1;
    }

    if (!Iset) {
        fprintf(stderr, "Missing parameter -I\n");
        print_usage(argv[0]);
        return 1;
    }

    opts->argv_to_run = argv + optind;
    opts->argc_to_run = argc - optind;

    return 0;
}

void print_usage(char *argv0) {
    fprintf(stderr,
            "Usage: %s [-V] <-I docker-img | rootfs-path> <command> [parameters]\n"
            "   -V     Increase verbose level\n",
            argv0);
}