#include "seccomp.h"

int seccomp_init(void) {
    struct sock_filter filter[] = {
        BPF_STMT(BPF_LD | BPF_W | BPF_ABS, offsetof(struct seccomp_data, nr)), // Load syscall number
        BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K, __NR_clock_nanosleep, 0, 1), // If syscall is clock_nanosleep, jump to the next instruction
        BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_KILL), // Deny the syscall
        BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_ALLOW), // Allow all other syscalls
    };
    struct sock_fprog prog = {
        .len = 4,
        .filter = filter,
    };

}