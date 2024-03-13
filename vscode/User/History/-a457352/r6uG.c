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
    struct data_t *data, zero = { 0 };

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