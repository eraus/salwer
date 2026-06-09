"""Test functions for edit distance calculations."""

import pytest

from salwer.levenshtein import (
    num_prefix_drift,
    max_ind_of_min,
    levenshtein_seg_fast,
    levenshtein_word_fast,
    levenshtein_word,
)


# Test the helper functions used for levenshtein_word.

def test_num_prefix_drift():
    r1 = "B C D".split()
    h1 = "A C D".split()
    assert num_prefix_drift(r1, h1) == 0
    r2 = "B C D".split()
    h2 = "  C D".split()
    assert num_prefix_drift(r2, h2) == 0
    r3 = "  B C D".split()
    h3 = "A B C D".split()
    assert num_prefix_drift(r3, h3) == 1
    r4 = "    B C D".split()
    h4 = "Z A B C D".split()
    assert num_prefix_drift(r4, h4) == 2


def test_max_ind_of_min():
    d1 = [1, 0, 0, 1, 2, 3, 4, 5]
    #           ^
    assert max_ind_of_min(d1) == 2
    d2 = [3, 2, 1, 1, 1, 2, 3, 4]
    #                 ^
    assert max_ind_of_min(d2) == 4



# When we calculate the word-level Levenshtein distance using the seg-based
# approach, we need to use the head version, which includes the prefix drift
# which is called head or hallucination.


############################################
# x1s1
# s1s1 = "A B C D E F G H I".split()
# t1s1 = "Z B C D Y F G H X".split()
#        |^    |  ^  |    ^|
#                                         i = 0   1   2   3   4   5   6   7   8
# s\t j   Z   B   C   D   Y   F   G   H   X   :   :   :   :   :   :   :   :   :
# i   0+| 1   2   3 | 4   5   6 | 7   8   9   d0  :   :   :   :   :   :   :   :
#    ---------------------------------------  :   :   :   :   :   :   :   :   :
# A   1 | 1-  2   3 | 4   5   6 | 7   8   9   d1  d0  :   :   :   :   :   :   :
# B   2 | 2   1   2 | 3   4   5 | 6   7   8       d1  d0  :   :   :   :   :   :
# C   3 | 3   2   1+| 2   3   4 | 5   6   7           d1  d0  :   :   :   :   :
#    ---------------------------------------              :   :   :   :   :   :
# D   4 | 4   3   2 | 1-  2   3 | 4   5   6               d1  d0  :   :   :   :
# E   5 | 5   4   3 | 2   2   3 | 4   5   6                   d1  d0  :   :   :
# F   6 | 6   5   4 | 3   3   2+| 3   4   5                       d1  d0  :   :
#    ---------------------------------------                          :   :   :
# G   7 | 7   6   5 | 4   4   3 | 2-  3   4                           d1  d0  :
# H   8 | 8   7   6 | 5   5   4 | 3   2   3                               d1  d0
# I   9 | 9   8   7 | 6   6   5 | 4   3   3+                                  d1

s1s1 = "A B C D E F G H I".split()
t1s1 = "Z B C D Y F G H X".split()

def test_levenshtein_word_fast_1s1():
    """Test word-level Levenshtein distance using word-based approach."""
    assert levenshtein_word_fast(s1s1, t1s1) == \
        [["A", 1], ["B", 0], ["C", 0],
         ["D", 0], ["E", 1], ["F", 0],
         ["G", 0], ["H", 0], ["I", 1]]

def test_levenshtein_word_1s1():
    """Test word-level Levenshtein distance using word-based approach."""
    assert levenshtein_word(s1s1, t1s1) == \
        [["A", 2], ["B", 0], ["C", 0],
         ["D", 0], ["E", 2], ["F", 0],
         ["G", 0], ["H", 0], ["I", 2]]

def test_levenshtein_seg_fast_1s1w():
    """Test seg_size_n_edit_distance with the above lists."""
    segs = [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5],
            [5, 6], [6, 7], [7, 8], [8, 9]]
    assert levenshtein_seg_fast(s1s1, t1s1, segs) == \
        [[1, 1], [1, 0], [1, 0], [1, 0], [1, 1],
         [1, 0], [1, 0], [1, 0], [1, 1]]

