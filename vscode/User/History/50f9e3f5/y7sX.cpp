#include "filter_impl.h"

#include <cassert>
#include <chrono>
#include <cmath>
#include <cstdint>
#include <cstring>
#include <stdio.h>
#include <stdlib.h>
#include <thread>
#include <type_traits>

#include "color_conversion.h"
#include "logo.h"
#include "types.h"

// background analysis
#define NB_IMG 5
#define THRESHOLD 5
#define BLACK false
#define WHITE true
#define MORPHING_RADIUS 1

#define THRESHOLD_HYST_LOW 30
#define THRESHOLD_HYST_HIGH 50

#define GET(ptr, x, y, width) ((ptr) + (y) * (width) + (x))

static int bg_img_counter = 0;
static u32 *background = NULL;
static u32 *tmp1 = NULL;
static u32 *tmp2 = NULL;

void lab_delta_to_grayscale(u8 *img, u32 *bg, u32 *out, u32 height, u32 width,
                            u32 stride) {
    f32 delta_max = 0.f;

    // Find max
    for (u32 y = 0; y < height; y++) {
        rgb *lineptr = (rgb *)(img + y * stride);
        u32 *bg_ptr = (bg + y * width);
        f32 *line_out = (f32 *)(out + y * width);

        for (u32 x = 0; x < width; x++) {
            rgb *bg_pix = (rgb *)&bg_ptr[x];

            f32 delta = delta_e(lineptr[x], *bg_pix);
            if (delta > delta_max) {
                delta_max = delta;
            }

            // Store the delta in the tmp buffer.
            line_out[x] = delta;
        }
    }

    // Divide by max
    for (u32 y = 0; y < height; y++) {
        rgb *lineptr = (rgb *)(img + y * stride);
        f32 *line_out = (f32 *)(out + y * width);

        for (u32 x = 0; x < width; x++) {
            // Get the delta in the tmp buffer.
            f32 delta = line_out[x];

            // Normalize delta
            delta /= delta_max;

            lineptr[x] = {
                .r = (u8)(255.f * delta),
                .g = (u8)(255.f * delta),
                .b = (u8)(255.f * delta),
            };

            rgb *rgb_out = (rgb *)&line_out[x];
            *rgb_out = {
                .r = (u8)(255.f * delta),
                .g = (u8)(255.f * delta),
                .b = (u8)(255.f * delta),
            };

            // Buggy heatmap
            // lineptr[x] = {
            //     .r = 0,
            //     .g = (u8) (255.f * delta),
            //     .b = (u8) (255 * (1.f - delta))
            // };
        }
    }
}

void rec_hyst(bool *low, bool *high, int height, int width, int x, int y);

void dispatch_hyst(bool *low, bool *high, int height, int width, int x, int y) {
    if (x + 1 < width)
        rec_hyst(low, high, height, width, x + 1, y);
    if (x - 1 >= 0)
        rec_hyst(low, high, height, width, x - 1, y);
    if (y + 1 < height)
        rec_hyst(low, high, height, width, x, y + 1);
    if (y - 1 >= 0)
        rec_hyst(low, high, height, width, x, y - 1);
}

void rec_hyst(bool *low, bool *high, int height, int width, int x, int y) {
    bool *lowptr = (low + y * width);
    bool *highptr = (high + y * width);
    if (lowptr[x] == WHITE && highptr[x] == BLACK) {
        highptr[x] = WHITE;
        dispatch_hyst(low, high, height, width, x, y);
    }
}

void hysteresis(bool *low, bool *high, int height, int width) {
    for (int y = 0; y < height; y++) {
        bool *lowptr = (low + y * width);
        bool *highptr = (high + y * width);

        for (int x = 0; x < width; x++) {
            if (highptr[x] == WHITE) {
                dispatch_hyst(low, high, height, width, x, y);
            }
        }
    }
}

