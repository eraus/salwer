"""Test functions for edit distance calculations."""

import pytest

from salwer.levenshtein import (
    levenshtein_seg_fast,
    levenshtein_seg,
)

###############################################################
# Name coding of test cases: (example s1s1)
# 1. char s/t---source/target or ref/hyp
# 2. num  n (1/2/3)---Up to n consecutive
#        substitutions/deletions/insertions
# 3. char s/d/i---substitution/deletion/insertion
# 4. num  m---case number

###############################################################
# Notations in the distance table:
# ^ = deletion/insertion/substitution/
# | = boundary of segments
# + = Min of d0 for a certain value of i
# - = Min of d0 for a ceatain value of i
# * = Base value used for tight seg distance


############################################
# x1s1
# s1s1 = "J K L M N O P Q R".split()
# t1s1 = "Z K L M Y O P Q X".split()
# segs   |^    |  ^  |    ^|
# diff    S       S       S
#                                         i = 0   1   2   3   4   5   6   7   8
# s\t j   Z   K   L   M   Y   O   P   Q   X   :   :   :   :   :   :   :   :   :
# i   0+| 1   2   3 | 4   5   6 | 7   8   9   d0  :   :   :   :   :   :   :   :
#    ---------------------------------------  :   :   :   :   :   :   :   :   :
# J   1 | 1-  2   3 | 4   5   6 | 7   8   9   d1  d0  :   :   :   :   :   :   :
# K   2 | 2   1   2 | 3   4   5 | 6   7   8       d1  d0  :   :   :   :   :   :
# L   3 | 3   2   1+| 2   3   4 | 5   6   7           d1  d0  :   :   :   :   :
#    ---------------------------------------              :   :   :   :   :   :
# M   4 | 4   3   2 | 1-  2   3 | 4   5   6               d1  d0  :   :   :   :
# N   5 | 5   4   3 | 2   2   3 | 4   5   6                   d1  d0  :   :   :
# O   6 | 6   5   4 | 3   3   2+| 3   4   5                       d1  d0  :   :
#    ---------------------------------------                          :   :   :
# P   7 | 7   6   5 | 4   4   3 | 2-  3   4                           d1  d0  :
# Q   8 | 8   7   6 | 5   5   4 | 3   2   3                               d1  d0
# R   9 | 9   8   7 | 6   6   5 | 4   3   3+                                  d1

s1s1 = "J K L M N O P Q R".split()
t1s1 = "Z K L M Y O P Q X".split()

def test_levenshtein_seg_fast_1s1():
    """Test seg_size_n_edit_distance with the above lists."""
    segs = [[0, 3], [3, 6], [6, 9]]
    assert levenshtein_seg_fast(s1s1, t1s1, segs) == \
        [[3, 1], [3, 1], [3, 1]]
    assert levenshtein_seg(s1s1, t1s1, segs) == \
        [[3, 1], [3, 1], [3, 1]]

def test_levenshtein_seg_fast_head_1s1():
    """Test seg_size_n_edit_distance with the above lists."""
    segs = [[0, 3], [3, 6], [6, 9]]
    assert levenshtein_seg_fast(s1s1, t1s1, segs, head=True) == \
        [[3, 1], [3, 1], [3, 1]]
    assert levenshtein_seg(s1s1, t1s1, segs, head=True) == \
        [[3, 1], [3, 1], [3, 1]]


############################################
# x1s2
# s1s2 = "J K J M N K P Q J".split()
# t1s2 = "J K L M N O P Q R".split()
# segs   |    ^|    ^|    ^|
# diff        S     S     S
# s\t j   J   K   L   M   N   O   P   Q   R
# i   0+| 1   2   3 | 4   5   6 | 7   8   9
#    ---------------------------------------
# J   1 | 0-  1   2 | 3   4   5 | 6   7   8
# K   2 | 1   0   1 | 2   3   4 | 5   6   7
# J   3 | 2   1   1+| 2   3   4 | 5   6   7
#    ---------------------------------------
# M   4 | 3   2   2 | 1-  2   3 | 4   5   6
# N   5 | 4   3   3 | 2   1   2 | 3   4   5
# K   6 | 5   4   4 | 3   2   2+| 3   4   5
#    ---------------------------------------
# P   7 | 6   5   5 | 4   3   3 | 2-  3   4
# Q   8 | 7   6   6 | 5   4   4 | 3   2   3
# J   9 | 8   7   7 | 6   5   5 | 4   3   3+

