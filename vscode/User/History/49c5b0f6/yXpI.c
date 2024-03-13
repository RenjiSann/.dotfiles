#include "utils.h"

#include <fcntl.h>
#include <stdio.h>
#include <unistd.h>

#include "log.h"

int write_to_file(const char *path, const char *content) {
    int fd = open(path, O_WRONLY);
}