def test_levenshtein_seg_fast_head_1s1w():
    """Test seg_size_n_edit_distance with the above lists."""
    segs = [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5],
            [5, 6], [6, 7], [7, 8], [8, 9]]
    assert levenshtein_seg_fast(s1s1, t1s1, segs, head=True) == \
        [[1, 1], [1, 0], [1, 0], [1, 0], [1, 1],
         [1, 0], [1, 0], [1, 0], [1, 1]]


############################################
# x1s2
# s1s2 = "A B A D E B G H A".split()
# t1s2 = "A B C D E F G H I".split()
#        |    ^|    ^|    ^|
# s\t j   A   B   C   D   E   F   G   H   I
# i   0+| 1   2   3 | 4   5   6 | 7   8   9
#    ---------------------------------------
# A   1 | 0-  1   2 | 3   4   5 | 6   7   8
# B   2 | 1   0   1 | 2   3   4 | 5   6   7
# A   3 | 2   1   1+| 2   3   4 | 5   6   7
#    ---------------------------------------
# D   4 | 3   2   2 | 1-  2   3 | 4   5   6
# E   5 | 4   3   3 | 2   1   2 | 3   4   5
# B   6 | 5   4   4 | 3   2   2+| 3   4   5
#    ---------------------------------------
# G   7 | 6   5   5 | 4   3   3 | 2-  3   4
# H   8 | 7   6   6 | 5   4   4 | 3   2   3
# A   9 | 8   7   7 | 6   5   5 | 4   3   3+

s1s2 = "A B A D E B G H A".split()
t1s2 = "A B C D E F G H I".split()

def test_levenshtein_word_fast_1s2():
    """Test word-level Levenshtein distance using word-based approach."""
    assert levenshtein_word_fast(s1s2, t1s2) == \
        [["A", 0], ["B", 0], ["A", 1],
         ["D", 0], ["E", 0], ["B", 1],
         ["G", 0], ["H", 0], ["A", 1]]

def test_levenshtein_word_1s2():
    """Test word-level Levenshtein distance using word-based approach."""
    assert levenshtein_word(s1s2, t1s2) == \
        [["A", 0], ["B", 0], ["A", 2],
         ["D", 0], ["E", 0], ["B", 2],
         ["G", 0], ["H", 0], ["A", 2]]

def test_levenshtein_seg_fast_1s2w():
    """Test seg_size_n_edit_distance with the above lists."""
    segs = [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5],
            [5, 6], [6, 7], [7, 8], [8, 9]]
    assert levenshtein_seg_fast(s1s2, t1s2, segs, head=True) == \
        [[1, 0], [1, 0], [1, 1], [1, 0], [1, 0],
         [1, 1], [1, 0], [1, 0], [1, 1]]

def test_levenshtein_seg_fast_head_1s2w():
    """Test seg_size_n_edit_distance with the above lists."""
    segs = [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5],
            [5, 6], [6, 7], [7, 8], [8, 9]]
    assert levenshtein_seg_fast(s1s2, t1s2, segs, head=True) == \
        [[1, 0], [1, 0], [1, 1], [1, 0], [1, 0],
         [1, 1], [1, 0], [1, 0], [1, 1]]


############################################
# x1d1
# s1d1 = "A B C D E F G H I".split()
# t1d1 = "  B C D   F G H  ".split()
#        |^    |  ^  |    ^|
# s\t j   B   C   D   F   G   H
# i   0+| 1   2 | 3   4 | 5   6
#    ---------------------------
# A   1 | 1-  2 | 3   4 | 5   6
# B   2 | 1   2 | 3   4 | 5   6
# C   3 | 2   1+| 2   3 | 4   5
#    ---------------------------
# D   4 | 3   2 | 1-  2 | 3   4
# E   5 | 4   3 | 2   2 | 3   4
# F   6 | 5   4 | 3   2+| 3   4
#    ---------------------------
# G   7 | 6   5 | 4   3 | 2-  3
# H   8 | 7   6 | 5   4 | 3   2
# I   9 | 8   7 | 6   5 | 4   3+