void erode(u8_4 *in, u8_4 *out, u32 height, u32 width) {
    for (i32 y = 0; y < height; y++) {
        u8_4 *line_out = (out + y * width);

        for (i32 x = 0; x < width; x++) {
            u8 min = 0xff;

            for (i32 dx = -MORPHING_RADIUS; dx <= MORPHING_RADIUS; ++dx) {
                for (i32 dy = -MORPHING_RADIUS; dy <= MORPHING_RADIUS; ++dy) {
                    // Do not check center pixel
                    if (dy == 0 && dx == 0) {
                        continue;
                    }
                    // Continue if outside of bounds
                    if (x + dx < 0 || x + dx >= width || y + dy < 0
                        || y + dy >= height) {
                        continue;
                    }

                    // get the input pixel
                    u8_4 *line = (in + (y + dy) * width);
                    u8 value = line[x + dx].b1; // Grayscale so r = g = b
                    if (value < min) {
                        min = value;
                    }
                }
            }

            line_out[x].b1 = min;
            line_out[x].b2 = min;
            line_out[x].b3 = min;
        }
    }
}

void dilate(u8_4 *in, u8_4 *out, u32 height, u32 width) {
    for (i32 y = 0; y < height; y++) {
        u8_4 *line_out = (out + y * width);

        for (i32 x = 0; x < width; x++) {
            u8 max = 0;

            for (i32 dx = -MORPHING_RADIUS; dx <= MORPHING_RADIUS; ++dx) {
                for (i32 dy = -MORPHING_RADIUS; dy <= MORPHING_RADIUS; ++dy) {
                    // Do not check center pixel
                    if (dy == 0 && dx == 0) {
                        continue;
                    }
                    // Continue if outside of bounds
                    if (x + dx < 0 || x + dx >= width || y + dy < 0
                        || y + dy >= height) {
                        continue;
                    }

                    // get the input pixel
                    u8_4 *line = (in + (y + dy) * width);
                    u8 value = line[x + dx].b1; // Grayscale so r = g = b
                    if (value > max) {
                        max = value;
                    }
                }
            }

            line_out[x].b1 = max;
            line_out[x].b2 = max;
            line_out[x].b3 = max;
        }
    }
}

/*
 * Binarize a grayscale image.
 */
void binarize(u32 *in, u32 *out, u8 thresh, u32 height, u32 width) {
    for (u32 y = 0; y < height; y++) {
        u8_4 *line_in = (u8_4 *)(in + y * width);
        u8_4 *line_out = (u8_4 *)(out + y * width);

        for (u32 x = 0; x < width; x++) {
            line_out[x].b1 = (line_in[x].b1 > thresh) ? 0xff : 0x00;

            // DEBUG : replicate data for green and blue
            line_out[x].b2 = line_out[x].b1;
            line_out[x].b3 = line_out[x].b1;
        }
    }
}

bool not_moved(rgb value, int_rgb ref) {
    /*
       printf("value: %d, %d, %d : ref: %d, %d, %d\n", value.r, value.g,
       value.b, ref.r, ref.g, ref.b);
       */
    return (value.r > (ref.r - THRESHOLD) && value.r < (ref.r + THRESHOLD))
        && (value.g > (ref.g - THRESHOLD) && value.g < (ref.g + THRESHOLD))
        && (value.b > (ref.b - THRESHOLD) && value.b < (ref.b + THRESHOLD));
}

void copy_to_strided_buffer(u32 *in, u8 *out, u32 height, u32 width,
                            u32 stride) {
    for (u32 y = 0; y < height; ++y) {
        rgb *buf_line_ptr = (rgb *)(out + y * stride);
        u32 *in_line_ptr = (tmp1 + y * width);
        for (u32 x = 0; x < width; ++x) {
            rgb *pix_in = (rgb *)&in_line_ptr[x];
            memcpy(&buf_line_ptr[x], pix_in, 3 * sizeof(u8));
        }
    }
}

