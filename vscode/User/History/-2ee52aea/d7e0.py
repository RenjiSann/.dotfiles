#!/usr/bin/env python
# @lint-avoid-python-3-compatibility-imports

from bcc import BPF
from bcc.containers import filter_by_containers
from bcc.utils import ArgString, printb
import bcc.utils as utils


bpf_text = """
#include <linux/sched.h>

struct data_t {
    u32 max_latency;
    u32 avg_latency;
};

BPF_HASH(my_map, pid_t, struct data_t);

int kprobe__sys_clone(void *ctx)
{
    bpf_trace_printk("Hello, World!\\n");
    return 0;
}

int kprobe__sys_sync(void *ctx)
{
    bpf_trace_printk("sys_sync() called\\n");
    return 0;
}

"""

print("Tracing sys_sync()... Ctrl-C to end")
b = BPF(text=bpf_text).trace_print()

while True:
    print(b.get_table("my_map"))
    sleep(1000)