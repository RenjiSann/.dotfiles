#pragma once

#include <filesystem>
#include <string>
#include <vector>
namespace fs = std::filesystem;

#include "types.h"

struct cg_info {
    std::string name;
    fs::path path; // Path to the cgroup from the cgroup root
    cg_info *parent;
    u32 nb_procs;
    std::vector<cg_info> children;
};

void cg_init(void);
void cg_clear(void);

/// Populate the given struct with current cgroup info
void cg_get_current(cg_info *cgroup);

/// Fill the given vector withall the PIDs directly attached to the
/// given cgroup. Also update the number of processes in cg_info.
void cg_list_procs(std::vector<u32> *out, cg_info *cgroup);