// Superpose high and low on the same buffer
void debug_show_low_on_high(u32 *high, u32 *low, u32 height, u32 width) {
    for (u32 y = 0; y < height; ++y) {
        u32 *line_high = (high + y * width);
        u32 *line_low = (low + y * width);
        for (u32 x = 0; x < width; ++x) {
            rgb *pix_high = (rgb *)&line_high[x];
            rgb *pix_low = (rgb *)&line_low[x];

            pix_high->r = pix_high->r && ~pix_low->r;
            pix_high->g = pix_low->g;
            pix_high->b = 0;
        }
    }
}

void propagate_high_from_low(u8_4 *high, u8_4 *low, u32 height, u32 width) {
    u8_4 *tmp = (u8_4 *)malloc(height * width * sizeof(u8_4));
    if (tmp == NULL) {
        printf("Explosion");
        std::exit(3);
    }

    u8_4 *from = high;
    u8_4 *to = tmp;

    do {
        for (u32 y = 0; y < height; ++y) {
            for (u32 x = 0; x < width; ++x) {
                u8_4 *pix_from = GET(from, x, y, width);
                if (pix_from->b1 == 0) {
                    // Off, do not propagate to others
                    continue;
                }

                // Pixel is on, propagate to other pixels
                if (y > 0) {
                    *GET(low, x, y - 1, width) = {
                        .b1 = 0xff,
                        .b2 = 0xff,
                        .b3 = 0xff,
                    };
                }

                if (y < height - 1) {
                    *GET(low, x, y + 1, width) = {
                        .b1 = 0xff,
                        .b2 = 0xff,
                        .b3 = 0xff,
                    };
                }
                    || (x > 0 && GET(low, x - 1, y, width)->b1 != 0)
                    || (x < width - 1 && GET(low, x + 1, y, width)->b1 != 0)) {
                    pix_from->b1 = 0xff;
                    pix_from->b2 = 0xff;
                    pix_from->b3 = 0xff;
                }
            }
        }
        std::swap(from, to);
    } while (memcmp(from, to, height * width * sizeof(u8_4)) != 0);

    if (to != high) {
        // memcpy
    }

    free(tmp);
}

