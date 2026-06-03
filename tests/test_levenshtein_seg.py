"""Test functions for edit distance calculations."""

import pytest

from salwer.levenshtein import (
    levenshtein_seg,
)
# from salwer.utils import (
#     _clean_transcript,
#     _cue_class,
#     _cue_seg_ranges,
# )
# from salwer.recipes.check_llm_class_n_seg_results import (
#     _check_class_seg_ann,
# )
from salwer.labels import Transcripts


# def test_rmin_1():
#     """Test seg_size_n_edit_distance with the above lists."""
#     d = [
#         [1, 1, 2, 2, 3, 4, 5, 6],
#         [2, 2, 2, 3, 2, 3, 4, 5],
#         [3, 3, 3, 3, 3, 2, 3, 4],
#         [4, 3, 4, 4, 4, 3, 2, 3]
#     ]
#     assert rmin(d[0]) == 2
#     assert rmin(d[1]) == 2
#     assert rmin(d[2]) == 2
#     assert rmin(d[3]) == 2


# def test_rmin_2():
#     """Test seg_size_n_edit_distance with the above lists."""
#     d = [
#         [1, 1, 2, 2, 3, 4, 5],
#         [2, 1, 2, 3, 2, 3, 4],
#         [3, 2, 2, 3, 3, 2, 3],
#         [4, 3, 2, 3, 4, 3, 2]
#     ]
#     assert rmin(d[0]) == 2
#     assert rmin(d[1]) == 2
#     assert rmin(d[2]) == 2
#     assert rmin(d[3]) == 2



##################################################################
#
#         ""      cat     sat     on      mat  |  in      the     room
# ""      0       1       2       3       4    |  5       6       7
# cat     1       0       1       2       3    |  4       5       6
# sat     2       1       0       1       2    |  3       4       5
# on      3       2       1       0       1    |  2       3       4
# the     4       3       2       1       1    |  2       2       3
# mat     5       4       3       2      (1)   |  2       3       3
# -----------------------------------------------------------------
# in      6       5       4       3       2    |  1       2       3
# a       7       6       5       4       3    |  2       2       3
# room    8       7       6       5       4    |  3       3       2

# s1 = "cat sat on the mat in a room".split()
# t1 = "cat sat on mat in the room".split()

# def test_levenshtein_n_seg_size_tail_1a():
#     """Test seg_size_n_edit_distance with the above lists."""
#     segs_a = [[0, 5], [5, 8]]
#     assert levenshtein_n_seg_size_tail(s1, t1, segs_a) == [[5, 1], [3, 1]]
#     assert levenshtein_n_seg_size(s1, t1, segs_a) == [[5, 1], [3, 1]]


# def test_levenshtein_n_seg_size_tail_1b():
#     """Test seg_size_n_edit_distance with the above lists."""
#     segs_b = [[0, 2], [2, 5], [5, 8]]
#     assert levenshtein_n_seg_size_tail(s1, t1, segs_b) == [[2, 0], [3, 1], [3, 1]]
#     assert levenshtein_n_seg_size(s1, t1, segs_b) == [[2, 0], [3, 1], [3, 1]]


# def test_levenshtein_n_seg_size_head_1a():
#     """Test seg_size_n_edit_distance with the above lists."""
#     segs_a = [[0, 5], [5, 8]]
#     assert levenshtein_n_seg_size_head(s1, t1, segs_a) == [[5, 1], [3, 1]]
#     assert levenshtein_n_seg_size(s1, t1, segs_a, head=True) == [[5, 1], [3, 1]]


# def test_levenshtein_n_seg_size_head_1b():
#     """Test seg_size_n_edit_distance with the above lists."""
#     segs_b = [[0, 2], [2, 5], [5, 8]]
#     assert levenshtein_n_seg_size_head(s1, t1, segs_b) == [[2, 0], [3, 1], [3, 1]]
#     assert levenshtein_n_seg_size(s1, t1, segs_b, head=True) == [[2, 0], [3, 1], [3, 1]]


# s = "A B A D E B G H I".split()
# t = "A B C D E F G H I".split()
#
# s\t j   A   B   C   D   E   F   G   H   I
# i   0+| 1   2   3 | 4   5   6 | 7   8   9
#    ---|-----------|-----------|-----------
# A   1 | 0-  1   2 | 3   4   5 | 6   7   8
# B   2 | 1   0   1 | 2   3   4 | 5   6   7
# A   3 | 2   1   1+| 2   3   4 | 5   6   7
#    ---|-----------|-----------|-----------
# D   4 | 3   2   2 | 1-  2   3 | 4   5   6
# E   5 | 4   3   3 | 2   1   2 | 3   4   5
# B   6 | 5   4   4 | 3   2   2+| 3   4   5
#    ---|-----------|-----------|-----------
# G   7 | 6   5   5 | 4   3   3 | 2-  3   4
# H   8 | 7   6   6 | 5   4   4 | 3   2   3
# I   9 | 8   7   7 | 6   5   5 | 4   3   2+

