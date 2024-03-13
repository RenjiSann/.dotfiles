#pragma once

#include "types.h"

inline u32 fnv32_hash(const char *str, u64 len)
{
    unsigned char *s = (unsigned char *)str;	/* unsigned string */

    /* See the FNV parameters at www.isthe.com/chongo/tech/comp/fnv/#FNV-param */
    const u32 FNV_32_PRIME = 0x01000193; /* 16777619 */

    u32 h = 0x811c9dc5; /* 2166136261 */
    while (len--) {
        /* xor the bottom with the current octet */
        h ^= *s++;
        /* multiply by the 32 bit FNV magic prime mod 2^32 */
        h *= FNV_32_PRIME;
    }

    return h;
}

inline void u32_to_hexa(u32 n, char out[8]) {

}