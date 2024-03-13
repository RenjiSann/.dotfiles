#!/usr/bin/env python
# @lint-avoid-python-3-compatibility-imports

from bcc import BPF
import bcc.utils as utils
from time import sleep


bpf_text = """
#include <linux/sched.h>

struct data_t {
    u64 init_time;
    u64 max_latency;
    u64 avg_latency;
};

BPF_HASH(my_map, pid_t, struct data_t);

static int trace_enqueue(u32 tgid, u32 pid)
{
    u64 ts = bpf_ktime_get_ns();
    my_map.update(&pid, &ts);
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
b.attach_kprobe(event="ttwu_do_wakeup", fn_name="trace_ttwu_do_wakeup")
b.attach_kprobe(event="wake_up_new_task", fn_name="trace_wake_up_new_task")

table = b.get_table("my_map")
while True:

    for k in table:
        print(f"{int(k)}: {table[k]}")

    print ("--------")
    sleep(1)