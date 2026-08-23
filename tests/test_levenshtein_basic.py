"""Test functions for BASIC Levenshtein distance calculations."""

import pytest

from salwer.levenshtein import (
    levenshtein_2d,
    levenshtein,
    levenshtein_1d,
    _check_st_tails,
    _clip_wlst_err,
    _max_ind_of_min,
    _num_prefix_drift,
    _num_suffix_drift,
    _prefix_drift_rh,
    _prefix_drift_sub_rh,
    _update_d1,
)
from .helpers import assert_word_list_eq

#--------------------------------------------------------------------
# Test Levenshtein distance with empty lists
#--------------------------------------------------------------------

def test_levenshtein_with_two_empty_lists():
    assert levenshtein_2d([], []) == 0
    assert levenshtein_1d([], []) == 0
    assert levenshtein([], []) == 0


def test_levenshtein_with_single_empty_list():
    s = "J K L".split()
    t = "     ".split()
    #    ^ ^ ^
    assert levenshtein_2d(s, t) == 3
    assert levenshtein_2d(t, s) == 3
    assert levenshtein_1d(s, t) == 3
    assert levenshtein_1d(t, s) == 3
    assert levenshtein(s, t) == 3
    assert levenshtein(t, s) == 3


#--------------------------------------------------------------------
# Test Levenshtein distance with identical lists
#--------------------------------------------------------------------

def test_levenshtein_with_identical_lists_case1():
    s = "J K L".split()
    t = "J K L".split()
    assert levenshtein_2d(s, t) == 0
    assert levenshtein_1d(s, t) == 0
    assert levenshtein(s, t) == 0


def test_levenshtein_with_identical_lists_case2():
    s = "J".split()
    t = "J".split()
    assert levenshtein_2d(s, t) == 0
    assert levenshtein_1d(s, t) == 0
    assert levenshtein(s, t) == 0


#--------------------------------------------------------------------
# Test Levenshtein distance with single partial difference
#--------------------------------------------------------------------

def test_levenshtein_with_single_substitute():
    s = "J K L".split()
    t = "J M L".split()
    #      ^
    assert levenshtein_2d(s, t) == 1
    assert levenshtein_2d(t, s) == 1
    assert levenshtein_1d(s, t) == 1
    assert levenshtein_1d(t, s) == 1
    assert levenshtein(s, t) == 1
    assert levenshtein(t, s) == 1


def test_levenshtein_with_single_deletion():
    s = "J K L".split()
    t = "J   L".split()
    #      ^
    assert levenshtein_2d(s, t) == 1
    assert levenshtein_1d(s, t) == 1
    assert levenshtein(s, t) == 1


def test_levenshtein_with_single_insertion():
    s = "J   L".split()
    t = "J K L".split()
    #      ^
    assert levenshtein_2d(s, t) == 1
    assert levenshtein_1d(s, t) == 1
    assert levenshtein(s, t) == 1


#--------------------------------------------------------------------
# Test Levenshtein distance with two partial differences
#--------------------------------------------------------------------

def test_levenshtein_wiht_two_substitutes():
    s = "J K L M".split()
    t = "J M L N".split()
    #      ^   ^
    assert levenshtein_2d(s, t) == 2
    assert levenshtein_2d(t, s) == 2
    assert levenshtein_1d(s, t) == 2
    assert levenshtein_1d(t, s) == 2
    assert levenshtein(s, t) == 2
    assert levenshtein(t, s) == 2


def test_levenshtein_with_two_deletions():
    s = "J K L M".split()
    t = "J     M".split()
    #      ^ ^
    assert levenshtein_2d(s, t) == 2
    assert levenshtein_1d(s, t) == 2
    assert levenshtein(s, t) == 2


def test_levenshtein_with_two_insertions():
    s = "J     M".split()
    t = "J K L M".split()
    #      ^ ^
    assert levenshtein_2d(s, t) == 2
    assert levenshtein_1d(s, t) == 2
    assert levenshtein(s, t) == 2


#--------------------------------------------------------------------
# Test Levenshtein distance without common elements
#--------------------------------------------------------------------

def test_levenshtein_with_no_common_elements():
    s = "J M".split()
    t = "K L".split()
    #    ^ ^
    assert levenshtein_2d(s, t) == 2
    assert levenshtein_2d(t, s) == 2
    assert levenshtein_1d(s, t) == 2
    assert levenshtein_1d(t, s) == 2
    assert levenshtein(s, t) == 2
    assert levenshtein(t, s) == 2


#--------------------------------------------------------------------
# Test Levenshtein distance with mixed differences
#--------------------------------------------------------------------

