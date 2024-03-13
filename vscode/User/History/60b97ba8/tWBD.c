#include <criterion/criterion.h>
#include <fnmatch.h>

#include "my_fnmatch.h"

#define FAIL 1
#define SUCCESS 0

Test(basics, criterion_works)
{
    cr_assert_eq(1, 1);
}

Test(basics, first)
{
    cr_assert_eq(my_fnmatch("", ""), fnmatch("", "", SUCCESS));
}

Test(basics, empty_pattern)
{
    cr_assert_eq(my_fnmatch("", "  "), FAIL);
}

Test(basics, interogation_mark_simple)
{
    cr_assert_eq(my_fnmatch("?", "2"), SUCCESS);
}

Test(basics, interogation_mark_simple_2)
{
    cr_assert_eq(my_fnmatch("?", "!2"), FAIL);
}

Test(basics, interogation_mark_plus_letters)
{
    cr_assert_eq(my_fnmatch("ab?d", "abcd"), SUCCESS);
}

Test(basics, interogation_mark_several)
{
    cr_assert_eq(my_fnmatch("a??d", "abcd"), SUCCESS);
}

Test(basics, interogation_mark_several_fail)
{
    cr_assert_eq(my_fnmatch("a??d", "abc?"), FAIL);
}

Test(basics, star_empty)
{
    cr_assert_eq(my_fnmatch("*", ""), SUCCESS);
}

Test(basics, star_simple)
{
    cr_assert_eq(my_fnmatch("*", "a"), SUCCESS);
}

Test(basics, star_simple_2)
{
    cr_assert_eq(my_fnmatch("a*", "a"), SUCCESS);
}

Test(basics, star_simple_3)
{
    cr_assert_eq(my_fnmatch("a*a", "a"), FAIL);
}

Test(basics, star_interogation)
{
    cr_assert_eq(my_fnmatch("a*?", "acb"), SUCCESS);
}

Test(basics, star_harder)
{
    cr_assert_eq(my_fnmatch("*abc", "cxabcabc"), SUCCESS);
}

Test(basics, tony_1)
{
    cr_assert_eq(my_fnmatch("cou*il*les??", "could ill Phil bless?"), SUCCESS);
}

Test(basics, tony_2)
{
    cr_assert_eq(my_fnmatch("cou*il*les??$", "could ill Phil bless?"), FAIL);
}

Test(basics, lots_of_stars)
{
    cr_assert_eq(my_fnmatch("*********b*?*", "jkdfhvcghlsghsxfbkjcbhbsfcufxuijf"), SUCCESS);
}

Test(basics, lots_of_stars_fail)
{
    cr_assert_eq(my_fnmatch("*b??*", "ghlsghsxfkjcbh"), FAIL);
}

Test(basics, negate_1)
{
    cr_assert_eq(my_fnmatch("a\\*", "a"), FAIL);
}

Test(basics, negate_2)
{
    cr_assert_eq(my_fnmatch("a\\*", "a*"), SUCCESS);
}

Test(basics, negate_3)
{
    cr_assert_eq(my_fnmatch("a\\\\", "a\\"), SUCCESS);
}

Test(basics, negate_4)
{
    cr_assert_eq(my_fnmatch("a\\t", "a\\t"), FAIL);
}

Test(basics, negate_5)
{
    cr_assert_eq(my_fnmatch("a\\t", "at"), SUCCESS);
}

Test(basics, negate_6)
{
    cr_assert_eq(my_fnmatch("a\\\\t", "a\\t"), SUCCESS);
}

Test(basics, brackets)
{
    cr_assert_eq(my_fnmatch("[a]", "a"), SUCCESS);
}

Test(basics, brackets_negated)
{
    cr_assert_eq(my_fnmatch("[!a]", "a"), FAIL);
    cr_assert_eq(my_fnmatch("[!a]", "b"), SUCCESS);
}

Test(basics, tony_3)
{
    cr_assert_eq(my_fnmatch("T\\[[]][]N]Y", "T[]NY"), SUCCESS);
}

Test(basics, tony_4)
{
    cr_assert_eq(my_fnmatch("T\\[[]][]N]Y$", "T[]NY"), FAIL);
}

// Test(basics, range_simple)
// {
//     cr_assert_eq(my_fnmatch("[a-z]", "j"), SUCCESS);
// }

// Test(basics, range_negated)
// {
//     char *pat = "[!a-z]";
//     cr_assert_eq(my_fnmatch(pat, "j"), FAIL);
//     cr_assert_eq(my_fnmatch(pat, "J"), SUCCESS);
// }

// Test(basics, range_multiple)
// {
//     char *pat = "[!0-9a-z]";
//     cr_assert_eq(my_fnmatch(pat, "9"), FAIL);
//     cr_assert_eq(my_fnmatch(pat, ":"), SUCCESS);
// }

// Test(basics, range_special_chars)
// {
//     char *pat = "[!-z]";
//     cr_assert_eq(my_fnmatch(pat, "-"), FAIL);
//     cr_assert_eq(my_fnmatch(pat, "z"), FAIL);
//     cr_assert_eq(my_fnmatch(pat, "9"), SUCCESS);
//     cr_assert_eq(my_fnmatch(pat, ":"), SUCCESS);
// }

// Test(basics, tony_hard)
// {
//     char *pat = "I'm on [A-z] of the w[!--np-~]*d";
//     cr_assert_eq(my_fnmatch(pat, "I'm on ^ of the world"), SUCCESS);
//     cr_assert_eq(my_fnmatch(pat, "I'm on ^ of the wyrd"), FAIL);
// }

Test(basics, tony_hard_2)
{
    char *pat = "T\\[[]][NOPE][YES]";
    cr_assert_eq(my_fnmatch(pat, "T[]NY"), SUCCESS);
    cr_assert_eq(my_fnmatch(pat, "T["), FAIL);
}
