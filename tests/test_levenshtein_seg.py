"""Test functions for edit distance calculations."""

import pytest

from salwer.levenshtein import (
    levenshtein_seg_fast,
)


s0 = "A B A D E B G H I".split()
t0 = "A B C D E F G H I".split()

def test_levenshtein_seg_fast_0a():
    """Test seg_size_n_edit_distance with the above lists."""
    segs = [[0, 3], [3, 6], [6, 9]]
    assert levenshtein_seg_fast(s0, t0, segs) == [[3, 1], [3, 1], [3, 0]]

def test_levenshtein_seg_fast_0b():
    """Test seg_size_n_edit_distance with the above lists."""
    segs = [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 9]]
    assert levenshtein_seg_fast(s0, t0, segs) == \
        [[1, 0], [1, 0], [1, 1], [1, 0], [1, 0], [1, 1], [3, 0]]


def test_levenshtein_seg_fast_head_0a():
    """Test seg_size_n_edit_distance with the above lists."""
    segs = [[0, 3], [3, 6], [6, 9]]
    assert levenshtein_seg_fast(s0, t0, segs, head=True) == [[3, 1], [3, 1], [3, 0]]

def test_levenshtein_seg_fast_head_0b():
    """Test seg_size_n_edit_distance with the above lists."""
    segs = [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 9]]
    assert levenshtein_seg_fast(s0, t0, segs, head=True) == \
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

def test_levenshtein_seg_fast_1a():
    """Test seg_size_n_edit_distance with the above lists."""
    segs = [[0, 3], [3, 6], [6, 9]]
    assert levenshtein_seg_fast(s1, t1, segs) == [[3, 1], [3, 1], [3, 0]]

def test_levenshtein_seg_fast_1b():
    """Test seg_size_n_edit_distance with the above lists."""
    segs = [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 9]]
    assert levenshtein_seg_fast(s1, t1, segs) == \
        [[1, 0], [1, 0], [1, 1], [1, 0], [1, 0], [1, 1], [3, 0]]


def test_levenshtein_seg_fast_head_1a():
    """Test seg_size_n_edit_distance with the above lists."""
    segs = [[0, 3], [3, 6], [6, 9]]
    assert levenshtein_seg_fast(s1, t1, segs, head=True) == [[3, 1], [3, 1], [3, 0]]

def test_levenshtein_seg_fast_head_1b():
    """Test seg_size_n_edit_distance with the above lists."""
    segs = [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 9]]
    assert levenshtein_seg_fast(s1, t1, segs, head=True) == \
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

def test_levenshtein_seg_fast_2a():
    """Test seg_size_n_edit_distance with the above lists."""
    segs = [[0, 2], [2, 4], [4, 7]]
    assert levenshtein_seg_fast(s2, t2, segs) == [[2, 0], [2, 0], [3, 0]]

def test_levenshtein_seg_fast_2b():
    """Test seg_size_n_edit_distance with the above lists."""
    segs = [[0, 1], [1, 2], [2, 3], [3, 4], [4, 7]]
    assert levenshtein_seg_fast(s2, t2, segs) == \
        [[1, 0], [1, 0], [1, 0], [1, 0], [3, 0]]


def test_levenshtein_seg_fast_head_2a():
    """Test seg_size_n_edit_distance with the above lists."""
    segs = [[0, 2], [2, 4], [4, 7]]
    assert levenshtein_seg_fast(s2, t2, segs, head=True) == [[2, 0], [2, 1], [3, 1]]

def test_levenshtein_seg_fast_head_2b():
    """Test seg_size_n_edit_distance with the above lists."""
    segs = [[0, 1], [1, 2], [2, 3], [3, 4], [4, 7]]
    assert levenshtein_seg_fast(s2, t2, segs, head=True) == \
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

def test_levenshtein_seg_fast_3b():
    """Test seg_size_n_edit_distance with the above lists."""
    segs = [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 7]]
    assert levenshtein_seg_fast(s3, t3, segs) == \
        [[1, 0], [1, 0], [1, 0], [1, 0], [1, 0], [2, 0]]


def test_levenshtein_seg_fast_head_3b():
    """Test seg_size_n_edit_distance with the above lists."""
    segs = [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 7]]
    assert levenshtein_seg_fast(s3, t3, segs, head=True) == \
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

def test_levenshtein_seg_fast_4a():
    """Test seg_size_n_edit_distance with the above lists."""
    segs = [[0, 3], [3, 5]]
    assert levenshtein_seg_fast(s4, t4, segs) == \
        [[3, 2], [2, 2]]   # tight WER fails due to shifted min d1


def test_levenshtein_seg_fast_4b():
    """Test seg_size_n_edit_distance with the above lists."""
    segs = [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5]]
    # print(f"{levenshtein_n_seg_size(s4, t4, segs) = }")
    # tight WER fails due to shifted min d1
    assert levenshtein_seg_fast(s4, t4, segs) == \
        [[1, 1], [1, 0], [1, 0], [1, 1], [1, 0]]


def test_levenshtein_seg_fast_head_4a():
    """Test seg_size_n_edit_distance with the above lists."""
    segs = [[0, 3], [3, 5]]
    assert levenshtein_seg_fast(s4, t4, segs, head=True) == \
        [[3, 2], [2, 2]]


def test_levenshtein_seg_fast_head_4b():
    """Test seg_size_n_edit_distance with the above lists."""
    segs = [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5]]
    # print(f"{levenshtein_n_seg_size(s4, t4, segs, head=True) = }")
    # WER propergates due to shifted min d1
    assert levenshtein_seg_fast(s4, t4, segs, head=True) == \
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

def test_levenshtein_seg_fast_5a():
    """Test seg_size_n_edit_distance with the above lists."""
    segs = [[0, 5], [5, 9]]
    assert levenshtein_seg_fast(s5, t5, segs) == \
        [[5, 2], [4, 2]]


def test_levenshtein_seg_fast_5b():
    """Test seg_size_n_edit_distance with the above lists."""
    segs = [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 9]]
    assert levenshtein_seg_fast(s5, t5, segs) == \
        [[1, 1], [1, 1], [1, 0], [1, 0], [1, 0], [4, 2]]


def test_levenshtein_seg_fast_head_5a():
    """Test seg_size_n_edit_distance with the above lists."""
    segs = [[0, 5], [5, 9]]
    assert levenshtein_seg_fast(s5, t5, segs, head=True) == \
        [[5, 2], [4, 2]]


def test_levenshtein_seg_fast_head_5b():
    """Test seg_size_n_edit_distance with the above lists."""
    segs = [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 9]]
    assert levenshtein_seg_fast(s5, t5, segs, head=True) == \
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