extern "C" {
void filter_impl(uint8_t *buffer, int width, int height, int stride,
                 int pixel_stride) {
    /*
    buffer (u8) -> img source / output
    background (u8) -> Store the background image
    tmp1 (u8) -> Store the deltaLab grayscale, and hysteriesis low
    tmp2 (u8) -> Store the morphed deltaLab, hysteriesis high, and final
    hysterisis result
    */

    assert(sizeof(u8_4) == sizeof(u32));

    // printf("ENTER IN FILTER FUNCTION %d\n", bg_img_counter);
    if (background == NULL) {
        // Save NB_IMG frames
        background = (u32 *)calloc(width * height * NB_IMG, sizeof(u32));
        if (background == NULL) {
            printf("background EXPLOSION\n");
            return;
        }
    }

    if (tmp1 == NULL) {
        tmp1 = (u32 *)malloc(width * height * sizeof(u32));
        if (tmp1 == NULL) {
            printf("low image EXPLOSION\n");
            return;
        }
    }

    if (tmp2 == NULL) {
        tmp2 = (u32 *)malloc(width * height * sizeof(u32));
        if (tmp2 == NULL) {
            printf("high image EXPLOSION\n");
            return;
        }
    }

    // cf = current_frame
    int image_size = width * height;
    int cf = (bg_img_counter % NB_IMG) * image_size;
    // printf("CF : %d %d\n", cf, image_size);

    // If img_counter < nb_image, copy the buffer to the background
    if (bg_img_counter == 0) {
        for (u32 y = 0; y < height; ++y) {
            rgb *buf_line_ptr = (rgb *)(buffer + y * stride);
            u32 *bg_line_ptr = (background + y * width);
            for (u32 x = 0; x < width; ++x) {
                rgb *bg_pix = (rgb *)&bg_line_ptr[x];
                memcpy(bg_pix, &buf_line_ptr[x], 3 * sizeof(u8));
            }
        }
    } else {
        lab_delta_to_grayscale(buffer, background, tmp1, height, width, stride);
        erode((u8_4 *)tmp1, (u8_4 *)tmp2, height, width);
        dilate((u8_4 *)tmp2, (u8_4 *)tmp1, height, width);

        // Look at tmp1, compute and put low in tmp2
        // Note: At this point, we waste space because there is 32bits in
        // the pixels. But at least we avoid reallocating a buffer for the
        // exact size
        binarize(tmp1, tmp2, THRESHOLD_HYST_LOW, height, width);

        // Look at tmp1, compute and put high in tmp1
        binarize(tmp1, tmp1, THRESHOLD_HYST_HIGH, height, width);

        // DEBUG: merge low and high
        // debug_show_low_on_high(tmp1, tmp2, height, width);

        // Spread high to low with hysteriesis

        // Copy tmp1 into buffer
        copy_to_strided_buffer(tmp1, buffer, height, width, stride);
    }

    // for (int y = 0; y < height; ++y)
    // {
    //     rgb* lineptr = (rgb*) (buffer + y * stride);
    //     rgb* bg_ptr = (background + cf + y * width);
    //     bool* low_ptr = (tmp1 + y * width);
    //     bool* high_ptr = (tmp2 + y * width);

    //     for (int x = 0; x < width; ++x)
    //     {
    //         if (bg_img_counter >= NB_IMG)
    //         {
    //             //int cf_test = (bg_img_counter-1 % NB_IMG) * image_size;
    //             //rgb* bg_test = (bg_img + cf_test + y);

    //             rgb pixel;
    //             int_rgb ref;
    //             ref.r = 0;
    //             ref.g = 0;
    //             ref.b = 0;
    //             for (int i = 0; i < NB_IMG; i++)
    //             {
    //                 pixel = bg_img[i * image_size + y*width + x];
    //                 ref.r += pixel.r;
    //                 ref.g += pixel.g;
    //                 ref.b += pixel.b;
    //             }
    //             ref.r /= NB_IMG;
    //             ref.g /= NB_IMG;
    //             ref.b /= NB_IMG;

    //             if (not_moved(lineptr[x], ref)) {
    //                 low_ptr[x] = BLACK;
    //                 high_ptr[x] = BLACK;
    //                 src_ptr[x] = BLACK;
    //             } else {
    //                 // white == Move
    //                 low_ptr[x] = WHITE;
    //                 high_ptr[x] = WHITE;
    //                 src_ptr[x] = WHITE;
    //             }
    //         }
    //         bg_ptr[x].r = uint8_t (lineptr[x].r);
    //         bg_ptr[x].b = uint8_t (lineptr[x].b);
    //         bg_ptr[x].g = uint8_t (lineptr[x].g);
    //     }
    // }

    // printf("END FIRST LOOP\n");

    // if (bg_img_counter >= NB_IMG)
    // {
    //     lab_delta_to_grayscale(buffer, bg_img, height, width, stride);

    // morphing(src_img, height, width, high_img, BLACK);
    // //printf("AFTER MORPHING BLACK\n");
    // morphing(src_img, height, width, low_img, WHITE);
    // //printf("AFTER WHITE BLACK\n");

    // hysteresis(low_img, high_img, height, width);

    // for (int y = 0; y < height; ++y)
    // {
    //     rgb* lineptr = (rgb*) (buffer + y * stride);
    //     bool* img_ptr = (high_img + y * width);
    //     for (int x = 0; x < width; ++x)
    //     {
    //         if (img_ptr[x] == WHITE) {
    //             int tmp = lineptr[x].r + 127;
    //             lineptr[x].r = tmp > 255 ? 255 : tmp;
    //         }
    //     }
    // }
    // }

    bg_img_counter++;

    // You can fake a long-time process with sleep
    {
        using namespace std::chrono_literals;
        // std::this_thread::sleep_for(100ms);
    }
}
}