s1d1 = "A B C D E F G H I".split()
t1d1 = "  B C D   F G H  ".split()

def test_levenshtein_word_fast_1d1():
    """Test word-level Levenshtein distance using word-based approach."""
    assert levenshtein_word_fast(s1d1, t1d1) == \
        [["A", 1], ["B", 0], ["C", 0],
         ["D", 0], ["E", 1], ["F", 0],
         ["G", 0], ["H", 0], ["I", 1]]

def test_levenshtein_word_1d1():
    """Test word-level Levenshtein distance using word-based approach."""
    assert levenshtein_word(s1d1, t1d1) == \
        [["A", 2], ["B", 0], ["C", 0],
         ["D", 0], ["E", 2], ["F", 0],
         ["G", 0], ["H", 0], ["I", 2]]

def test_levenshtein_seg_fast_1d1w():
    """Test seg_size_n_edit_distance with the above lists."""
    segs = [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5],
            [5, 6], [6, 7], [7, 8], [8, 9]]
    assert levenshtein_seg_fast(s1d1, t1d1, segs) == \
        [[1, 1], [1, 0], [1, 0], [1, 0], [1, 1],
         [1, 0], [1, 0], [1, 0], [1, 0]]
# Note that Difference (1d1)         ^ #######################################

def test_levenshtein_seg_fast_head_1d1w():
    """Test seg_size_n_edit_distance with the above lists."""
    segs = [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5],
            [5, 6], [6, 7], [7, 8], [8, 9]]
    assert levenshtein_seg_fast(s1d1, t1d1, segs, head=True) == \
        [[1, 1], [1, 0], [1, 0], [1, 0], [1, 1],
         [1, 0], [1, 0], [1, 0], [1, 1]]
# Note that Difference (1d1)         ^ #######################################


############################################
# x1i1
# s1i1 = "  B C D   F G H  ".split()
# t1i1 = "A B C D E F G H I".split()
#         ^|   |  ^  |   |^
#                                         i = 0   1   2   3   4   5
# s\t j   A   B   C   D   E   F   G   H   I   :   :   :   :   :   :
# i   0+| 1*| 2   3 | 4   5   6 | 7   8 | 9   d0  :   :   :   :   :
#    ---------------------------------------  :   :   :   :   :   :
# B   1 | 1 | 1-  2 | 3   4   5 | 6   7 | 8   d1  d0  :   :   :   :
# C   2 | 2 | 2   1+| 2   3   4 | 5   6 | 7       d1  d0  :   :   :
#    ---------------------------------------          :   :   :   :
# D   3 | 3 | 3   2 | 1-  2   3 | 4   5 | 6           d1  d0  :   :
# F   4 | 4 | 4   3 | 2   2   2+| 3   4 | 5               d1  d0  :
#    ---------------------------------------                  :   :
# G   5 | 5 | 5   4 | 3   3   3 | 2-  3 | 4                   d1  d0
# H   6 | 6 | 6   5 | 4   4   4 | 3   2+| 3                       d1

s1i1 = "  B C D   F G H  ".split()
t1i1 = "A B C D E F G H I".split()

def test_levenshtein_word_fast_1i1():
    """Test word-level Levenshtein distance using word-based approach."""
    assert levenshtein_word_fast(s1i1, t1i1) == \
        [["B", 1], ["C", 0], ["D", 0],
         ["F", 1], ["G", 0], ["H", 0]]

def test_levenshtein_word_1i1():
    """Test word-level Levenshtein distance using word-based approach."""
    assert levenshtein_word(s1i1, t1i1) == \
        [["B", 2], ["C", 0], ["D", 1],
         ["F", 1], ["G", 0], ["H", 2]]