s0 = "A B A D E B G H I".split()
t0 = "A B C D E F G H I".split()

def test_levenshtein_seg_0a():
    """Test seg_size_n_edit_distance with the above lists."""
    segs = [[0, 3], [3, 6], [6, 9]]
    assert levenshtein_seg(s0, t0, segs) == [[3, 1], [3, 1], [3, 0]]

def test_levenshtein_seg_0b():
    """Test seg_size_n_edit_distance with the above lists."""
    segs = [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 9]]
    assert levenshtein_seg(s0, t0, segs) == \
        [[1, 0], [1, 0], [1, 1], [1, 0], [1, 0], [1, 1], [3, 0]]


def test_levenshtein_seg_head_0a():
    """Test seg_size_n_edit_distance with the above lists."""
    segs = [[0, 3], [3, 6], [6, 9]]
    assert levenshtein_seg(s0, t0, segs, head=True) == [[3, 1], [3, 1], [3, 0]]

def test_levenshtein_seg_head_0b():
    """Test seg_size_n_edit_distance with the above lists."""
    segs = [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 9]]
    assert levenshtein_seg(s0, t0, segs, head=True) == \
        [[1, 0], [1, 0], [1, 1], [1, 0], [1, 0], [1, 1], [3, 0]]

############################################
# s\t j   A   B   D   E   G   H   I
# i   0+| 1   2 | 3   4 | 5   6   7
#    -------------------------------
# A   1 | 0-  1 | 2   3 | 4   5   6
# B   2 | 1   0 | 1   2 | 3   4   5
# C   3 | 2   1+| 1   2 | 3   4   5
#    -------------------------------
# D   4 | 3   2 | 1-  2 | 3   4   5
# E   5 | 4   3 | 2   1 | 2   3   4
# F   6 | 5   4 | 3   2+| 2   3   4
#    -------------------------------
# G   7 | 6   5 | 4   3 | 2-  3   4
# H   8 | 7   6 | 5   4 | 3   2   3
# I   9 | 8   7 | 6   5 | 4   3   2+

s1 = "A B C D E F G H I".split()
t1 = "A B   D E   G H I".split()

def test_levenshtein_seg_1a():
    """Test seg_size_n_edit_distance with the above lists."""
    segs = [[0, 3], [3, 6], [6, 9]]
    assert levenshtein_seg(s1, t1, segs) == [[3, 1], [3, 1], [3, 0]]

def test_levenshtein_seg_1b():
    """Test seg_size_n_edit_distance with the above lists."""
    segs = [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 9]]
    assert levenshtein_seg(s1, t1, segs) == \
        [[1, 0], [1, 0], [1, 1], [1, 0], [1, 0], [1, 1], [3, 0]]


def test_levenshtein_seg_head_1a():
    """Test seg_size_n_edit_distance with the above lists."""
    segs = [[0, 3], [3, 6], [6, 9]]
    assert levenshtein_seg(s1, t1, segs, head=True) == [[3, 1], [3, 1], [3, 0]]

def test_levenshtein_seg_head_1b():
    """Test seg_size_n_edit_distance with the above lists."""
    segs = [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 9]]
    assert levenshtein_seg(s1, t1, segs, head=True) == \
        [[1, 0], [1, 0], [1, 1], [1, 0], [1, 0], [1, 1], [3, 0]]

##############################################################################
#                                           i = 0   1   2   3   4   5   6   7
# s\t j   A   B   C   D   E   F   G   H   I
# i   0+| 1   2 | 3 | 4   5 | 6 | 7   8   9     d0
#    ---|-------|---|-------|---|-----------
# A   1 | 0-  1 | 2 | 3   4 | 5 | 6   7   8     d1  d0
# B   2 | 1   0+| 1*| 2   3 | 4 | 5   6   7         d1  d0
#    ---|-------|---|-------|---|-----------            d1
# D   3 | 2   1 | 1 | 1-  2 | 3 | 4   5   6
# E   4 | 3   2 | 2 | 2   1+| 2*| 3   4   5
#    ---|-------|---|-------|---|-----------
# G   5 | 4   3 | 3 | 3   2 | 2 | 2-  3   4
# H   6 | 5   4 | 4 | 4   3 | 3 | 3   2   3
# I   7 | 6   5 | 5 | 5   4 | 4 | 4   3   2+

s2 = "A B   D E   G H I".split()
t2 = "A B C D E F G H I".split()
#         ^     ^

def test_levenshtein_seg_2a():
    """Test seg_size_n_edit_distance with the above lists."""
    segs = [[0, 2], [2, 4], [4, 7]]
    assert levenshtein_seg(s2, t2, segs) == [[2, 0], [2, 0], [3, 0]]

def test_levenshtein_seg_2b():
    """Test seg_size_n_edit_distance with the above lists."""
    segs = [[0, 1], [1, 2], [2, 3], [3, 4], [4, 7]]
    assert levenshtein_seg(s2, t2, segs) == \
        [[1, 0], [1, 0], [1, 0], [1, 0], [3, 0]]


