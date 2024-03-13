#ifndef _GCOV_SYSCALL_H
#define _GCOV_SYSCALL_H

typedef int (*dump_fn)(const char *buf, int len);

int _gcov_open_file(const char *name, int flags, int mode);
int _gcov_write_file(int file, char *ptr, int len);

#endif // _GCOV_SYSCALL_H