def test_levenshtein_seg_fast_1i1w():
    """Test seg_size_n_edit_distance with the above lists."""
    segs = [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 6]]
    assert levenshtein_seg_fast(s1i1, t1i1, segs) == \
        [[1, 0], [1, 0], [1, 0], [1, 0], [1, 0], [1, 0]]

def test_levenshtein_seg_fast_head_1i1w():
    """Test seg_size_n_edit_distance with the above lists."""
    segs = [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 6]]
    assert levenshtein_seg_fast(s1i1, t1i1, segs, head=True) == \
        [[1, 1], [1, 0], [1, 0], [1, 1], [1, 0], [1, 0]]


############################################
# x1sdi1
# s1sdi1 = "  A B C   E F G H".split()
# t1sdi1 = "X A   C D E X   H".split()
#           ^|  ^  | |  ^ ^  |
# s\t j   X   A   C   D   E   X   H
# i   0+| 1*| 2   3 | 4 | 5   6   7
#    -------------------------------
# A   1 | 1 | 1-  2 | 3 | 4   5   6
# B   2 | 2 | 2   2 | 3 | 4   5   6
# C   3 | 3 | 3   2+| 3*| 4   5   6
#    -------------------------------
# E   4 | 4 | 4   3 | 3 | 3-  4   5
# F   5 | 5 | 5   4 | 4 | 4   4   5
# G   6 | 6 | 6   5 | 5 | 5   5   5
# H   7 | 7 | 7   6 | 6 | 6   6   5+

s1sdi1 = "  A B C   E F G H".split()
t1sdi1 = "X A   C D E X   H".split()

def test_levenshtein_word_fast_1sdi1():
    """Test word-level Levenshtein distance using word-based approach."""
    assert levenshtein_word_fast(s1sdi1, t1sdi1) == \
        [["A", 1], ["B", 1], ["C", 0],
         ["E", 1], ["F", 1], ["G", 1], ["H", 0]]

def test_levenshtein_word_1sdi1():
    """Test word-level Levenshtein distance using word-based approach."""
    assert levenshtein_word(s1sdi1, t1sdi1) == \
        [["A", 2], ["B", 2], ["C", 1],
         ["E", 1], ["F", 2], ["G", 2], ["H", 0]]

def test_levenshtein_seg_fast_1sdi1w():
    """Test seg_size_n_edit_distance with the above lists."""
    segs = [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 7]]
    assert levenshtein_seg_fast(s1sdi1, t1sdi1, segs) == \
        [[1, 0], [1, 1], [1, 0], [1, 0], [1, 1], [1, 1], [1, 0]]

def test_levenshtein_seg_fast_head_1sdi1w():
    """Test seg_size_n_edit_distance with the above lists."""
    segs = [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 7]]
    assert levenshtein_seg_fast(s1sdi1, t1sdi1, segs, head=True) == \
        [[1, 1], [1, 1], [1, 0], [1, 1], [1, 1], [1, 1], [1, 0]]



############################################
# x1sdi2
# s1sdi2 = "A B   D E F   H I".split()
# t1sdi2 = "B B C D   F G H I".split()
#          |^  |^|  ^  |^|   |
# s\t j   B   B   C   D   F   G   H   I
#                                     i = 0   1   2   3   4   5   6
# i   0+| 1   2 | 3 | 4   5 | 6 | 7   8   d0  :   :   :   :   :   :
#    -----------------------------------  :   :   :   :   :   :   :
# A   1 | 1-  2 | 3 | 4   5 | 6 | 7   8   d1  d0  :   :   :   :   :
# B   2 | 1   1+| 2*| 3   4 | 5 | 6   7       d1  d0  :   :   :   :
#    -----------------------------------          :   :   :   :   :
# D   3 | 2   2 | 2 | 2-  3 | 4 | 5   6           d1  d0  :   :   :
# E   4 | 3   3 | 3 | 3   3 | 4 | 5   6               d1  d0  :   :
# F   5 | 4   4 | 4 | 4   3+| 4*| 5   6                   d1  d0  :
#    -----------------------------------                      :   :
# H   6 | 5   5 | 5 | 5   4 | 4 | 4-  5                       d1  d0
# I   7 | 6   6 | 6 | 6   5 | 5 | 5   4+                          d1