def test_levenshtein_seg_head_2a():
    """Test seg_size_n_edit_distance with the above lists."""
    segs = [[0, 2], [2, 4], [4, 7]]
    assert levenshtein_seg(s2, t2, segs, head=True) == [[2, 0], [2, 1], [3, 1]]

def test_levenshtein_seg_head_2b():
    """Test seg_size_n_edit_distance with the above lists."""
    segs = [[0, 1], [1, 2], [2, 3], [3, 4], [4, 7]]
    assert levenshtein_seg(s2, t2, segs, head=True) == \
        [[1, 0], [1, 0], [1, 1], [1, 0], [3, 1]]


# s\t j   A   B   C   D   E   F   G   H   I
# i   0   1   2   3   4   5   6   7   8   9
# B   1   1   1   2   3   4   5   6   7   8
# C   2   2   2   1   2   3   4   5   6   7
# D   3   3   3   2   1   2   3   4   5   6
# E   4   4   4   3   2   1   2   3   4   5
# G   5   5   5   4   3   2   2   2   3   4
# H   6   6   6   5   4   3   3   3   2   3
# I   7   7   7   6   5   4   4   4   3   2

s3 = "  B C D E   G H I".split()
t3 = "A B C D E F G H I".split()

def test_levenshtein_seg_3b():
    """Test seg_size_n_edit_distance with the above lists."""
    segs = [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 7]]
    assert levenshtein_seg(s3, t3, segs) == \
        [[1, 0], [1, 0], [1, 0], [1, 0], [1, 0], [2, 0]]


def test_levenshtein_seg_head_3b():
    """Test seg_size_n_edit_distance with the above lists."""
    segs = [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 7]]
    assert levenshtein_seg(s3, t3, segs, head=True) == \
        [[1, 1], [1, 0], [1, 0], [1, 0], [1, 1], [2, 0]]


##############################################################################
#                                           i = 0   1   2   3   4   5   6   7
# s\t j   A   B   C   D   E   F   G   H   I
# i   0+| 1   2*| 3   4   5 | 6   7 | 8   9     d0
#    ---------------------------------------
# C   1 | 1-  2 | 2-  3   4 | 5   6 | 7   8     d1
# D   2 | 2   2 | 3   2   3 | 4   5 | 6   7
# E   3 | 3   3 | 3   3   2+| 3   4*| 5   6
#    ---------------------------------------
# H   4 | 4   4 | 4   4   3 | 3-  4 | 4-  5
# I   5 | 5   5 | 5   5   4 | 4   4 | 5   4+

s4 = "    C D E     H I".split()
t4 = "A B C D E F G H I".split()

def test_levenshtein_seg_4a():
    """Test seg_size_n_edit_distance with the above lists."""
    segs = [[0, 3], [3, 5]]
    assert levenshtein_seg(s4, t4, segs) == \
        [[3, 2], [2, 2]]   # tight WER fails due to shifted min d1


def test_levenshtein_seg_4b():
    """Test seg_size_n_edit_distance with the above lists."""
    segs = [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5]]
    # print(f"{levenshtein_n_seg_size(s4, t4, segs) = }")
    # tight WER fails due to shifted min d1
    assert levenshtein_seg(s4, t4, segs) == \
        [[1, 1], [1, 0], [1, 0], [1, 1], [1, 0]]


def test_levenshtein_seg_head_4a():
    """Test seg_size_n_edit_distance with the above lists."""
    segs = [[0, 3], [3, 5]]
    assert levenshtein_seg(s4, t4, segs, head=True) == \
        [[3, 2], [2, 2]]


def test_levenshtein_seg_head_4b():
    """Test seg_size_n_edit_distance with the above lists."""
    segs = [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5]]
    # print(f"{levenshtein_n_seg_size(s4, t4, segs, head=True) = }")
    # WER propergates due to shifted min d1
    assert levenshtein_seg(s4, t4, segs, head=True) == \
        [[1, 1], [1, 1], [1, 0], [1, 1], [1, 1]]


# s\t j   C   D   E   H   I
# i   0   1   2   3   4   5
# A   1   1   2   3   4   5
# B   2   2   2   3   4   5
# C   3   2   3   3   4   5
# D   4   3   2   3   4   5
# E   5   4   3   2   3   4
#    -----------------------
# F   6   5   4   3   3   4
# G   7   6   5   4   4   4
# H   8   7   6   5   4   5
# I   9   8   7   6   5   4

s5 = "A B C D E F G H I".split()
t5 = "    C D E     H I".split()

def test_levenshtein_seg_5a():
    """Test seg_size_n_edit_distance with the above lists."""
    segs = [[0, 5], [5, 9]]
    assert levenshtein_seg(s5, t5, segs) == \
        [[5, 2], [4, 2]]


def test_levenshtein_seg_5b():
    """Test seg_size_n_edit_distance with the above lists."""
    segs = [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 9]]
    assert levenshtein_seg(s5, t5, segs) == \
        [[1, 1], [1, 1], [1, 0], [1, 0], [1, 0], [4, 2]]