def test_levenshtein_with_single_sub_del_ins():
    s = "J K L M N O   Q".split()
    t = "J R L M   O P Q".split()
    #      ^     ^   ^
    #      S     D   I
    assert levenshtein_2d(s, t) == 3
    assert levenshtein_1d(s, t) == 3
    assert levenshtein(s, t) == 3


#--------------------------------------------------------------------
# Test the helper functions used for levenshtein_word.
#--------------------------------------------------------------------

# def test_num_suffix_drift_sub():
#     r0 = "B C D".split()
#     h0 = "A C D".split()
#     assert _num_suffix_drift_sub(r0, h0) == (0, 0)
#     assert r0 == "B C D".split()   # No change to the sequence
#     r1 = "B C D".split()
#     h1 = "B C D E".split()
#     assert _num_suffix_drift_sub(r1, h1) == (1, 0)
#     r2 = "B C D F".split()
#     h2 = "B C D E".split()
#     assert _num_suffix_drift_sub(r2, h2) == (0, 0)
#     r3 = "B      ".split()
#     h3 = "B Y Z A ".split()
#     assert _num_suffix_drift_sub(r3, h3) == (3, 0)
#     r5 = "C D E".split()
#     h5 = "C D  ".split()
#     assert _num_suffix_drift_sub(r5, h5) == (0, 0)
#     r7 = "B C    ".split()
#     h7 = "B Y Z A ".split()
#     assert _num_suffix_drift_sub(r7, h7) == (2, 1)
#     r9 = "D C    ".split()
#     h9 = "B Y Z A ".split()
#     assert _num_suffix_drift_sub(r9, h9) == (2, 2)

    # s = "J K L M N O   Q".split()
    # t = "J R L M   O P Q".split()

def test_check_st_tails_case1():
    s = "M N O K".split()
    t = "J L K".split()
    o_s, o_t, o_fwlst, o_pwlst, o_ld = _check_st_tails(s, t)
    assert o_s == s
    assert o_t == t
    assert o_ld == pytest.approx(0.0)
    assert o_fwlst == []
    assert o_pwlst == []


def test_check_st_tails_case2():
    s = "M N O".split()
    t = "J R L".split()
    o_s, o_t, o_fwlst, o_pwlst, o_ld = _check_st_tails(s, t)
    assert o_s == s
    assert o_t == t
    assert o_ld == pytest.approx(0.0)
    assert o_pwlst == []
    assert_word_list_eq(o_fwlst, [["M", 1.0], ["N", 1.0], ["O", 1.0]])


def test_check_st_tails_case3b():
    s = "K".split()
    t = "K J R L".split()
    o_s, o_t, o_fwlst, o_pwlst, o_ld = _check_st_tails(s, t)
    assert o_s == s[:1]
    assert o_t == t[:1]
    assert o_ld == pytest.approx(3.0)
    assert o_fwlst == []
    assert o_pwlst == []


def test_check_st_tails_case3c():
    s = "K M N O".split()
    t = "K J R L Q".split()
    o_s, o_t, o_fwlst, o_pwlst, o_ld = _check_st_tails(s, t)
    assert o_s == s[:1]
    assert o_t == t[:1]
    assert o_ld == pytest.approx(0.5)
    assert o_fwlst == []
    a_ld = 3.5 / 3
    assert_word_list_eq(o_pwlst, [["M", a_ld], ["N", a_ld], ["O", a_ld]])


def test_check_st_tails_case4b():
    s = "K J R L".split()
    t = "K".split()
    o_s, o_t, o_fwlst, o_pwlst, o_ld = _check_st_tails(s, t)
    assert o_s == s[:1]
    assert o_t == t[:1]
    assert o_ld == pytest.approx(0.0)
    assert o_fwlst == []
    assert_word_list_eq(o_pwlst, [["J", 1.0], ["R", 1.0], ["L", 1.0]])


def test_check_st_tails_case4c():
    s = "K M N O".split()
    t = "K J R".split()
    o_s, o_t, o_fwlst, o_pwlst, o_ld = _check_st_tails(s, t)
    assert o_s == s[:1]
    assert o_t == t[:1]
    assert o_ld == pytest.approx(0.0)
    assert o_fwlst == []
    assert_word_list_eq(o_pwlst, [["M", 1.0], ["N", 1.0], ["O", 1.0]])