s1sdi2 = "A B   D E F   H I".split()
t1sdi2 = "B B C D   F G H I".split()

def test_levenshtein_word_fast_1sdi2():
    """Test word-level Levenshtein distance using word-based approach."""
    assert levenshtein_word_fast(s1sdi2, t1sdi2) == \
        [["A", 1], ["B", 0], ["D", 1],
         ["E", 1], ["F", 0], ["H", 1], ["I", 0]]

def test_levenshtein_word_1sdi2():
    """Test word-level Levenshtein distance using word-based approach."""
    assert levenshtein_word(s1sdi2, t1sdi2) == \
        [["A", 2], ["B", 1], ["D", 1],
         ["E", 2], ["F", 1], ["H", 1], ["I", 0]]

def test_levenshtein_seg_fast_1sdi2w():
    """Test seg_size_n_edit_distance with the above lists."""
    segs = [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 7]]
    assert levenshtein_seg_fast(s1sdi2, t1sdi2, segs) == \
        [[1, 1], [1, 0], [1, 0], [1, 1], [1, 0], [1, 0], [1, 0]]

def test_levenshtein_seg_fast_head_1sdi2w():
    """Test seg_size_n_edit_distance with the above lists."""
    segs = [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 7]]
    assert levenshtein_seg_fast(s1sdi2, t1sdi2, segs, head=True) == \
        [[1, 1], [1, 0], [1, 1], [1, 1], [1, 0], [1, 1], [1, 0]]


############################################
# x1sdi3
# s1sdi3 = "  A B C   E F G H".split()
# t1sdi3 = "X Y B C D E   Z H".split()
#           ^|^    | |  ^ ^  |
# s\t j   X   Y   B   C   D   E   Z   H
# i   0+| 1 | 2   3   4 | 5 | 6   7   8
#    -----------------------------------
# A   1 | 1-| 2   3   4 | 5 | 6   7   8
# B   2 | 2 | 2   2   3 | 4 | 5   6   7
# C   3 | 3 | 3   3   2+| 3*| 4   5   6
#    -----------------------------------
# E   4 | 4 | 4   4   3 | 3 | 3-  4   5
# F   5 | 5 | 5   5   4 | 4 | 4   4   5
# G   6 | 6 | 6   6   5 | 5 | 5   5   5
# H   7 | 7 | 7   7   6 | 6 | 6   6   5+

s1sdi3 = "  A B C   E F G H".split()
t1sdi3 = "X Y B C D E   Z H".split()

def test_levenshtein_word_fast_1sdi3():
    """Test word-level Levenshtein distance using word-based approach."""
    assert levenshtein_word_fast(s1sdi3, t1sdi3) == \
        [["A", 1], ["B", 1], ["C", 0], ["E", 1], ["F", 1], ["G", 1], ["H", 0]]
# Note         ^         ^
#     Values are spreaded.

def test_levenshtein_word_1sdi3():
    """Test word-level Levenshtein distance using word-based approach."""
    assert levenshtein_word(s1sdi3, t1sdi3) == \
        [["A", 4], ["B", 0], ["C", 1],
         ["E", 1], ["F", 2], ["G", 2], ["H", 0]]

def test_levenshtein_seg_fast_1sdi3w():
    """Test seg_size_n_edit_distance with the above lists."""
    segs = [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 7]]
    assert levenshtein_seg_fast(s1sdi3, t1sdi3, segs) == \
        [[1, 1], [1, 0], [1, 0], [1, 0], [1, 1], [1, 1], [1, 0]]
# Note       ^
#     Number is off by 1.

def test_levenshtein_seg_fast_head_1sdi3w():
    """Test seg_size_n_edit_distance with the above lists."""
    segs = [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 7]]
    assert levenshtein_seg_fast(s1sdi3, t1sdi3, segs, head=True) == \
        [[1, 1], [1, 1], [1, 0], [1, 1], [1, 1], [1, 1], [1, 0]]
