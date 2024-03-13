#include <stdio.h>

int this_is_a_test(int a) {
    if (a < 0) {
        return -1;
    } else {
        return a + 1;
    }
}

int main() {
    printf("Hello World %d\n", this_is_a_test(13));
    return 0;
}