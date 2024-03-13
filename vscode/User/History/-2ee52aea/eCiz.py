#!/usr/bin/env python
# @lint-avoid-python-3-compatibility-imports

from bcc import BPF
import bcc.utils as utils
from time import sleep


bpf_text = """
#include <linux/sched.h>

struct data_t {
    u32 max_latency;
    u32 avg_latency;
};

BPF_HASH(my_map, pid_t, struct data_t);

static int trace_enqueue(u32 tgid, u32 pid)
{
    u64 ts = bpf_ktime_get_ns();
    start.update(&pid, &ts);
    return 0;
}

int trace_wake_up_new_task(struct pt_regs *ctx, struct task_struct *p)
{
    return trace_enqueue(p->tgid, p->pid);
}

int trace_ttwu_do_wakeup(struct pt_regs *ctx, struct rq *rq, struct task_struct *p,
    int wake_flags)
{
    return trace_enqueue(p->tgid, p->pid);
}

"""

print("Tracing sys_sync()... Ctrl-C to end")
b = BPF(text=bpf_text)

while True:
    print(dict(b.get_table("my_map")))
    sleep(1)