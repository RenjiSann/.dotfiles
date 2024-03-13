#ifndef _GCOV_COVERAGE_H
#define _GCOV_COVERAGE_H

#include "dump.h"

int gcov_coverage_dump();
void gcov_set_dump_function(dump_fn fn);

#endif // _GCOV_COVERAGE_H