s1s2 = "J K J M N K P Q J".split()
t1s2 = "J K L M N O P Q R".split()

def test_levenshtein_seg_fast_1s2():
    """Test seg_size_n_edit_distance with the above lists."""
    segs = [[0, 3], [3, 6], [6, 9]]
    assert levenshtein_seg_fast(s1s2, t1s2, segs) == \
        [[3, 1], [3, 1], [3, 1]]
    assert levenshtein_seg(s1s2, t1s2, segs) == \
        [[3, 1], [3, 1], [3, 1]]

def test_levenshtein_seg_fast_head_1s2():
    """Test seg_size_n_edit_distance with the above lists."""
    segs = [[0, 3], [3, 6], [6, 9]]
    assert levenshtein_seg_fast(s1s2, t1s2, segs, head=True) == \
        [[3, 1], [3, 1], [3, 1]]
    assert levenshtein_seg(s1s2, t1s2, segs, head=True) == \
        [[3, 1], [3, 1], [3, 1]]


############################################
# x1d1
# s1d1 = "A B C D E F G H I".split()
# t1d1 = "  B C D   F G H  ".split()
#        |^    |  ^  |    ^|
# segs   |    ^|    ^|    ^|
# diff        S     S     S
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

def test_levenshtein_seg_fast_1d1():
    """Test seg_size_n_edit_distance with the above lists."""
    segs = [[0, 3], [3, 6], [6, 9]]
    assert levenshtein_seg_fast(s1d1, t1d1, segs) == \
        [[3, 1], [3, 1], [3, 1]]
    assert levenshtein_seg(s1d1, t1d1, segs) == \
        [[3, 1], [3, 1], [3, 1]]

def test_levenshtein_seg_fast_head_1d1():
    """Test seg_size_n_edit_distance with the above lists."""
    segs = [[0, 3], [3, 6], [6, 9]]
    assert levenshtein_seg_fast(s1d1, t1d1, segs, head=True) == \
        [[3, 1], [3, 1], [3, 1]]
    assert levenshtein_seg(s1d1, t1d1, segs, head=True) == \
        [[3, 1], [3, 1], [3, 1]]


############################################
# x1i1
# s1i1 = "  B C D   F G H  ".split()
# t1i1 = "A B C D E F G H I".split()
#         ^|   |  ^  |   |^
# segs   |    ^|    ^|    ^|
# diff        S     S     S
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

def test_levenshtein_seg_fast_1i1():
    """Test seg_size_n_edit_distance with the above lists."""
    segs = [[0, 2], [2, 4], [4, 6]]
    assert levenshtein_seg_fast(s1i1, t1i1, segs) == \
        [[2, 0], [2, 1], [2, 0]]
    assert levenshtein_seg(s1i1, t1i1, segs) == \
        [[2, 0], [2, 1], [2, 0]]

def test_levenshtein_seg_fast_head_1i1():
    """Test seg_size_n_edit_distance with the above lists."""
    segs = [[0, 2], [2, 4], [4, 6]]
    assert levenshtein_seg_fast(s1i1, t1i1, segs, head=True) == \
        [[2, 1], [2, 1], [2, 0]]
    assert levenshtein_seg(s1i1, t1i1, segs, head=True) == \
        [[2, 1], [2, 1], [2, 0]]


