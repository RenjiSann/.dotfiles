#!/usr/bin/env python
# @lint-avoid-python-3-compatibility-imports
#
# runqslower    Trace long process scheduling delays.
#               For Linux, uses BCC, eBPF.
#
# This script traces high scheduling delays between tasks being
# ready to run and them running on CPU after that.
#
# USAGE: runqslower [-p PID] [-t TID] [-P] [min_us]
#
# REQUIRES: Linux 4.9+ (BPF_PROG_TYPE_PERF_EVENT support).
#
# This measures the time a task spends waiting on a run queue for a turn
# on-CPU, and shows this time as a individual events. This time should be small,
# but a task may need to wait its turn due to CPU load.
#
# This measures two types of run queue latency:
# 1. The time from a task being enqueued on a run queue to its context switch
#    and execution. This traces ttwu_do_wakeup(), wake_up_new_task() ->
#    finish_task_switch() with either raw tracepoints (if supported) or kprobes
#    and instruments the run queue latency after a voluntary context switch.
# 2. The time from when a task was involuntary context switched and still
#    in the runnable state, to when it next executed. This is instrumented
#    from finish_task_switch() alone.
#
# Copyright 2016 Cloudflare, Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
#
# 02-May-2018   Ivan Babrou   Created this.
# 18-Nov-2019   Gergely Bod   BUG fix: Use bpf_probe_read_kernel_str() to extract the
#                               process name from 'task_struct* next' in raw tp code.
#                               bpf_get_current_comm() operates on the current task
#                               which might already be different than 'next'.

from __future__ import print_function
from bcc import BPF
import argparse
from time import strftime, sleep

# define BPF program
bpf_text = """
#include <uapi/linux/ptrace.h>
#include <linux/sched.h>
#include <linux/nsproxy.h>
#include <linux/pid_namespace.h>

struct data_t {
    char task[TASK_COMM_LEN];
    u64 max_delta;
    u64 avg_delta;
    u64 nb_sched;
};

BPF_ARRAY(start, u64, MAX_PID);
BPF_HASH(output, u32, struct data_t, MAX_PID);

// record enqueue timestamp
static int trace_enqueue(u32 tgid, u32 pid)
{
    struct data_t *data;
    u32 zero = 0;

    // Do not record pid 0, nor kernel threads (tgid = 2)
    if (pid == 0 || tgid == 2 || pid == 2) {
        return 0;
    }
    u64 ts = bpf_ktime_get_ns();
    start.update(&pid, &ts);

    data = output.lookup_or_try_init(&tgid, &zero);
    ++data->nb_sched;
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

// calculate latency
int trace_scheduling_done(struct pt_regs *ctx, struct task_struct *prev)
{
    u32 pid, tgid;

    // Involuntary context switch:
    // The stopped task is re-enqueued at this timestamp.
    if (prev->STATE_FIELD == TASK_RUNNING) {
        tgid = prev->tgid;
        pid = prev->pid;
        u64 ts = bpf_ktime_get_ns();
        if (pid != 0 && tgid != 2 && pid != 2) {
            start.update(&pid, &ts);
        }
    }

    pid = bpf_get_current_pid_tgid();
    tgid = bpf_get_current_pid_tgid() >> 32;

    u64 *tsp, delta_ns;

    // fetch timestamp and calculate delta
    tsp = start.lookup(&pid);
    if ((tsp == NULL) || (*tsp == 0)) {
        return 0;   // missed enqueue
    }

    delta_ns = (bpf_ktime_get_ns() - *tsp);

    struct data_t *data_ptr = output.lookup(&tgid);
    struct data_t data = { 0 };
    bpf_get_current_comm(&data.task, sizeof(data.task));

    // First pid of the tgid group
    if (data_ptr == NULL) {
        data_ptr = &data;
    }

    // Override max-latency
    if (delta_ns > data_ptr->max_delta) {
        data_ptr->max_delta = delta_ns;
    }


    // Update hashtable
    output.update(&tgid, data_ptr);

    //array map has no delete method, set ts to 0 instead
    *tsp = 0;
    return 0;
}
"""

# code substitutions
if BPF.kernel_struct_has_field(b'task_struct', b'__state') == 1:
    bpf_text = bpf_text.replace('STATE_FIELD', '__state')
else:
    bpf_text = bpf_text.replace('STATE_FIELD', 'state')

# process event
def print_event(cpu, data, size):
    event = b["events"].event(data)
    # if args.previous:
    #     print("%-8s %-16s %-6s %14s %-16s %-6s" % (strftime("%H:%M:%S"), event.task.decode('utf-8', 'replace'), event.pid, event.delta_us, event.prev_task.decode('utf-8', 'replace'), event.prev_pid))
    # else:
    print("%-8s %-16s %-6s %-6s %14s" % (strftime("%H:%M:%S"), event.task.decode('utf-8', 'replace'), event.pid, event.tgid, event.delta_us))


max_pid = int(open("/proc/sys/kernel/pid_max").read())

# load BPF program
b = BPF(text=bpf_text, cflags=["-DMAX_PID=%d" % max_pid])
b.attach_kprobe(event="ttwu_do_wakeup", fn_name="trace_ttwu_do_wakeup")
b.attach_kprobe(event="wake_up_new_task", fn_name="trace_wake_up_new_task")
b.attach_kprobe(event_re="^finish_task_switch$|^finish_task_switch\.isra\.\d$",
                fn_name="trace_scheduling_done")

print("Tracing run queue latency higher than 0 us")
# if args.previous:
#     print("%-8s %-16s %-6s %14s %-16s %-6s" % ("TIME", "COMM", "TID", "LAT(us)", "PREV COMM", "PREV TID"))
# else:
print("%-8s %-16s %-6s %-6s %14s" % ("TIME", "COMM", "PID", "TGID", "LAT(us)"))

def print_header():
    tgid = "TGID"
    avg_lat = "AVG LAT"
    max_lat = "MAX LAT"
    nb_events = "NB EVENTS"
    comm = "COMM"
    exe = "EXE"
    argv = "ARGV"
    print(f'{tgid:<7} {avg_lat:>8} {max_lat:>8}'
          f'{nb_events:>6} {comm:>16} {exe:>16} {argv}')

def print_line(tgid, data_t):
    # print(f'{tgid:<7} {data_t.avg_delta:>8} {data_t.max_delta:>8}'
    #       '{number_of_events:>6} {comm:>16} {exe:>16} {argv}')
    print(f'{tgid.value:<7} {data_t.avg_delta:>8} {data_t.max_delta:>8}'
          f'{"xxx":>6} {data_t.task:>16} {"xxx":>16} {"xxx"}')

# read events
while 1:
    print_header()
    d = b["output"]
    for tgid, v in d.items():
        print_line(tgid, v)
    sleep(1)
