#ifndef _GCOV_COVERAGE_H
#define _GCOV_COVERAGE_H

typedef int (*dump_fn)(const char *buf, int len);

int coverage_dump();

void set_dump_function()

#endif // _GCOV_COVERAGE_H
