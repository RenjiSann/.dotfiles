#pragma once

#include "moulette_opts.h"

/**
 * Compute a hash from the opts and the current timestamp and change the current
 * hostname to this hash.
 * @note: Must be run in a separated UTS namespace, otherwise will affect the
 * actual hostname of the computer.
 */
int moulette_set_hostname(moulette_opts *opts);

/**
 * Set the /proc/$pid/[ug]id_map files of the user namespaced process $pid
 * to enable user mapping.
 * @note: Must be run on the HOST process, because the cloned process is also
 * isolated in a PID namespace, so it is unable to edit the right procfs.
 */
void moulette_set_userns_mappings(pid_t pid);