############################################
# x1i2 = x1i1
# s1i2 = "  B C D   F G H  ".split()
# t1i2 = "A B C D E F G H I".split()
#         ^|     |^|     |^
# segs   |    ^|    ^|    ^|
# diff        S     S     S
#                                         i = 0   1   2   3   4   5
# s\t j   A   B   C   D   E   F   G   H   I   :   :   :   :   :   :
# i   0+| 1*| 2   3   4 | 5 | 6   7   8 | 9   d0  :   :   :   :   :
#    ---------------------------------------  :   :   :   :   :   :
# B   1 | 1 | 1-  2   3 | 4 | 5   6   7 | 8   d1  d0  :   :   :   :
# C   2 | 2 | 2   1   2 | 3 | 4   5   6 | 7       d1  d0  :   :   :
# D   3 | 3 | 3   2   1-| 2*| 3   4   5 | 6           d1  d0  :   :
#    ---------------------------------------          :   :   :   :
# F   4 | 4 | 4   3   2 | 2 | 2-  3   4 | 5               d1  d0  :
# G   5 | 5 | 5   4   3 | 3 | 3   2   3 | 4                   d1  d0
# H   6 | 6 | 6   5   4 | 4 | 4   3   2+| 3                       d1

s1i2 = "  B C D   F G H  ".split()
t1i2 = "A B C D E F G H I".split()

def test_levenshtein_seg_fast_1i2():
    """Test seg_size_n_edit_distance with the above lists."""
    segs = [[0, 3], [3, 6]]
    assert levenshtein_seg_fast(s1i2, t1i2, segs) == \
        [[3, 0], [3, 0]]
    assert levenshtein_seg(s1i2, t1i2, segs) == \
        [[3, 0], [3, 0]]

def test_levenshtein_seg_fast_head_1i2():
    """Test seg_size_n_edit_distance with the above lists."""
    segs = [[0, 3], [3, 6]]
    assert levenshtein_seg_fast(s1i2, t1i2, segs, head=True) == \
        [[3, 1], [3, 1]]
    assert levenshtein_seg(s1i2, t1i2, segs, head=True) == \
        [[3, 1], [3, 1]]


############################################
# x1sdi1
# s1sdi1 = "  A B C   E F G H".split()
# t1sdi1 = "X A   C D E X   H".split()
#           ^|  ^  |^|  ^ ^  |
# segs   |    ^|    ^|    ^|
# diff        S     S     S
# s\t j   X   A   C   D   E   X   H
#                                 i = 0   1   2   3   4   5   6
# i   0+| 1*| 2   3 | 4 | 5   6   7   d0  :   :   :   :   :   :
#    -------------------------------  :   :   :   :   :   :   :
# A   1 | 1 | 1-  2 | 3 | 4   5   6   d1  d0  :   :   :   :   :
# B   2 | 2 | 2   2 | 3 | 4   5   6       d1  d0  :   :   :   :
# C   3 | 3 | 3   2+| 3*| 4   5   6           d1  d0  :   :   :
#    -------------------------------          :   :   :   :   :
# E   4 | 4 | 4   3 | 3 | 3-  4   5               d1  d0  :   :
# F   5 | 5 | 5   4 | 4 | 4   4   5                   d1  d0  :
# G   6 | 6 | 6   5 | 5 | 5   5   5                       d1  d0
# H   7 | 7 | 7   6 | 6 | 6   6   5+                          d1

s1sdi1 = "  A B C   E F G H".split()
t1sdi1 = "X A   C D E X   H".split()

def test_levenshtein_seg_fast_1sdi1():
    """Test seg_size_n_edit_distance with the above lists."""
    segs = [[0, 3], [3, 7]]
    assert levenshtein_seg_fast(s1sdi1, t1sdi1, segs) == \
        [[3, 1], [4, 2]]
    assert levenshtein_seg(s1sdi1, t1sdi1, segs) == \
        [[3, 1], [4, 2]]

def test_levenshtein_seg_fast_head_1sdi1():
    """Test seg_size_n_edit_distance with the above lists."""
    segs = [[0, 3], [3, 7]]
    assert levenshtein_seg_fast(s1sdi1, t1sdi1, segs, head=True) == \
        [[3, 2], [4, 3]]
    assert levenshtein_seg(s1sdi1, t1sdi1, segs, head=True) == \
        [[3, 2], [4, 3]]


