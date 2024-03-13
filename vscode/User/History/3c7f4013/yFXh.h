#pragma once

#include "types.h"

inline cie_xyz rgb2xyz(rgb color);
inline cie_lab xyz2lab(cie_xyz color);
inline f32 delta_e(rgb c1, rgb c2);

#include "color_conversion.hxx"
