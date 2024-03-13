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


# code substitutions
if BPF.kernel_struct_has_field(b'task_struct', b'__state') == 1:
    state_field = '__state'
else:
    state_field = 'state'

# process event
def print_event(cpu, data, size):
    event = b["events"].event(data)
    # if args.previous:
    #     print("%-8s %-16s %-6s %14s %-16s %-6s" % (strftime("%H:%M:%S"), event.task.decode('utf-8', 'replace'), event.pid, event.delta_us, event.prev_task.decode('utf-8', 'replace'), event.prev_pid))
    # else:
    print("%-8s %-16s %-6s %-6s %14s" % (strftime("%H:%M:%S"), event.task.decode('utf-8', 'replace'), event.pid, event.tgid, event.delta_us))


max_pid = int(open("/proc/sys/kernel/pid_max").read())

# load BPF program
b = BPF(src_file="bpf.c",
        cflags=["-DMAX_PID=%d" % max_pid, "-DSTATE_FIELD=%s" % state_field])
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
    avg_lat = "AVG(us)"
    max_lat = "MAX(us)"
    nb_events = "COUNT"
    comm = "COMM"
    exe = "EXE"
    argv = "ARGV"

    s = f'{tgid:<7} {avg_lat:>8} {max_lat:>8} ' \
        f'{nb_events:<6} {comm:<16} {exe:<16} {argv}'
    s2 = "=" * len(s)
    print(s)
    print(s2)

def print_line(tgid, data_t, argv):
    # print(f'{tgid:<7} {data_t.avg_delta:>8} {data_t.max_delta:>8}'
    #       '{number_of_events:>6} {comm:>16} {exe:>16} {argv}')
    exe = "EXE"
    avg_us = data_t.avg_delta // 1000
    max_us = data_t.max_delta // 1000
    if len(argv) > 80:
        argv= argv[:77] + "..."
    print(f'{tgid:>7} {avg_us:>8} {max_us:>8} '
          f'{data_t.nb_sched:>6} {str(data_t.task):>16} {exe:>16} {argv}')

# read events
argv_cache = {}
def get_argv(tgid):
    if tgid in argv_cache.keys():
        return argv_cache[tgid]
    argv = open(f"/proc/{tgid}/cmdline").read().replace('\0', ' ')
    argv_cache[tgid] = argv
    return argv

while 1:
    print_header()
    d = b["output"]
    for tgid, v in d.items():
        tgid = tgid.value
        print_line(tgid, v, get_argv(tgid))
    sleep(1)
