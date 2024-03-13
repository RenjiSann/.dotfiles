#include <stdio.h>

#include "coverage.h"

int this_is_a_test(int a) {
    if (a < 0) {
        return -1;
    } else {
        return a + 1;
    }
}

int main() {
    printf("Hello World %d\n", this_is_a_test(13));
#ifdef COVERAGE
    coverage_dump();
#endif
    return 0;
}