def test_levenshtein_seg_head_5a():
    """Test seg_size_n_edit_distance with the above lists."""
    segs = [[0, 5], [5, 9]]
    assert levenshtein_seg(s5, t5, segs, head=True) == \
        [[5, 2], [4, 2]]


def test_levenshtein_seg_head_5b():
    """Test seg_size_n_edit_distance with the above lists."""
    segs = [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 9]]
    assert levenshtein_seg(s5, t5, segs, head=True) == \
        [[1, 1], [1, 1], [1, 0], [1, 0], [1, 0], [4, 2]]


# s\t j   B   C   D   E   F   G   H   I
# i   0   1   2   3   4   5   6   7   8
# A   1   1   2   3   4   5   6   7   8
# C   2   2   1   2   3   4   5   6   7
# D   3   3   2   1   2   3   4   5   6
# E   4   4   3   2   1   2   3   4   5
# G   5   5   4   3   2   2   2   3   4
# H   6   6   5   4   3   3   3   2   3
# I   7   7   6   5   4   4   4   3   2

# s = "A C D E   G H I".split()
# t = "B C D E F G H I".split()
#####################################################
#
# s \ t ""    the   cat   laid  on    the   dry   mat
# ""    0     1     2  |  3  |  4     5  |  6  |  7
# the   1     0     1  |  2  |  3     4  |  5  |  6
# fat   2     1     1  |  2  |  3     4  |  5  |  6
# cat   3     2    (1) |  2  |  3     4  |  5  |  6
#       ---------------------|-----------|-----|---
# sat   4     3     2  | (2) |  3     4  |  5  |  6
#       ---------------------------------|-----|---
# on    5     4     3  |  3  |  2     3  |  4  |  5
# the   6     5     4  |  4  |  3    (2) | [3] |  4
#       ---------------------------------|-----|---
# mat   7     6     5  |  5  |  4     3  |  3  | (3)

# s3 = "the fat cat sat  on the     mat".split()
# t3 = "the     cat laid on the dry mat".split()
# #         del     sub         ins

# def test_levenshtein_n_seg_size_tail_3a():
#     """Test seg_size_n_edit_distance with the above lists."""
#     segs_a = [[0, 4], [4, 7]]
#     assert levenshtein_n_seg_size_tail(s3, t3, segs_a) \
#         == [[4, 2],[3, 1]]
#     assert levenshtein_n_seg_size(s3, t3, segs_a) \
#         == [[4, 2],[3, 1]]

# def test_levenshtein_n_seg_size_tail_3b():
#     """Test seg_size_n_edit_distance with the above lists."""
#     segs_a = [[0, 3], [3, 4], [4, 6], [6, 7]]
#     assert levenshtein_n_seg_size_tail(s3, t3, segs_a) \
#         == [[3, 1], [1, 1], [2, 0], [1, 0]]
#     assert levenshtein_n_seg_size(s3, t3, segs_a) \
#         == [[3, 1], [1, 1], [2, 0], [1, 0]]


# def test_levenshtein_n_seg_size_head_3c():
#     """Test seg_size_n_edit_distance with the above lists."""
#     segs_a = [[0, 3], [3, 4], [4, 6], [6, 7]]
#     assert levenshtein_n_seg_size_head(s3, t3, segs_a) \
#         == [[3, 1], [1, 1], [2, 0], [1, 1]]
#     assert levenshtein_n_seg_size(s3, t3, segs_a, head=True) \
#         == [[3, 1], [1, 1], [2, 0], [1, 1]]

# def test_levenshtein_n_seg_size_tail_1b():
#     """Test seg_size_n_edit_distance with the above lists."""
#     segs_b = [[0, 2], [2, 5], [5, 8]]
#     assert levenshtein_n_seg_size_tail(s1, t1, segs_b) == [[2, 0], [3, 1], [3, 1]]


# def test_levenshtein_n_seg_size_head_1a():
#     """Test seg_size_n_edit_distance with the above lists."""
#     segs_a = [[0, 5], [5, 8]]
#     assert levenshtein_n_seg_size_head(s1, t1, segs_a) == [[5, 1], [3, 1]]


# def test_levenshtein_n_seg_size_head_1b():
#     """Test seg_size_n_edit_distance with the above lists."""
#     segs_b = [[0, 2], [2, 5], [5, 8]]
#     assert levenshtein_n_seg_size_head(s1, t1, segs_b) == [[2, 0], [3, 1], [3, 1]]

# s3 = "the fat cat sat  on the     mat".split()
# t3 = "the     cat laid on the dry mat".split()
#         del     sub         ins

#####################################################
#
# s \ t ""    the   cat   laid  on    the   dry   mat
# ""    0     1     2  |  3  |  4     5  |  6  |  7
# the   1     0     1  |  2  |  3     4  |  5  |  6
# fat   2     1     1  |  2  |  3     4  |  5  |  6
# cat   3     2    (1) |  2  |  3     4  |  5  |  6
#       ---------------------|-----------|-----|---
# sat   4     3     2  | (2) |  3     4  |  5  |  6
#       ---------------------------------|-----|---
# on    5     4     3  |  3  |  2     3  |  4  |  5
# the   6     5     4  |  4  |  3    (2) | [3] |  4
#       ---------------------------------|-----|---
# mat   7     6     5  |  5  |  4     3  |  3  | (3)



