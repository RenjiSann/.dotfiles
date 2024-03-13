#include "my_fnmatch_bracket.h"

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