############################################
# x1sdi2
# s1sdi2 = "A B   D E F   H I".split()
# t1sdi2 = "B B C D   F G H I".split()
#          |^  |^|  ^  |^|   |
# segs   |    ^|    ^|    ^|
# diff        S     S     S
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

def test_levenshtein_seg_fast_1sdi2():
    """Test seg_size_n_edit_distance with the above lists."""
    segs = [[0, 2], [2, 5], [5, 7]]
    assert levenshtein_seg_fast(s1sdi2, t1sdi2, segs) == \
        [[2, 1], [3, 1], [2, 0]]
    assert levenshtein_seg(s1sdi2, t1sdi2, segs) == \
        [[2, 1], [3, 1], [2, 0]]

def test_levenshtein_seg_fast_head_1sdi2():
    """Test seg_size_n_edit_distance with the above lists."""
    segs = [[0, 2], [2, 5], [5, 7]]
    assert levenshtein_seg_fast(s1sdi2, t1sdi2, segs, head=True) == \
        [[2, 1], [3, 2], [2, 1]]
    assert levenshtein_seg(s1sdi2, t1sdi2, segs, head=True) == \
        [[2, 1], [3, 2], [2, 1]]


############################################
# x1sdi3
# s1sdi3 = "  A B C   E F G H".split()
# t1sdi3 = "X Y B C D E   Z H".split()
#           ^|^    | |  ^ ^  |
# segs   |    ^|    ^|    ^|
# diff        S     S     S
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

def test_levenshtein_seg_fast_1sdi3():
    """Test seg_size_n_edit_distance with the above lists."""
    segs = [[0, 3], [3, 7]]
    assert levenshtein_seg_fast(s1sdi3, t1sdi3, segs) == \
        [[3, 2], [4, 2]]
# Note       ^
#     This extra distance is caused by the min of d1 in Line A
    assert levenshtein_seg(s1sdi3, t1sdi3, segs) == \
        [[3, 1], [4, 2]]
# Note       ^
#     This is the correct distance.

def test_levenshtein_seg_fast_head_1sdi3():
    """Test seg_size_n_edit_distance with the above lists."""
    segs = [[0, 3], [3, 7]]
    assert levenshtein_seg_fast(s1sdi3, t1sdi3, segs, head=True) == \
        [[3, 2], [4, 3]]
    assert levenshtein_seg(s1sdi3, t1sdi3, segs, head=True) == \
        [[3, 2], [4, 3]]


############################################
# x1sdi4 = x1sdi3
# s1sdi4 = "  A B C   E F G H".split()
# t1sdi4 = "X Y B C D E   Z H".split()
#           ^ ^|   | |  ^ ^  |
# segs   |    ^|    ^|    ^|
# diff        S     S     S
# s\t j   X   Y   B   C   D   E   Z   H
# i   0+| 1   2 | 3   4 | 5 | 6   7   8
#    -----------------------------------
# A   1 | 1+  2*| 3   4 | 5 | 6   7   8
#    -----------------------------------
# B   2 | 2   2 | 2-  3 | 4 | 5   6   7
# C   3 | 3   3 | 3   2+| 3*| 4   5   6
#    -----------------------------------
# E   4 | 4   4 | 4   3 | 3 | 3-  4   5
# F   5 | 5   5 | 5   4 | 4 | 4   4   5
# G   6 | 6   6 | 6   5 | 5 | 5   5   5
# H   7 | 7   7 | 7   6 | 6 | 6   6   5+

s1sdi4 = "  A B C   E F G H".split()
t1sdi4 = "X Y B C D E   Z H".split()

def test_levenshtein_seg_fast_1sdi4():
    """Test seg_size_n_edit_distance with the above lists."""
    segs = [[1, 3], [3, 7]]
    assert levenshtein_seg_fast(s1sdi3, t1sdi3, segs) == \
        [[2, 0], [4, 2]]
    assert levenshtein_seg(s1sdi3, t1sdi3, segs) == \
        [[2, 0], [4, 2]]

