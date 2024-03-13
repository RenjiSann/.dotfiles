#define _POSIX_C_SOURCE 2
#include "moulette_opts.h"

#include <stdio.h>
#include <string.h>
#include <unistd.h>

#include "log.h"

static int check_opts(const moulette_opts *opts);
static void print_usage(char *argv0);

int parse_opts(int argc, char **argv, moulette_opts *opts) {
    int opt;
    int Iset = 0;
    int vset = 0;
    u32 verbose = 0;

    memset(opts, 0, sizeof(moulette_opts));

    while ((opt = getopt(argc, argv, "v:VI:")) != -1) {
        switch (opt) {
        case 'I':
            if (Iset) {
                fprintf(stderr, "Duplicate parameter -I\n");
                print_usage(argv[0]);
                return 1;
            }
            Iset = 1;
            opts->kind = MOULETTE_IMAGE;
            opts->path = optarg;
            break;
        case 'V':
            verbose++;
            break;
        case 'v':
            if (vset) {
                fprintf(stderr, "Duplicate parameter -v\n");
                print_usage(argv[0]);
                return 1;
            }
            vset = 1;
            opts->student_directory = optarg;
            break;
        default:
            print_usage(argv[0]);
            return 1;
        }
    }

    if (!Iset) {
        // -I was not set
        if (argc - optind < 2) {
            // Missing argument
            fprintf(stderr, "Missing argument\n");
            print_usage(argv[0]);
            return 1;
        }

        opts->kind = MOULETTE_ROOTFS;
        opts->path = argv[optind++];
    }

    if (optind >= argc) {
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

void dump_cfg(moulette_opts *opts) {
    fprintf(stderr,
            "Moulette Configuration:\n"
            "Kind: %s\n"
            "%s: %s\n"
            "Entrypoint:",
            (opts->kind == MOULETTE_ROOTFS) ? "rootfs" : "docker image",
            (opts->kind == MOULETTE_ROOTFS) ? "Path" : "Image", opts->path);
    // Print entrypoint
    for (u32 i = 0; i < opts->argc_to_run; i++) {
        fprintf(stderr, " %s", opts->argv_to_run[i]);
    }
    fputc('\n', stderr);
}

/**
 * Check opts arguments for illegal values
 */
static int check_opts(const moulette_opts *opts) {

}

static void print_usage(char *argv0) {
    fprintf(
        stderr,
        "Usage: %s [-V] [-v student-dir] <-I docker-img | rootfs-path> "
        "<command> [parameters]\n"
        "   -V              Increase verbose level\n"
        "   -v student-dir  Mount the student directory into /home/student\n",
        argv0);
}
