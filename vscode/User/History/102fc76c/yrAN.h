#pragma once

#include <cstdint>

typedef float f32;
typedef uint8_t u8;
typedef uint16_t u16;
typedef uint32_t u32;
typedef uint64_t u64;
typedef int8_t i8;
typedef int16_t i16;
typedef int32_t i32;
typedef int64_t i64;

struct u8_4 {
    u8 b1, b2, b3, b4; // When used for storing colors, b1 = r, b2 = g, b3 = b
};

struct rgb {
    u8 r, g, b;
};

struct cie_xyz {
    f32 x, y, z;
};

// Use https://www.easyrgb.com/en/math.php D65 reference values
#define REF_X 94.811f
#define REF_Y 100.f
#define REF_Z 107.304f

struct cie_lab {
    f32 l, a, b;
};