# Note       ^       ^
#     Values are spreaded.


############################################
# x2s1
# s2s1 = "A B C D E F G H".split()
# t2s1 = "X Y C D E F E B".split()
#        |^ ^    |    ^ ^|
# s\t j   X   Y   C   D   E   F   E   B
# i   0+| 1   2   3   4 | 5   6   7   8
#    -----------------------------------
# A   1 | 1-  2   3   4 | 5   6   7   8
# B   2 | 2   2   3   4 | 5   6   7   7
# C   3 | 3   3   2   3 | 4   5   6   7
# D   4 | 4   4   3   2+| 3   4   5   6
#    -----------------------------------
# E   5 | 5   5   4   3 | 2-  3   4   5
# F   6 | 6   6   5   4 | 3   2   3   4
# G   7 | 7   7   6   5 | 4   3   3   4
# H   8 | 8   8   7   6 | 5   4   4   4+

s2s1 = "A B C D E F G H".split()
t2s1 = "X Y C D E F E B".split()

def test_levenshtein_word_fast_2s1():
    """Test word-level Levenshtein distance using word-based approach."""
    assert levenshtein_word_fast(s2s1, t2s1) == \
        [["A", 1], ["B", 1], ["C", 0], ["D", 0],
         ["E", 0], ["F", 0], ["G", 1], ["H", 1]]

def test_levenshtein_word_2s1():
    """Test word-level Levenshtein distance using word-based approach."""
    assert levenshtein_word(s2s1, t2s1) == \
        [["A", 2], ["B", 2], ["C", 0], ["D", 0],
         ["E", 0], ["F", 0], ["G", 2], ["H", 2]]

def test_levenshtein_seg_fast_2s1w():
    """Test seg_size_n_edit_distance with the above lists."""
    segs = [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5],
            [5, 6], [6, 7], [7, 8]]
    assert levenshtein_seg_fast(s2s1, t2s1, segs) == \
        [[1, 1], [1, 1], [1, 0], [1, 0], [1, 0], [1, 0], [1, 1], [1, 1]]

def test_levenshtein_seg_fast_head_2s1w():
    """Test seg_size_n_edit_distance with the above lists."""
    segs = [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5],
            [5, 6], [6, 7], [7, 8]]
    assert levenshtein_seg_fast(s2s1, t2s1, segs, head=True) == \
        [[1, 1], [1, 1], [1, 0], [1, 0], [1, 0], [1, 0], [1, 1], [1, 1]]



############################################
# x2d1
# s2d1 = "A B C D E F G H I".split()
# t2d1 = "    C D     G H  ".split()
#        |^ ^  |  ^ ^  |  ^|
# s\t j   C   D   G   H
# i   0+| 1 | 2   3 | 4
#    -------------------
# A   1 | 1-| 2   3 | 4
# B   2 | 2 | 2   3 | 4
# C   3 | 2+| 3   3 | 4
#    -------------------
# D   4 | 3 | 2-  3 | 4
# E   5 | 4 | 3   3 | 4
# F   6 | 5 | 4   4 | 4
# G   7 | 6 | 5   4+| 5
#    -------------------
# H   8 | 7 | 6   5 | 4-
# I   9 | 8 | 7   6 | 5+

s2d1 = "A B C D E F G H I".split()
t2d1 = "    C D     G H  ".split()

def test_levenshtein_word_fast_2d1():
    """Test word-level Levenshtein distance using word-based approach."""
    assert levenshtein_word_fast(s2d1, t2d1) == \
        [["A", 1], ["B", 1], ["C", 0], ["D", 0],
         ["E", 1], ["F", 1], ["G", 0], ["H", 0], ["I", 1]]

