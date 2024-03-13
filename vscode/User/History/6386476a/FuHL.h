#pragma once

/// Use the seccomp syscall to blacklist some syscalls.
int seccomp_init(void);