##############################################
#
# s \ t ""    the    desk  top   popped
# ""    0     1      2  |  3     4
# on    1     1      2  |  3     4
# the   2     1      2  |  3     4
# desk  3     2      1  |  2     3
#       --------------------------
# top   4     3      2  |  1     2

# s5 = "on the desk top".split()
# t5 = "   the desk top popped".split()
# print(f"{s5 = }, {t5 = }")

# The approach to obtain (1) is to find the right most min of the current line. Find its index. Then find the value of

# def test_levenshtein_n_seg_size_tail_5a():
#     """Test seg_size_n_edit_distance with the above lists."""
#     segs = [[0, 3], [3, 4]]
#     assert levenshtein_n_seg_size_tail(s5, t5, segs) \
#         == [[3, 1], [1, 0]]
#     assert levenshtein_n_seg_size(s5, t5, segs) \
#         == [[3, 1], [1, 0]]


# def test_levenshtein_n_seg_size_head_5b():
#     """Test seg_size_n_edit_distance with the above lists."""
#     segs = [[0, 3], [3, 4]]
#     assert levenshtein_n_seg_size_head(s5, t5, segs) \
#         == [[3, 1], [1, 0]]
#     assert levenshtein_n_seg_size(s5, t5, segs, head=True) \
#         == [[3, 1], [1, 0]]


# def test_levenshtein_n_seg_size_tail_5x():
#     """Test seg_size_n_edit_distance with the above lists."""
#     segs = [[0, 1], [1, 2], [2, 3], [3, 4]]
#     assert levenshtein_n_seg_size_tail(s5, t5, segs) \
#         == [[1, 1], [1, 0], [1, 0], [1, 0]]
#     assert levenshtein_n_seg_size(s5, t5, segs) \
#         == [[1, 1], [1, 0], [1, 0], [1, 0]]


# def test_levenshtein_n_seg_size_head_5y():
#     """Test seg_size_n_edit_distance with the above lists."""
#     segs = [[0, 1], [1, 2], [2, 3], [3, 4]]
#     assert levenshtein_n_seg_size_head(s5, t5, segs) \
#         == [[1, 1], [1, 0], [1, 0], [1, 0]]
#     assert levenshtein_n_seg_size(s5, t5, segs, head=True) \
#         == [[1, 1], [1, 0], [1, 0], [1, 0]]


s7 = "      on the desk top".split()
t7 = "a cat on the desk top hopped".split()

##############################################
#
# s \ t ""    a     cat   on    the   desk  top   hopped
# ""    0     1    (2)    3     4     5     6     7
# on    1     1     2    (2)    3     4     5     6
# the   2     2     2     3    (2)    3     4     5
# desk  3     3     3     3     3    (2)    3     4
# top   4     3     4     4     4     3    (2)    3

# The approach to obtain (1) is to find the right most min of the current line. Find its index. Then find the value of


def test_levenshtein_seg_7x():
    """Test seg_size_n_edit_distance with the above lists."""
    segs = [[0, 1], [1, 2], [2, 3], [3, 4]]
    assert levenshtein_seg(s7, t7, segs) \
        == [[1, 1], [1, 0], [1, 0], [1, 0]]


def test_levenshtein_seg_head_7y():
    """Test seg_size_n_edit_distance with the above lists."""
    segs = [[0, 1], [1, 2], [2, 3], [3, 4]]
    assert levenshtein_seg(s7, t7, segs, head=True) \
        == [[1, 1], [1, 1], [1, 0], [1, 0]]


# s7 = "        on the desk top".split()
# t7 = "the top on the desk top dropped".split()

##############################################
#
# s \ t ""    the    top   on    the    desk  top   dropped
# ""    0     1      2     3     4      5     6     7
# on    1     1      2     2     3      4     5     6
# the   2     1      2     3     2      3     4     5
# desk  3     2      2     3     3      2     3     4
# top   4     3      2     3     4      3     2     3

# The approach to obtain (1) is to find the right most min of the current line. Find its index. Then find the value of


# def test_levenshtein_n_seg_size_tail_7x():
#     """Test seg_size_n_edit_distance with the above lists."""
#     segs = [[0, 1], [1, 2], [2, 3], [3, 4]]
#     print(f"{levenshtein_n_seg_size_tail(s7, t7, segs) = }")
#     # assert levenshtein_n_seg_size_tail(s7, t7, segs) \
#     #     == [[1, 1], [1, 0], [1, 0], [1, 0]]


# def test_levenshtein_n_seg_size_head_7y():
#     """Test seg_size_n_edit_distance with the above lists."""
#     segs = [[0, 1], [1, 2], [2, 3], [3, 4]]
#     print(f"{levenshtein_n_seg_size_head(s7, t7, segs) = }")
#     # assert levenshtein_n_seg_size_head(s7, t7, segs) \
#     #     == [[1, 1], [1, 0], [1, 0], [1, 0]]