def test_check_st_tails_case5b():
    s = "K M N O".split()
    t = "K J R L".split()
    o_s, o_t, o_fwlst, o_pwlst, o_ld = _check_st_tails(s, t)
    assert o_s == s[:1]
    assert o_t == t[:1]
    assert o_ld == pytest.approx(0.0)
    assert o_fwlst == []
    assert_word_list_eq(o_pwlst, [["M", 1.0], ["N", 1.0], ["O", 1.0]])





def test_clip_wlst_err():
    wlst = [['A', 2], ['B', 4], ['A', 8], ['B', 6]]
    assert _clip_wlst_err(wlst, 5) == \
        [['A', 2], ['B', 4], ['A', 5], ['B', 5]]


def test_max_ind_of_min():
    d0 = [1]
    #     ^
    assert _max_ind_of_min(d0) == 0
    d1 = [1, 1]
    #        ^
    assert _max_ind_of_min(d1) == 1
    d2 = [1, 0, 0, 1, 2, 3, 4, 5]
    #           ^
    assert _max_ind_of_min(d2) == 2
    d3 = [3, 2, 1, 1, 2, 3, 4]
    #              ^
    assert _max_ind_of_min(d3) == 3


def test_num_prefix_drift():
    r0 = "B C D".split()
    h0 = "A C D".split()
    assert _num_prefix_drift(r0, h0) == 0
    r1 = "  B C D".split()
    h1 = "A B C D".split()
    assert _num_prefix_drift(r1, h1) == 1
    r2 = "    B C D".split()
    h2 = "Z A B C D".split()
    assert _num_prefix_drift(r2, h2) == 2
    r3 = "      B".split()
    h3 = "Y Z A B".split()
    assert _num_prefix_drift(r3, h3) == 3

    r5 = "B C D".split()
    h5 = "  C D".split()
    assert _num_prefix_drift(r5, h5) == 0
    r6 = "B C".split()
    h6 = "  C".split()
    assert _num_prefix_drift(r6, h6) == 0
    r7 = "B".split()
    h7 = " ".split()
    assert _num_prefix_drift(r7, h7) == 0
    r8 = "B C D".split()
    h8 = "  C  ".split()
    assert _num_prefix_drift(r8, h8) == 0
    r9 = ['t']
    h9 = ['V']
    assert _num_prefix_drift(r9, h9) == 0


def test_num_suffix_drift():
    r0 = "B C D".split()
    h0 = "A C D".split()
    assert _num_suffix_drift(r0, h0) == 0
    assert r0 == "B C D".split()   # No change to the sequence
    r1 = "B C D".split()
    h1 = "B C D E".split()
    assert _num_suffix_drift(r1, h1) == 1
    r3 = "B      ".split()
    h3 = "B Y Z A ".split()
    assert _num_suffix_drift(r3, h3) == 3
    r5 = "C D E".split()
    h5 = "C D  ".split()
    assert _num_suffix_drift(r5, h5) == 0


#--------------------------------------------------------------------
# Idea behind the _num_prefix_drift function
#--------------------------------------------------------------------

def test_levenshtein_prefix_hallucination_removal():
    s = "        N O P Q R".split()
    t = "J K L M N   P Q R".split()
    assert levenshtein(s, t) == 5
    assert levenshtein(s, t[1:]) == 4
    assert levenshtein(s, t[2:]) == 3
    assert levenshtein(s, t[3:]) == 2
    assert levenshtein(s, t[4:]) == 1
    assert levenshtein(s, t[5:]) == 2




def test_prefix_drift_rh_and_sub_rh_1():
    s = "    R   N O P Q R".split()
    t = "J K L M N   P Q R".split()
    r = "R   N O P Q R".split()
    h = "M N   P Q R".split()
    m, n = len(s), len(t)   # sizes of s and t
    d0 = list(range(n+1))   # prev LD list
    d1 = [0] * (n+1)        # curr LD list
    min_d0 = 0      # v_plus, base_dist of the seg version
    # for i in range(m):
    i = 0
    d1 = _update_d1(s, t, d0, d1, i, n)
    min_d1 = min(d1)                # _v_plus_upper(d1)
    dist = min_d1 - min_d0          # LD of word
    assert dist == 1
    d0, d1, min_d0 = d1, d0, min_d1
    # Check if dist is caused by prefix drift.
    n_pd1, r1, h1 = _prefix_drift_rh(s, t, i, d1)  # d1 is actually d0
    n_pd2, n_sub, r2, h2 = _prefix_drift_sub_rh(s, t, i, d1)
    assert n_pd1 == 3
    assert n_pd2 == 3
    assert n_sub == 1
    assert r1 == s
    assert r2 == s
    assert h1 == t
    assert h2 == t