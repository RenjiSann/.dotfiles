#pragma once

#include "moulette_opts.h"

/**
 * Compute a hash from the opts and the current timestamp and change the current
 * hostname to this hash.
 * @note: Must be run in a separated UTS namespace, otherwise will affect the
 * actual hostname of the computer.
 */
int moulette_set_hostname(moulette_opts *opts);