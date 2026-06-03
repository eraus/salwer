"""Test functions for edit distance calculations."""

import pytest

from salwer.levenshtein import (
    levenshtein_seg,
    levenshtein_word,
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


def test_levenshtein_seg_head_0():
    """Test seg_size_n_edit_distance with the above lists."""
    segs = [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 9]]
    assert levenshtein_seg(s0, t0, segs, head=True) == \
        [[1, 0], [1, 0], [1, 1], [1, 0], [1, 0], [1, 1], [3, 0]]

def test_levenshtein_word_0():
    """Test seg_size_n_edit_distance with the above lists."""
    assert levenshtein_word(s0, t0) == \
        [["A", 0], ["B", 0], ["A", 1],
         ["D", 0], ["E", 0], ["B", 1],
         ["G", 0], ["H", 0], ["I", 1]]


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

def test_levenshtein_seg_head_1():
    """Test seg_size_n_edit_distance with the above lists."""
    segs = [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 9]]
    assert levenshtein_seg(s1, t1, segs, head=True) == \
        [[1, 0], [1, 0], [1, 1], [1, 0], [1, 0], [1, 1], [3, 0]]

def test_levenshtein_word_1():
    """Test seg_size_n_edit_distance with the above lists."""
    assert levenshtein_word(s1, t1) == \
        [["A", 0], ["B", 0], ["C", 1],
         ["D", 0], ["E", 0], ["F", 1],
         ["G", 0], ["H", 0], ["I", 0]]


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

def test_levenshtein_seg_head_2():
    """Test seg_size_n_edit_distance with the above lists."""
    segs = [[0, 1], [1, 2], [2, 3], [3, 4], [4, 7]]
    assert levenshtein_seg(s2, t2, segs, head=True) == \
        [[1, 0], [1, 0], [1, 1], [1, 0], [3, 1]]

def test_levenshtein_word_2():
    """Test seg_size_n_edit_distance with the above lists."""
    assert levenshtein_word(s2, t2) == \
        [["A", 0], ["B", 0], ["D", 1],
         ["E", 0], ["G", 1], ["H", 0],
         ["I", 0]]


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

def test_levenshtein_seg_head_3b():
    """Test seg_size_n_edit_distance with the above lists."""
    segs = [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 7]]
    assert levenshtein_seg(s3, t3, segs, head=True) == \
        [[1, 1], [1, 0], [1, 0], [1, 0], [1, 1], [2, 0]]

def test_levenshtein_word_3():
    """Test seg_size_n_edit_distance with the above lists."""
    assert levenshtein_word(s3, t3) == \
        [["B", 1], ["C", 0], ["D", 0],
         ["E", 0], ["G", 1], ["H", 0],
         ["I", 0]]

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


def test_levenshtein_seg_head_4():
    """Test seg_size_n_edit_distance with the above lists."""
    segs = [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5]]
    # print(f"{levenshtein_n_seg_size(s4, t4, segs, head=True) = }")
    assert levenshtein_seg(s4, t4, segs, head=True) == \
        [[1, 1], [1, 1], [1, 0], [1, 1], [1, 1]]

def test_levenshtein_word_4():
    """Test seg_size_n_edit_distance with the above lists."""
    assert levenshtein_word(s4, t4) == \
        [["C", 1], ["D", 1], ["E", 0],
         ["H", 0], ["I", 1]]


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


def test_levenshtein_seg_head_5():
    """Test seg_size_n_edit_distance with the above lists."""
    segs = [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 9]]
    assert levenshtein_seg(s5, t5, segs, head=True) == \
        [[1, 1], [1, 1], [1, 0], [1, 0], [1, 0], [4, 2]]

def test_levenshtein_word_5():
    """Test seg_size_n_edit_distance with the above lists."""
    assert levenshtein_word(s4, t4) == \
        [["A", 1], ["B", 1], ["C", 0],
         ["D", 0], ["E", 0], ["F", 1],
         ["G", 1], ["H", 0], ["I", 0]]

