"""Test functions used for validating word-level LD function."""

import pytest

from salwer.levenshtein import levenshtein_gld
from .levenshtein_word_validation import (
    random_size_of_cue, random_cue,
    add_errors, verify_s_t_e,
    attribute_wl_gld,
)
from .helpers import wlst_approx_eq


def test_validate_wrd_ld_fun_():
    """Calculate word-level WER between ref and hyp transcripts.

    Arguments:
    -   num_examples: int = 1000. The number of simulation examples.
    """

    num_examples = 1000
    good_cases = []
    bad_cases = []
    for i in range(num_examples):
        s = random_cue(random_size_of_cue())
        s, t, e, _ = add_errors(s)
        ss = [ele for ele in s if ele != " "]
        tt = [ele for ele in t if ele != " "]
        if not verify_s_t_e(s, t, e):
            continue
        print(f"{i = }")
        print(f"{ss = }")
        print(f"{tt = }")
        direct_cal = attribute_wl_gld(s, e)
        wrd_ld_cal = levenshtein_gld(ss, tt, err_limit=100)

        if wlst_approx_eq(direct_cal, wrd_ld_cal):
            good_cases.append(direct_cal)
        else:
            bad_cases.append([direct_cal, wrd_ld_cal, s, t, e, ss, tt])

    print(f"Number of good cases: {len(good_cases)}")
    print(f"Number of bad cases: {len(bad_cases)}")

    for case in bad_cases:
        print(f"direct_cal = {case[0]}")
        print(f"wrd_ld_cal = {case[1]}")
        print(f"s  = {case[2]}")
        print(f"t  = {case[3]}")
        print(f"e  = {case[4]}")
        print(f"ss = {case[5]}")
        print(f"tt = {case[6]}\n")

    print(f"Skipped cases: {num_examples - len(good_cases) - len(bad_cases)}")
    print(f"Number of good cases: {len(good_cases)}")
    print(f"Number of bad cases: {len(bad_cases)}")
