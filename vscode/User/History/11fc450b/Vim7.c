#define _POSIX_C_SOURCE 2
#include "moulette_opts.h"

#include <stdio.h>
#include <string.h>
#include <unistd.h>

#include "log.h"

int parse_opts(int argc, char **argv, moulette_opts *opts) {
    int opt;
    int Iset = 0;
    u32 verbose = 0;

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
            verbose++;
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

    switch (verbose) {
    case 0:
        opts->verbose_level = LOG_WARN;
        break;
    case 1:
        opts->verbose_level = LOG_INFO;
        break;
    case 2:
        opts->verbose_level = LOG_DEBUG;
        break;
    default:
        // More than 2
        opts->verbose_level = LOG_DEBUG;
    }

    return 0;
}

void print_usage(char *argv0) {
    fprintf(
        stderr,
        "Usage: %s [-V] <-I docker-img | rootfs-path> <command> [parameters]\n"
        "   -V     Increase verbose level\n",
        argv0);
}