def test_levenshtein_word_2d1():
    """Test word-level Levenshtein distance using word-based approach."""
    assert levenshtein_word(s2d1, t2d1) == \
        [["A", 2], ["B", 2], ["C", 0], ["D", 0],
         ["E", 2], ["F", 2], ["G", 0], ["H", 0], ["I", 2]]

def test_levenshtein_seg_fast_2d1w():
    """Test seg_size_n_edit_distance with the above lists."""
    segs = [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5],
            [5, 6], [6, 7], [7, 8], [8, 9]]
    assert levenshtein_seg_fast(s2d1, t2d1, segs) == \
        [[1, 1], [1, 1], [1, 0], [1, 0], [1, 1],
         [1, 1], [1, 0], [1, 0], [1, 0]]
# Note that Difference (2d1)         ^ #######################################

def test_levenshtein_seg_fast_head_2d1w():
    """Test seg_size_n_edit_distance with the above lists."""
    segs = [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5],
            [5, 6], [6, 7], [7, 8], [8, 9]]
    assert levenshtein_seg_fast(s2d1, t2d1, segs, head=True) == \
        [[1, 1], [1, 1], [1, 0], [1, 0], [1, 1],
         [1, 1], [1, 0], [1, 0], [1, 1]]
# Note that Difference (2d1)         ^ #######################################



############################################
# x2d2
# s2d2 = "A B C D E F G".split()
# t2d2 = "    C D E    ".split()
#        |^ ^  |    ^ ^|
# s\t j   C   D   E
# i   0+| 1 | 2   3
#    ---------------
# A   1 | 1-| 2   3
# B   2 | 2 | 2   3
# C   3 | 2+| 3   3
#    ---------------
# D   4 | 3 | 2-  3
# E   5 | 4 | 3   2
# F   6 | 5 | 4   3
# G   7 | 6 | 5   4+

s2d2 = "A B C D E F G".split()
t2d2 = "    C D E    ".split()

def test_levenshtein_word_fast_2d2():
    """Test word-level Levenshtein distance using word-based approach."""
    assert levenshtein_word_fast(s2d2, t2d2) == \
        [["A", 1], ["B", 1], ["C", 0], ["D", 0],
         ["E", 0], ["F", 1], ["G", 1]]

def test_levenshtein_word_2d2():
    """Test word-level Levenshtein distance using word-based approach."""
    assert levenshtein_word(s2d2, t2d2) == \
        [["A", 2], ["B", 2], ["C", 0], ["D", 0],
         ["E", 0], ["F", 2], ["G", 2]]

def test_levenshtein_seg_fast_2d2w():
    """Test seg_size_n_edit_distance with the above lists."""
    segs = [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 7]]
    assert levenshtein_seg_fast(s2d2, t2d2, segs) == \
        [[1, 1], [1, 1], [1, 0], [1, 0], [1, 0], [1, 0], [1, 0]]
# Note that Difference (2d2)                         ^       ^

def test_levenshtein_seg_fast_head_2d2w():
    """Test seg_size_n_edit_distance with the above lists."""
    segs = [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 7]]
    assert levenshtein_seg_fast(s2d2, t2d2, segs, head=True) == \
        [[1, 1], [1, 1], [1, 0], [1, 0], [1, 0], [1, 1], [1, 1]]
# Note that Difference (2d2)                         ^       ^


############################################
# x2i1
# s2i1 = "    C D E     H I".split()
# t2i1 = "A B C D E F G H I".split()
#         ^ ^ |    |^ ^|   |
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

s2i1 = "    C D E     H I".split()
t2i1 = "A B C D E F G H I".split()

def test_levenshtein_word_fast_2i1():
    """Test word-level Levenshtein distance using word-based approach."""
    assert levenshtein_word_fast(s2i1, t2i1) == \
        [["C", 1], ["D", 1], ["E", 0], ["H", 1], ["I", 1]]
# Note         ^         ^
#     Values are spreaded.

def test_levenshtein_word_2i1():
    """Test word-level Levenshtein distance using word-based approach."""
    assert levenshtein_word(s2i1, t2i1) == \
        [["C", 4], ["D", 0], ["E", 2], ["H", 2], ["I", 0]]

