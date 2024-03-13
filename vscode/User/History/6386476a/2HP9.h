#pragma once

/**
 * Use the seccomp syscall to blacklist some syscalls.
 * @note: Upon non compliance, the process will be killed.
 */
int moulette_seccomp_init(void);