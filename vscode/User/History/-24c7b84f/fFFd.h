#ifndef _GCOV_COVERAGE_H
#define _GCOV_COVERAGE_H

#include "dump.h"

/**
 * Dumps the coverage data to file system
 * @return Zero on success
 * @note Using the subs in syscall.c will use a kind of leight weight
 * filesystem which uses the serial interface to transfer the coverage data from
 * the embedded platform to a host computer.
 */
int gcov_coverage_dump();

/**
 * Set the coverage dump function that will be used to send
 * coverage data.
 */
void gcov_set_dump_function(dump_fn fn);

#endif // _GCOV_COVERAGE_H