def test_levenshtein_seg_fast_2i1w():
    """Test seg_size_n_edit_distance with the above lists."""
    segs = [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5]]
    assert levenshtein_seg_fast(s2i1, t2i1, segs) == \
        [[1, 1], [1, 0], [1, 0], [1, 1], [1, 0]]
# Note       ^                       ^
#     Tight WER fails due to shifted min d1

def test_levenshtein_seg_fast_head_2i1w():
    """Test seg_size_n_edit_distance with the above lists."""
    segs = [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5]]
    assert levenshtein_seg_fast(s2i1, t2i1, segs, head=True) == \
        [[1, 1], [1, 1], [1, 0], [1, 1], [1, 1]]
# Note               ^                       ^
#     Tight WER fails due to shifted min d1

# NOTE: If we have 2+ consecutive prefix hallucination words,
# the first two words in the reference will be affected. To address this issue,
# we can remove a word in the target repeatedly until the situation is getting
# worse.


############################################
# x3s1
# s3s1 = "  A B C D E F G H I".split()
# t3s1 = "B A   C D E E B A I".split()
#        |^   ^    |  ^ ^ ^  |
# s\t j   B   A   C   D   E   E   B   A   I
# i   0+  1*| 2   3   4 | 5   6   7   8   9
#     --------------------------------------
# A   1   1 | 1-  2   3 | 4   5   6   7   8
# B   2   1 | 2   2   3 | 4   5   5   6   7
# C   3   2 | 2   2   3 | 4   5   6   6   7
# D   4   3 | 3   3   2+| 3   4   5   6   7
#     --------------------------------------
# E   5   4 | 4   4   3 | 2-  3   4   5   6
# F   6   5 | 5   5   4 | 3   3   4   5   6
# G   7   6 | 6   6   5 | 4   4   4   5   6
# H   8   7 | 7   7   6 | 5   5   5   5   6
# I   9   8 | 8   8   7 | 6   6   6   6   5+

s3s1 = "  A B C D E F G H I".split()
t3s1 = "B A   C D E E B A I".split()

def test_levenshtein_word_fast_3s1():
    """Test word-level Levenshtein distance using word-based approach."""
    assert levenshtein_word_fast(s3s1, t3s1) == \
        [["A", 1], ["B", 0], ["C", 1], ["D", 0], ["E", 0], ["F", 1],
                                        ["G", 1], ["H", 1], ["I", 0]]
# Note                   ^         ^  These are issues.
def test_levenshtein_word_3s1():
    """Test word-level Levenshtein distance using word-based approach."""
    assert levenshtein_word(s3s1, t3s1) == \
        [["A", 2], ["B", 2], ["C", 0], ["D", 0], ["E", 0], ["F", 2],
                                        ["G", 2], ["H", 2], ["I", 0]]
# Note                   ^         ^  These are correct.

def test_levenshtein_seg_fast_3s1w():
    """Test seg_size_n_edit_distance with the above lists."""
    segs = [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5],
            [5, 6], [6, 7], [7, 8], [8, 9]]
    # print(f"{levenshtein_seg_fast(s3s1, t3s1, segs) = }")
    assert levenshtein_seg_fast(s3s1, t3s1, segs) == \
        [[1, 0], [1, 0], [1, 0], [1, 0], [1, 0], [1, 1], [1, 1], [1, 1], [1, 0]]
# Note       ^       ^

def test_levenshtein_seg_fast_head_3s1w():
    """Test seg_size_n_edit_distance with the above lists."""
    segs = [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5],
            [5, 6], [6, 7], [7, 8], [8, 9]]
    # print(f"{levenshtein_seg_fast(s3s1, t3s1, segs, head=True) = }")
    assert levenshtein_seg_fast(s3s1, t3s1, segs, head=True) == \
        [[1, 1], [1, 0], [1, 1], [1, 0], [1, 0], [1, 1], [1, 1], [1, 1], [1, 0]]
# Note               ^       ^

