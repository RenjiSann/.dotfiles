#pragma once

#include <stddef.h>
#include <stdint.h>

#define FILTER_DEFAULT_LOW 3
#define FILTER_DEFAULT_HIGH 30


#ifdef __cplusplus
extern "C" {
#endif

struct filter_params {
    int th_low;
    int th_high;
};

void filter_impl(uint8_t *buffer, int width, int height, int plane_stride,
                 int pixel_stride, struct filter_params *params);

#ifdef __cplusplus
}
#endif
