#include <stdlib.h>

#include "my_fnmatch.h"
#include "my_fnmatch_bracket.h"

int star(const char *pat, const char *str, int i_p, int i_s)
{
    if (pat[i_p + 1] == '\0')
        return 1;
    for (int i = i_s; str[i] != '\0'; ++i)
        if (matcher(pat, str, i_p + 1, i))
            return 1;
    return 0;
}

// Return 1 in case of match
int matcher(const char *pat, const char *str, int ip, int is)
{
    // size_t consumed = 0;
    while (pat[ip] != '\0' || str[is] != '\0')
    {
        // if the last char of the pattern is not '*'
        // and str is empty, return false
        if (str[is] == '\0' && pat[ip] != '*')
            return 0;
        switch (pat[ip])
        {
        case '?':
            is++;
            break;
        case '*':
            return star(pat, str, ip, is);
        case '[':
            if (bracket_match(pat, str, &ip, &is))
                return matcher(pat, str, ip + 1, is + 1);
            return 0;
        case '\\':
            if (pat[++ip] != str[is++])
                return 0;
            break;
        default:
            if (pat[ip] != str[is])
                return 0;
            is++;
            break;
        }
        ip++;
    }
    return pat[ip] == '\0' && str[is] == '\0';
}

int my_fnmatch(const char *pat, const char *str)
{
    // String iterator
    int i_s = 0;
    // Pattern iterator
    int i_p = 0;
    return !matcher(pat, str, i_p, i_s);
}
