#include "capabilities.h"

#include <errno.h>
#include <string.h>
#include <sys/capability.h>

#include "log.h"

static int is_in_array(cap_value_t to_test, const cap_value_t *to_keep,
                       size_t nb_capa);
static void printcaps(const char *prefix, cap_flag_t which);

/// Make sure the CAP_NET_RAW capability is put into the ambient set.
/// Return 0 on success.
int capa_init_ambient(void) {
    int res = 0;
    cap_iab_t iab = cap_iab_get_proc();
    if (iab == NULL) {
        log_error("Cannot get ambient capability set: %s", strerror(errno));
        res = -1;
        goto exit;
    }

    cap_value_t cap_to_enable[] = { CAP_NET_RAW, 0 };
    char *txt;

    for (size_t i = 0; cap_to_enable[i] != 0; i++) {
        res = cap_iab_set_vector(iab, CAP_IAB_AMB, cap_to_enable[i], CAP_SET);
        if (res != 0) {
            txt = cap_to_name(cap_to_enable[i]);
            log_error("Cannot set %s to ambient set: %s", txt, strerror(errno));
        }
    }

    cap_free(iab);
exit:
    return res;
}

int capa_init_fork(void) {
    const cap_value_t capas_to_add[] = { CAP_NET_RAW };
    size_t nb_capa = 1;

    // 1. Clear the inheritable set, we don't want to inherit random
    // capabilities.
    // 2. Add CAP_NET_RAW to inheritable.
    // 3. Add CAP_NET_RAW to ambient
    cap_t cap = cap_get_proc();
    if (cap == NULL) {
        log_error("Unable to get capabilities");
    }

    if (cap_clear_flag(cap, CAP_INHERITABLE) != 0) {
        log_error("Unable to clear inheritable set: %s", strerror(errno));
        goto error_free;
    }

    if (cap_set_flag(cap, CAP_INHERITABLE, nb_capa, capas_to_add, CAP_SET)
        != 0) {
        log_error("Unable to set cap flag");
        goto error_free;
    }

    if (cap_set_proc(cap) != 0) {
        log_error("Unable to set capabilities: %s", strerror(errno));
        goto error_free;
    }

    cap_free(cap);

    char *txt;

    for (size_t i = 0; i < nb_capa; i++) {
        if (cap_set_ambient(capas_to_add[i], CAP_SET) != 0) {
            txt = cap_to_name(capas_to_add[i]);
            log_error("Unable to set ambient %s: %s", txt, strerror(errno));
            return 1;
        }
    }

    // Iterate through all capabilities to drop them
    for (cap_value_t cap_val = 0; cap_val <= CAP_LAST_CAP; cap_val++) {
        if (!is_in_array(cap_val, capas_to_add, nb_capa)) {
            if (cap_drop_bound(cap_val) != 0) {
                char *txt = cap_to_name(cap_val);
                log_error("Unable to drop %s: %s", txt, strerror(errno));
                cap_free(txt);
                return 1;
            }
        }
    }

    return 0;
error_free:
    cap_free(cap);
    return 1;
}

void print_effective(void) {
    printcaps("Effective capabilities:\n", CAP_EFFECTIVE);
}

void print_permitted(void) {
    printcaps("Permitted capabilities:\n", CAP_PERMITTED);
}

void print_inheritable(void) {
    printcaps("Inheritable capabilities:\n", CAP_INHERITABLE);
}

void print_bounding(void) {
    int count = 0;
    char *txt;

    fputs("Bounding capabilities\n", stdout);

    for (cap_value_t cap_val = 0; cap_val <= CAP_LAST_CAP; cap_val++) {
        if (cap_get_bound(cap_val)) {
            txt = cap_to_name(cap_val);
            fprintf(stdout, "%s", txt);
            count++;
            if (count == 6) {
                fputc('\n', stdout);
                count = 0;
            } else {
                fprintf(stdout, ", ");
            }
            cap_free(txt);
        }
    }

    fprintf(stdout, "\n\n");
    fflush(stdout);
}

void print_ambient(void) {
    int count = 0;
    char *txt;

    fputs("Ambient capabilities:\n", stdout);

    for (cap_value_t cap_val = 0; cap_val <= CAP_LAST_CAP; cap_val++) {
        if (cap_get_ambient(cap_val)) {
            txt = cap_to_name(cap_val);
            fputs(txt, stdout);
            count++;
            if (count == 6) {
                fputc('\n', stdout);
                count = 0;
            } else {
                fprintf(stdout, ", ");
            }
            cap_free(txt);
        }
    }

    fprintf(stdout, "\n\n");
    fflush(stdout);
}

static void printcaps(const char *prefix, cap_flag_t which) {
    int count = 0;
    cap_t cap_info = cap_get_proc();
    cap_flag_value_t is_set;
    char *txt;

    fputs(prefix, stdout);

    for (cap_value_t cap_val = 0; cap_val <= CAP_LAST_CAP; cap_val++) {
        if (cap_get_flag(cap_info, cap_val, which, &is_set) == 0
            && is_set == CAP_SET) {
            txt = cap_to_name(cap_val);
            fputs(txt, stdout);
            count++;
            if (count == 6) {
                fputc('\n', stdout);
                count = 0;
            } else {
                fprintf(stdout, ", ");
            }
            cap_free(txt);
        }
    }

    fprintf(stdout, "\n\n");
    fflush(stdout);

    cap_free(cap_info);
}

static int is_in_array(cap_value_t to_test, const cap_value_t *to_keep,
                       size_t nb_capa) {
    for (size_t i = 0; i < nb_capa; i++) {
        if (to_test == to_keep[i]) {
            return 1;
        }
    }
    return 0;
}