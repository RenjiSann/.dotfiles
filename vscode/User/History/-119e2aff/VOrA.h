#pragma once

#include "moulette_opts.h"

/**
 * Compute a hash from the opts and the current timestamp and change the current
 * hostname to this hash.
 * @note: To be run in isolated UTS namespace
 */
int moulette_set_hostname(moulette_opts *opts);