# Need to see what is wrong with the following for Seg B. It should be one, but we had two.

# tim: 2324180
# hyp: nineteen right heading two seven zero
# ref: all right turn right heading two seven zero
# seg: (1) [(D) All right] [(B4) turn right heading] [(C4) two seven zero]
# dst: 2


# def test_seg_size_n_edit_distance_1c():
#     """Test seg_size_n_edit_distance with the above lists."""
#     segs_c = [[5, 8]]
#     assert seg_size_n_edit_distance(segs_c, ref1, hyp1) == [[3, 1]]


# def test_seg_size_n_edit_distance_1d():
#     """Test seg_size_n_edit_distance with the above lists."""
#     segs_d = [[1, 2]]
#     assert seg_size_n_edit_distance(segs_d, ref1, hyp1) == [[1, 0]]


# def test_seg_size_n_edit_distance_1e():
#     """Test seg_size_n_edit_distance with the above lists."""
#     segs_e = [[0, 1]]
#     assert seg_size_n_edit_distance(segs_e, ref1, hyp1) == [[1, 0]]

# Each of the following needs to be separated into two tests, one without
# considering the insertion and the other with.


#         ""      a       cat     sat     on      mat  |  in      the     room
# ""      0       1       2       3       4       5    |  6       7       8
# cat     1       1       1       2       3       4    |  5       6       7
# sat     2       2       2       1       2       3    |  4       5       6
# at      3       3       3       2       2       3    |  4       5       6
# mat     4       4       4       3       3      (2)   |  3       4       5
# ---------------------------------------------------------------------------
# in      5       5       5       4       4       3    |  2       3       4
# a       6       5       6       5       5       4    |  3       3       4
# room    7       6       6       6       6       5    |  4       4       3

# ref2 = "cat sat at mat in a room".split()
# hyp2 = "a cat sat on mat in the room".split()

# def test_seg_size_n_edit_distance_2a():
#     """Test seg_size_n_edit_distance with the above lists."""
#     segs_a = [[0, 4], [4, 7]]
#     assert seg_size_n_edit_distance(segs_a, ref2, hyp2) == [[4, 2], [3, 1]]


# def test_seg_size_n_edit_distance_2b():
#     """Test seg_size_n_edit_distance with the above lists."""
#     segs_b = [[0, 2], [4, 7]]
#     assert seg_size_n_edit_distance(segs_b, ref2, hyp2) == [[2, 1], [3, 1]]


# ref3 = "Twenty one zero five expediting to niner thousand Seven Five Charlie Fox good day now".split()
# hyp3 = "Twenty one zero five expediting to niner thousand Seven Charlie Fox good day now".split()


# def test_seg_size_n_edit_distance_3a():
#     """Test seg_size_n_edit_distance with the above lists."""
#     segs = [[8, 12]]
#     assert seg_size_n_edit_distance(segs, ref3, hyp3) == [[4, 1]]


# def test_seg_size_n_edit_distance_3c():
#     """Test seg_size_n_edit_distance with the above lists."""
#     segs_c = [[0, 4], [6, 8]]
#     assert seg_size_n_edit_distance(segs_c, ref3, hyp3) == [[4, 0], [2, 0]]


# tim: 3471260
# hyp4 = "u s air two eleven turn your transponder on your squawk six five one five your radar contact six northwest at national".split()
# ref4 = "u s air two eleven turn your transponder on squawk six five one five youre radar contact six northwest of national".split()
# hyp4 = "u s air two eleven turn your transponder on your squawk six five one five your radar contact six northwest at national".split()
# ref4 = "u s air two eleven turn your transponder on squawk six five one five youre radar contact six northwest of national".split()
# # seg: (1) [(A) U S Air Two Eleven] [(E) turn your transponder on] [(B6) squawk] [(C6) six five one five] [(D) you're radar contact] [(E) six northwest of [(G) National]]
# # dst: 1


# def test_seg_size_n_edit_distance_4b():
#     """Test seg_size_n_edit_distance with the above lists."""
#     segs_b = [[9, 10]]
#     assert seg_size_n_edit_distance(segs_b, ref4, hyp4) == [[1, 0]]


## Issues with the followingg as well:

# tim: 4249860
# hyp: november two sierra five we turn left heading zero two zero
# ref: november two sierra bravo turn left heading zero two zero
# seg: (1) [(A) November Two Sierra Bravo] [(B4) turn left heading] [(C4) zero two zero]
# dst: 1

# The pattern is if the word ahead of the segment is wrong, it is counted to the segment. Need to fix.

# def test_cue_seg_ranges_1B6():
#     """Test _cue_seg_ranges with class 1 transcript and B6 segments."""
#     txt = "u s air two eleven turn your transponder on squawk six five one five youre radar contact six northwest of national"
#     seg = "(1) [(A) U S Air Two Eleven] [(E) turn your transponder on] [(B6) squawk] [(C6) six five one five] [(D) you're radar contact] [(E) six northwest of [(G) National]]"
#     seg_sel = "B"
#     assert _cue_seg_ranges(txt, seg, seg_sel) == [[9, 10]]


