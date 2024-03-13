#include <stdlib.h>

#include "my_fnmatch.h"
#include "my_fnmatch_bracket.h"

#define NEG(N, P) ((N) ? !(P) : (P))

// Fill the histogram with all the values between beg and end
void bracket_range(char hist[256], char beg, char end)
{
    if (end < beg)
        return;
    for (char i = beg; i <= end; ++i)
    {
        int index = i;
        hist[index] = 1;
    }
}

int bracket_match(const char *pat, const char *str, int *ip, int *is)
{
    // First char must be a bracket
    int i = (*ip) + 1;
    int negator = (pat[i] == '!');
    if (negator)
        i++;
    
    // the first char of the match
    int strt = i;

    // Stock whether a char is valid or not
    char hist[256] = { 0 };

    // Case when ']' is the next element
    if (pat[i] == ']')
    {
        int c = ']';
        hist[c] = 1;
        ++i;
    }

    while (pat[i] != ']')
    {
        // If the char is '-' and is not at the beginning nor the end
        if ( pat[i] == '-' && i - 1 >= strt && pat[i + 1] != ']')
        {
            bracket_range(hist, pat[i - 1], pat[i + 1]);
            i += 2;
        }
        else
        {
            char x = pat[i];
            int xx = x;
            hist[xx] = 1; 
            ++i;
        }
    }

    int letter = str[*is];
    // Increment the indexes
    // i is now pointing to the char ']'
    *ip = i;
    return NEG(negator, hist[letter]);
}

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
