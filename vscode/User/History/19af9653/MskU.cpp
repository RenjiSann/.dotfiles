#include "color_conversion.h"

#include <cmath>

// https://www.easyrgb.com/en/math.php
inline cie_xyz rgb2xyz(rgb color) {
    cie_xyz ret;
    f32 vr = ((f32)color.r) / 255.;
    f32 vg = ((f32)color.g) / 255.;
    f32 vb = ((f32)color.b) / 255.;

    vr = (vr > 0.04045) ? std::pow((vr + 0.055f) / 1.055f, 2.4f) : vr / 12.92f;
    vg = (vg > 0.04045) ? std::pow((vg + 0.055f) / 1.055f, 2.4f) : vg / 12.92f;
    vb = (vb > 0.04045) ? std::pow((vb + 0.055f) / 1.055f, 2.4f) : vb / 12.92f;
    vr *= 100.f;
    vg *= 100.f;
    vb *= 100.f;

    ret.x = vr * 0.4124f + vg * 0.3576f + vb * 0.1805f;
    ret.y = vr * 0.2126f + vg * 0.7152f + vb * 0.0722f;
    ret.z = vr * 0.0193f + vg * 0.1192f + vb * 0.9505f;
    return ret;
}

inline cie_lab xyz2lab(cie_xyz color) {
    cie_lab ret;
    f32 vx = color.x / REF_X;
    f32 vy = color.y / REF_Y;
    f32 vz = color.z / REF_X;

    vx = (vx > 0.008856) ? std::pow(vx, 1.f / 3.f) : (vx * 7.87f) + (16.f / 116.f);
    vy = (vy > 0.008856) ? std::pow(vy, 1.f / 3.f) : (vy * 7.87f) + (16.f / 116.f);
    vz = (vz > 0.008856) ? std::pow(vz, 1.f / 3.f) : (vz * 7.87f) + (16.f / 116.f);

    ret.l = (vy * 116.f) - 16.f;
    ret.a = 500 * (vx - vy);
    ret.b = 200 * (vy - vz);
    return ret;
}