def test_levenshtein_seg_fast_head_1sdi4():
    """Test seg_size_n_edit_distance with the above lists."""
    segs = [[1, 3], [3, 7]]
    assert levenshtein_seg_fast(s1sdi3, t1sdi3, segs, head=True) == \
        [[2, 1], [4, 3]]
# Note       ^
#     There is ambiguity about how to determine this.
    assert levenshtein_seg(s1sdi3, t1sdi3, segs, head=True) == \
        [[2, 1], [4, 3]]
# Note       ^
#     This is determined by the shifting.


############################################
# x2s1
# s2s1 = "A B C D E F G H".split()
# t2s1 = "X Y C D E F E B".split()
#        |^ ^    |    ^ ^|
# segs   |    ^|    ^|    ^|
# diff        S     S     S
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

def test_levenshtein_seg_fast_2s1():
    """Test seg_size_n_edit_distance with the above lists."""
    segs = [[0, 4], [4, 8]]
    assert levenshtein_seg_fast(s2s1, t2s1, segs) == \
        [[4, 2], [4, 2]]
    assert levenshtein_seg(s2s1, t2s1, segs) == \
        [[4, 2], [4, 2]]

def test_levenshtein_seg_fast_head_2s1():
    """Test seg_size_n_edit_distance with the above lists."""
    segs = [[0, 4], [4, 8]]
    assert levenshtein_seg_fast(s2s1, t2s1, segs, head=True) == \
        [[4, 2], [4, 2]]
    assert levenshtein_seg(s2s1, t2s1, segs, head=True) == \
        [[4, 2], [4, 2]]


############################################
# x2d1
# s2d1 = "A B C D E F G H I".split()
# t2d1 = "    C D     G H  ".split()
#        |^ ^  |  ^ ^  |  ^|
# segs   |    ^|    ^|    ^|
# diff        S     S     S
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

def test_levenshtein_seg_fast_2d1():
    """Test seg_size_n_edit_distance with the above lists."""
    segs = [[0, 3], [3, 7], [7, 9]]
    assert levenshtein_seg_fast(s2d1, t2d1, segs) == \
        [[3, 2], [4, 2], [2, 1]]
    assert levenshtein_seg(s2d1, t2d1, segs) == \
        [[3, 2], [4, 2], [2, 1]]

def test_levenshtein_seg_fast_head_2d1():
    """Test seg_size_n_edit_distance with the above lists."""
    segs = [[0, 3], [3, 7], [7, 9]]
    assert levenshtein_seg_fast(s2d1, t2d1, segs, head=True) == \
        [[3, 2], [4, 2], [2, 1]]
    assert levenshtein_seg(s2d1, t2d1, segs, head=True) == \
        [[3, 2], [4, 2], [2, 1]]


############################################
# x2d2
# s2d2 = "A B C D E F G".split()
# t2d2 = "    C D E    ".split()
#        |^ ^  |    ^ ^|
# segs   |    ^|    ^|    ^|
# diff        S     S     S
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

def test_levenshtein_seg_fast_2d2():
    """Test seg_size_n_edit_distance with the above lists."""
    segs = [[0, 3], [3, 7]]
    assert levenshtein_seg_fast(s2d2, t2d2, segs) == \
        [[3, 2], [4, 2]]
    assert levenshtein_seg(s2d2, t2d2, segs) == \
        [[3, 2], [4, 2]]

def test_levenshtein_seg_fast_head_2d2():
    """Test seg_size_n_edit_distance with the above lists."""
    segs = [[0, 3], [3, 7]]
    assert levenshtein_seg_fast(s2d2, t2d2, segs, head=True) == \
        [[3, 2], [4, 2]]
    assert levenshtein_seg(s2d2, t2d2, segs, head=True) == \
        [[3, 2], [4, 2]]