# Tests of functions in s_class_n_seg_wer.py


# def test_cue_class_1():
#     """Test _cue_class with class 1 string."""
#     cmt = "(1) [(A) U S Air Two Eleven] [(B4) turn left heading]"
#     assert _cue_class(cmt) == "1"


# def test_clean_transcript():
#     """Test _clean_transcript."""
#     txt = "Army Nine Three Six, traffic is V F R at er ten o'clock and two miles, he's er holding at the er outer marker."
#     cleaned = "army nine three six traffic is v f r at ten oclock and two miles hes holding at the outer marker"
#     assert _clean_transcript(txt) == cleaned


# def test_str_to_list():
#     """Verify that punctuations follow words while splitting string to list."""
#     txt = "U S Air Two Eleven, turn left, heading"
#     lst = ["U", "S", "Air", "Two", "Eleven,", "turn", "left,", "heading"]
#     assert txt.split() == lst
#     exp_low_cln = ["u", "s", "air", "two", "eleven", "turn", "left", "heading"]
#     lst_low_cln = [re.sub(r"[^\w]", "", word.lower()) for word in lst]
#     assert lst_low_cln == exp_low_cln


# def test_cue_seg_ranges_1A():
#     """Test _cue_seg_ranges with class 1 transcript and A segment."""
#     txt = "U S Air Two Eleven, turn left, heading"
#     seg = "(1) [(A) U S Air Two Eleven] [(B4) turn left heading]"
#     seg_sel = "A"
#     assert _cue_seg_ranges(txt, seg, seg_sel) == [[0, 5]]


# def test_cue_seg_ranges_1B23():
#     """Test _cue_seg_ranges with class 1 transcript and B segments (B2 & B3)."""
#     txt = "King Air Five Charlie Foxtrot, climb and maintain niner thousand, expedite your climb, contact Departure one two one point zero five."
#     seg = "(1) [(A) King Air Five Charlie Foxtrot] [(B2) climb and maintain] [(C2) niner thousand] [(E) expedite your climb] [(B3) contact] [(G) Departure] [(C3) one two one point zero five]"
#     seg_sel = "B"
#     assert _cue_seg_ranges(txt, seg, seg_sel) == [[5, 8], [13, 14]]


# def test_cue_seg_ranges_1B4():
#     """Test _cue_seg_ranges with class 1 transcript and B4 segment."""
#     txt = "U S Air Two Eleven, turn left, heading"
#     seg = "(1) [(A) U S Air Two Eleven] [(B4) turn left heading]"
#     seg_sel = "B"
#     assert _cue_seg_ranges(txt, seg, seg_sel) == [[5, 8]]


# tim: 3471260
# hyp: u s air two eleven turn your transponder on your squawk six five one five your radar contact six northwest at national
# ref: u s air two eleven turn your transponder on squawk six five one five youre radar contact six northwest of national
# seg: (1) [(A) U S Air Two Eleven] [(E) turn your transponder on] [(B6) squawk] [(C6) six five one five] [(D) you're radar contact] [(E) six northwest of [(G) National]]
# dst: 1


# def test_cue_seg_ranges_1B6():
#     """Test _cue_seg_ranges with class 1 transcript and B6 segments."""
#     txt = "u s air two eleven turn your transponder on squawk six five one five youre radar contact six northwest of national"
#     seg = "(1) [(A) U S Air Two Eleven] [(E) turn your transponder on] [(B6) squawk] [(C6) six five one five] [(D) you're radar contact] [(E) six northwest of [(G) National]]"
#     seg_sel = "B"
#     assert _cue_seg_ranges(txt, seg, seg_sel) == [[9, 10]]


# def test_cue_seg_ranges_1C23():
#     """Test _cue_seg_ranges with class 1 transcript and B segments (B2 & B3)."""
#     txt = "King Air Five Charlie Foxtrot, climb and maintain niner thousand, expedite your climb, contact Departure one two one point zero five."
#     seg = "(1) [(A) King Air Five Charlie Foxtrot] [(B2) climb and maintain] [(C2) niner thousand] [(E) expedite your climb] [(B3) contact] [(G) Departure] [(C3) one two one point zero five]"
#     seg_sel = "C"
#     assert _cue_seg_ranges(txt, seg, seg_sel) == [[8, 10], [15, 21]]


# def test_cue_seg_ranges_3Ea():
#     """Test _cue_seg_ranges with class 3 transcript and E segment."""
#     txt = "It is the GORDONSVILLE zero five six zero three six, direct GORDONSVILLE, and resume your own navigation."
#     seg = "(3) [(E) It is the [(H) GORDONSVILLE] zero five six zero three six] [(E) direct [(H) GORDONSVILLE]] [(E) and resume your own navigation]"
#     seg_sel = "E"
#     assert _cue_seg_ranges(txt, seg, seg_sel) == [[0, 3], [4, 10], [10, 11], [12, 17]]


