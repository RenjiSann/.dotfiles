#include "utils.h"

#include <errno.h>
#include <fcntl.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>

#include "log.h"

int write_to_file(const char *path, const char *content) {
    int fd = open(path, O_WRONLY);

    if (fd == -1) {
        log_error("%s: Failed to open file: %s", __func__, strerror(errno));
        return 1;
    }

    if (dprintf(fd, "%s", content) < 0) {
        log_error("%s: Failed to write file: %s", __func__, strerror(errno));
        return 1;
    }

    close(fd);
    return 0;
}