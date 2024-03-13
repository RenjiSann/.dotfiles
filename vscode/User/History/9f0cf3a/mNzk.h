#pragma once

#include <stddef.h>
#include <stdint.h>

struct filter_params {
    int th_low;
    int th_high;
};

#ifdef __cplusplus
extern "C" {
#endif

void filter_impl(uint8_t *buffer, int width, int height, int plane_stride,
                 int pixel_stride, filter_params *params);

#ifdef __cplusplus
}
#endif