# def test_cue_seg_ranges_3Eb():
#     """Test _cue_seg_ranges with class 3 transcript and E segment."""
#     txt = "American Three Fourteen, cross er Jetta at, at six thousand."
#     seg = "(3) [(A) American Three Fourteen] [(E) cross [(H) Jetta] at six thousand]"
#     seg_sel = "E"
#     assert _cue_seg_ranges(txt, seg, seg_sel) == [[3, 4], [7, 10]]


# def test_cue_seg_ranges_3Ec():
#     """Test _cue_seg_ranges with class 3 transcript and E segment."""
#     txt = "Army Nine Three Six, traffic is V F R at er ten o'clock and two miles, he's er holding at the er outer marker."
#     txt = _clean_transcript(txt)
#     seg = "(3) [(A) Army Nine Three Six] [(E) traffic is V F R at ten o'clock and two miles] [(E) he's holding at the outer marker]"
#     seg_sel = "E"
#     assert _cue_seg_ranges(txt, seg, seg_sel) == [[4, 15], [15, 21]]


# def test_cue_seg_ranges_3H2():
#     """Test _cue_seg_ranges with class 3 transcript and E segment."""
#     txt = "HAFNER, it'll be the GORDON zero, * GORDONSVILLE zero five six zero three six, direct GORDONSVILLE, and resume your own navigation."
#     txt = _clean_transcript(txt)
#     seg = "(3) [(H) HAFNER] [(E) it'll be the GORDON zero [(H) GORDONSVILLE] zero five six zero three six] [(E) direct [(H) GORDONSVILLE]] [(E) and resume your own navigation]"
#     seg_sel = "H"
#     assert _cue_seg_ranges(txt, seg, seg_sel) == [[0, 1], [6, 7], [14, 15]]


# def test_cue_seg_ranges_4E():
#     """Test _cue_seg_ranges with class 4 transcript and E segment with er."""
#     txt = "The second layer tops out about er seventy five, there's another layer we're entering now about er ten thousand."
#     txt = _clean_transcript(txt)
#     seg = "(4) [(E) The second layer tops out about seventy five] [(E) there's another layer we're entering now about ten thousand.]"
#     seg_sel = "E"
#     assert _cue_seg_ranges(txt, seg, seg_sel) == [[0, 8], [8, 17]]


cns_text = """
stm: 1>D1-2>N5CF
tim: 3502290
txt: King Air Five Charlie Foxtrot, climb and maintain niner thousand, expedite your climb, contact Departure one two one point zero five.
cns: (1) [(A) King Air Five Charlie Foxtrot] [(B2) climb and maintain] [(C2) niner thousand] [(E) expedite your climb] [(B3) contact] [(G) Departure] [(C3) one two one point zero five]

stm: 2>N5CF>D1-2
tim: 3509240
txt: Twenty one zero five, expediting to niner thousand, Seven Five Charlie Fox, good day now.
cns: (2) [(C3) Twenty one zero five] [(B2) expediting to] [(C2) niner thousand] [(A) Seven Five Charlie Fox] [(I) good day now]

stm: 1>D1-2>USA211
tim: 3536270
txt: U S Air Two Eleven, turn left, heading two three zero, expect on course in twelve miles.
cns: (1) [(A) U S Air Two Eleven] [(B4) turn left heading] [(C4) two three zero] [(E) expect on course in twelve miles]

stm: 1>USA211>D1-2
tim: 3541460
txt: Two thirty the heading, U S Air Two Eleven.
cns: (2) [(C4) Two thirty] [(J) the heading] [(A) U S Air Two Eleven]

stm: 1>D1-2>N5CF
tim: 3308200
txt: HAFNER, it'll be the GORDON zero, * GORDONSVILLE zero five six zero three six, direct GORDONSVILLE, and resume your own navigation.
cns: (3) [(H) HAFNER] [(E) it'll be the GORDON [(H) GORDONSVILLE] zero five six zero three six] [(E) direct [(H) GORDONSVILLE]] [(E) and resume your own navigation]

stm: 2>N5CF>D1-2
tim: 3313860
txt: Charlie Fox, roger, thank you.
cns: (4) [(A) Charlie Fox] [(D) roger] [(I) thank you]

stm: 2>D1-2>N5CF
tim: 3350190
txt: King Air Five Charlie Foxtrot, expect climb in about seven miles.
cns: (3) [(A) King Air Five Charlie Foxtrot] [(E) expect climb in about seven miles]

stm: 1>N5CF>D1-2
tim: 3353220
txt: Charlie Fox, roger.
cns: (4) [(A) Charlie Fox] [(D) roger]
"""


# def test_check_class_seg_ann():
#     """Test _check_class_seg_ann using cns_text."""
#     ann = Transcripts.from_ref_cns_text(cns_text)
#     # _check_class_seg_ann(ann, prnt=True)
#     _check_class_seg_ann(ann)