############################################
# x2i1
# s2i1 = "    C D E     H I".split()
# t2i1 = "A B C D E F G H I".split()
#         ^ ^ |    |^ ^|   |
# segs   |    ^|    ^|    ^|
# diff        S     S     S
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

def test_levenshtein_seg_fast_2i1():
    """Test seg_size_n_edit_distance with the above lists."""
    segs = [[0, 3], [3, 5]]
    assert levenshtein_seg_fast(s2i1, t2i1, segs) == \
        [[3, 2], [2, 2]]
# Note       ^       ^
#     Tight WER fails due to shifted min d1
    assert levenshtein_seg(s2i1, t2i1, segs) == \
        [[3, 0], [2, 0]]

def test_levenshtein_seg_fast_head_2i1():
    """Test seg_size_n_edit_distance with the above lists."""
    segs = [[0, 3], [3, 5]]
    assert levenshtein_seg_fast(s2i1, t2i1, segs, head=True) == \
        [[3, 2], [2, 2]]
    assert levenshtein_seg(s2i1, t2i1, segs, head=True) == \
        [[3, 2], [2, 2]]


############################################
# x3s1
# s3s1 = "  A B C D E F G H I".split()
# t3s1 = "B A   C D E E B A I".split()
#        |^   ^    |  ^ ^ ^  |
# segs   |    ^|    ^|    ^|
# diff        S     S     S
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

def test_levenshtein_seg_fast_3s1():
    """Test seg_size_n_edit_distance with the above lists."""
    segs = [[0, 4], [4, 9]]
    assert levenshtein_seg_fast(s3s1, t3s1, segs) == \
        [[4, 1], [5, 3]]
    assert levenshtein_seg(s3s1, t3s1, segs) == \
        [[4, 1], [5, 3]]

def test_levenshtein_seg_fast_head_3s1():
    """Test seg_size_n_edit_distance with the above lists."""
    segs = [[0, 4], [4, 9]]
    assert levenshtein_seg_fast(s3s1, t3s1, segs, head=True) == \
        [[4, 2], [5, 3]]
    assert levenshtein_seg(s3s1, t3s1, segs, head=True) == \
        [[4, 2], [5, 3]]


## Special tests

def test_levenshtein_seg_head_st1():
    """Test seg_size_n_edit_distance with the above lists."""
    s_st = "roger".split()
    t_st = "all right".split()
    segs = [[0, 1]]
    assert levenshtein_seg_fast(s_st, t_st, segs, head=True) == \
        [[1, 1]]
    assert levenshtein_seg(s_st, t_st, segs, head=True) == \
        [[1, 1]]


def test_levenshtein_seg_head_st2():
    """Test seg_size_n_edit_distance with the above lists."""
    s_st = "wilco".split()
    t_st = "will come".split()
    segs = [[0, 1]]
    assert levenshtein_seg_fast(s_st, t_st, segs, head=True) == \
        [[1, 1]]
    assert levenshtein_seg(s_st, t_st, segs, head=True) == \
        [[1, 1]]

# #    s = "A B".split()
# #    t = "C D E".split()
# s\t j   C   D   E
# i   0   1   2   3
# A   1   1   2   3
# B   2   2   2   3

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

def test_levenshtein_seg_head_st3():
    """Test seg_size_n_edit_distance with the above lists."""
    s_st = "affirm gaithersburg".split()
    t_st = "affirmative gaither sir".split()
    segs = [[1, 2]]
    assert levenshtein_seg_fast(s_st, t_st, segs, head=True) == [[1, 1]]
    assert levenshtein_seg(s_st, t_st, segs, head=True) == \
        [[1, 1]]


def test_levenshtein_seg_head_st4():
    """Test seg_size_n_edit_distance with the above lists."""
    s_st = "roger wilco".split()
    t_st = "you will tell".split()
    segs = [[1, 2]]
    assert levenshtein_seg_fast(s_st, t_st, segs, head=True) == [[1, 1]]
    assert levenshtein_seg(s_st, t_st, segs, head=True) == \
        [[1, 1]]
