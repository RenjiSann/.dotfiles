#define _DEFAULT_SOURCE

#include <curl/curl.h>
#include <curl/easy.h>
#include <errno.h>
#include <stdlib.h>
#include <string.h>

#include "log.h"
#include "types.h"

#define TMPDIR_TEMPLATE "/tmp/moulette_XXXXXX"

static int pull_image(const char *image, const char *dl_dir);

int image_pull_then_init(const char *image,
                         __attribute((unused)) char *out_path,
                         __attribute((unused)) u32 len) {
    // Steps:
    // 1. Create a temp directory
    // 2. Download the image archive to the tempdir
    // 3. Decompress the archive in the tempdir
    // 4. Put the output in out_path
    //    int err = 0;
    char tmpdir[] = TMPDIR_TEMPLATE;

    log_info("Pulling image %s...", image);

    // Create a tmpdir
    if (mkdtemp(tmpdir) == NULL) {
        log_error("Failed to create tmpdir: %s", strerror(errno));
        return 1;
    }
    log_debug("Created tmpdir: `%s`", tmpdir);

    // Download the image to the tmpdir
    if (pull_image(image, tmpdir) != 0) {
        return 1;
    }

    return 0;
}

// Populate preallocated buffer with the download url
static void get_url(const char *image, char *buffer) {
    char *colon;
    char *version;
    i32 name_len;

    // `image` should be of the form "[author/]image[:version]"
    colon = strstr(image, ":");
    if (colon == NULL) {
        version = "latest";
        name_len = strlen(image);
    } else {
        if (*(colon + 1) == '\0') {
            log_error("Invalid image format");
            return;
        }
        version = colon + 1;
        name_len = colon - image;
    }

    sprintf(buffer, "https://registry-1.docker.io/v2/%.*s/manifests/%s",
            name_len, image, version);
}

// static int request_token(const char *image) {
//     const char* URL =
//     "https://auth.docker.io/token?service=registry.docker.io&scope=repository:samalba/my-app:pull";
//
//     return 0;
// }

static int pull_image(const char *image,
                      __attribute((unused)) const char *dl_dir) {
    char url_buf[1024];
    CURL *curl;
    CURLcode code;

    get_url(image, url_buf);
    log_debug("Pulling image from `%s`", url_buf);

    curl = curl_easy_init();
    if (curl == NULL) {
        log_error("Failed to initialize curl context");
    }

    curl_easy_setopt(curl, CURLOPT_URL, url_buf);
    code = curl_easy_perform(curl);
    curl_easy_cleanup(curl);

    if (code != CURLE_OK) {
        log_debug("CURL said oof");
        return 1;
    }

    return 0;
}
