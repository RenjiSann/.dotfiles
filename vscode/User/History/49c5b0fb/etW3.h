#pragma once

#include <stdlib.h>

#include "log.h"

#define die(EXIT_CODE, ...) {log_fatal(__VA_ARGS__); _exit(EXIT_CODE);}

/**
 * Utility function for writing to a file.
 */
int write_to_file(const char *path, const char *content);