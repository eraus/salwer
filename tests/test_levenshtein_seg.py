"""Test functions for edit distance calculations."""

import pytest

from salwer.levenshtein import (
    levenshtein_align_fast,
    levenshtein_align,
    levenshtein_seg_fast,
    levenshtein_seg,
)

###############################################################
# Name coding of test cases: (example s1s1a)
# 1. char s/t/sg---source/target/segment
# 2. num  n (1/2/3)---Up to n consecutive
#        substitutions/deletions/insertions
# 3. char s/d/i---substitution/deletion/insertion
# 4. num  m---case number for unique s and t sequences
# 5. char a/b/c---case number for the same s and t sequences

###############################################################
# Notations in the distance table:
# ^ = substitution/deletion/insertion.
# | = boundary of segments.
# + = minimum value(s) of d1 with the max index for a given i corresponding
#       to the upper boundary of a segment before swapping d0 and d1.
# - = minimum value of d1 with the max index for a given i corresponding
#       to the lower boundary of a segment before swapping d0 and d1.
# * = (before the number) base value used for no-head seg distance.

# Comments about d0 and d1 can be found below in the x1s1a example.


#--------------------------------------------------------------------
# Test Levenshtein segment alignment and distance for x1s1
#--------------------------------------------------------------------

s1s1 = "J K L M N O P Q R".split()
t1s1 = "Z K L M Y O P Q X".split()

# x1s1a                                         :
#    s = "J K L M N O P Q R".split()            :
#    t = "Z K L M Y O P Q X".split()            :
# segs   |^    |  ^  |    ^|                    :
# type    S       S       S                     :
#                                               :
# s\t     Z   K   L   M   Y   O   P   Q   X     :
#     j >                                       :
#  i *0+| 1   2   3 | 4   5   6 | 7   8   9     :                d0 (i = 0)
#  v ---------------------------------------    :
# J   1 | 1-  2   3 | 4   5   6 | 7   8   9     :    d1 (i = 0), d0 (i = 1)
# K   2 | 2   1   2 | 3   4   5 | 6   7   8     :    d1 (i = 1), d0 (i = 2)
# L   3 | 3   2  *1+| 2   3   4 | 5   6   7     :    d1 (i = 2), d0 (i = 3)
#    ---------------------------------------    :
# M   4 | 4   3   2 | 1-  2   3 | 4   5   6     :    d1 (i = 3), d0 (i = 4)
# N   5 | 5   4   3 | 2   2   3 | 4   5   6     :    d1 (i = 4), d0 (i = 5)
# O   6 | 6   5   4 | 3   3  *2+| 3   4   5     :    d1 (i = 5), d0 (i = 6)
#    ---------------------------------------    :
# P   7 | 7   6   5 | 4   4   3 | 2-  3   4     :    d1 (i = 6), d0 (i = 7)
# Q   8 | 8   7   6 | 5   5   4 | 3   2   3     :    d1 (i = 7), d0 (i = 8)
# R   9 | 9   8   7 | 6   6   5 | 4   3   3+    :    d1 (i = 8)

sg1s1a = [[0, 3], [3, 6], [6, 9]]

def test_levenshtein_align_1s1a_all_normal():
    assert levenshtein_align_fast(s1s1, t1s1, sg1s1a) == \
        [[0, 3], [3, 6], [6, 9]]
    assert levenshtein_align(s1s1, t1s1, sg1s1a) == \
        [[0, 3], [3, 6], [6, 9]]

def test_levenshtein_seg_1s1a_all_normal():
    assert levenshtein_seg_fast(s1s1, t1s1, sg1s1a) == \
        [[3, 1], [3, 1], [3, 1]]
    assert levenshtein_seg(s1s1, t1s1, sg1s1a) == \
        [[3, 1], [3, 1], [3, 1]]

def test_levenshtein_seg_head_1s1a_all_normal():
    assert levenshtein_seg_fast(s1s1, t1s1, sg1s1a, head=True) == \
        [[3, 1], [3, 1], [3, 1]]
    assert levenshtein_seg(s1s1, t1s1, sg1s1a, head=True) == \
        [[3, 1], [3, 1], [3, 1]]


# x1s1b                                         :
#    s = "J K L M N O P Q R".split()            :
#    t = "Z K L M Y O P Q X".split()            :
# segs   |^      |^|      ^|                    :
# type    S       S       S                     :
#                                               :
# s\t     Z   K   L   M   Y   O   P   Q   X     :
#     j >                                       :
#  i *0+| 1   2   3   4 | 5 | 6   7   8   9     :
#  v ---------------------------------------    :
# J   1 | 1-  2   3   4 | 5 | 6   7   8   9     :
# K   2 | 2   1   2   3 | 4 | 5   6   7   8     :
# L   3 | 3   2   1   2 | 3 | 4   5   6   7     :
# M   4 | 4   3   2  *1+| 2 | 3   4   5   6     :
#    ---------------------------------------    :
# N   5 | 5   4   3   2 |*2+| 3   4   5   6     :
#    ---------------------------------------    :
# O   6 | 6   5   4   3 | 3 | 2-  3   4   5     :
# P   7 | 7   6   5   4 | 4 | 3   2   3   4     :
# Q   8 | 8   7   6   5 | 5 | 4   3   2   3     :
# R   9 | 9   8   7   6 | 6 | 5   4   3   3+    :

sg1s1b = [[0, 4], [4, 5], [5, 9]]

def test_levenshtein_align_1s1b():
    assert levenshtein_align_fast(s1s1, t1s1, sg1s1b) == \
        [[0, 4], [4, 5], [5, 9]]
    assert levenshtein_align(s1s1, t1s1, sg1s1b) == \
        [[0, 4], [4, 5], [5, 9]]

def test_levenshtein_seg_1s1b():
    assert levenshtein_seg_fast(s1s1, t1s1, sg1s1b) == \
        [[4, 1], [1, 1], [4, 1]]
    assert levenshtein_seg(s1s1, t1s1, sg1s1b) == \
        [[4, 1], [1, 1], [4, 1]]

def test_levenshtein_seg_head_1s1b():
    assert levenshtein_seg_fast(s1s1, t1s1, sg1s1b, head=True) == \
        [[4, 1], [1, 1], [4, 1]]
    assert levenshtein_seg(s1s1, t1s1, sg1s1b, head=True) == \
        [[4, 1], [1, 1], [4, 1]]


# x1s1c
#    s = "J K L M N O P Q R".split()
#    t = "Z K L M Y O P Q X".split()
# segs   |^      |^       ^|
# type    S       S       S
#
# s\t     Z   K   L   M   Y   O   P   Q   X
#     j >
#  i *0+| 1   2   3   4 | 5   6   7   8   9
#  v ---------------------------------------
# J   1 | 1-  2   3   4 | 5   6   7   8   9
# K   2 | 2   1   2   3 | 4   5   6   7   8
# L   3 | 3   2   1   2 | 3   4   5   6   7
# M   4 | 4   3   2  *1+| 2   3   4   5   6
#    ---------------------------------------
# N   5 | 5   4   3   2 | 2-  3   4   5   6
# O   6 | 6   5   4   3 | 3   2   3   4   5
# P   7 | 7   6   5   4 | 4   3   2   3   4
# Q   8 | 8   7   6   5 | 5   4   3   2   3
# R   9 | 9   8   7   6 | 6   5   4   3   3+

sg1s1c = [[0, 4], [4, 9]]

def test_levenshtein_align_1s1c():
    assert levenshtein_align_fast(s1s1, t1s1, sg1s1c) == \
        [[0, 4], [4, 9]]
    assert levenshtein_align(s1s1, t1s1, sg1s1c) == \
        [[0, 4], [4, 9]]

def test_levenshtein_seg_1s1c():
    assert levenshtein_seg_fast(s1s1, t1s1, sg1s1c) == \
        [[4, 1], [5, 2]]
    assert levenshtein_seg(s1s1, t1s1, sg1s1c) == \
        [[4, 1], [5, 2]]

def test_levenshtein_seg_head_1s1c():
    assert levenshtein_seg_fast(s1s1, t1s1, sg1s1c, head=True) == \
        [[4, 1], [5, 2]]
    assert levenshtein_seg(s1s1, t1s1, sg1s1c, head=True) == \
        [[4, 1], [5, 2]]


#--------------------------------------------------------------------
# Test Levenshtein segment alignment and distance for x1s2
#--------------------------------------------------------------------

s1s2 = "J K J M N K P Q J".split()
t1s2 = "J K L M N O P Q R".split()

# x1s2
#    s = "J K J M N K P Q J".split()
#    t = "J K L M N O P Q R".split()
# segs   |    ^|    ^|    ^|
# type        S     S     S
#
# s\t j   J   K   L   M   N   O   P   Q   R
# i  *0+| 1   2   3 | 4   5   6 | 7   8   9
#    ---------------------------------------
# J   1 | 0-  1   2 | 3   4   5 | 6   7   8
# K   2 | 1   0   1 | 2   3   4 | 5   6   7
# J   3 | 2   1+ *1+| 2   3   4 | 5   6   7
#    ---------------------------------------
# M   4 | 3   2   2 | 1-  2   3 | 4   5   6
# N   5 | 4   3   3 | 2   1   2 | 3   4   5
# K   6 | 5   4   4 | 3   2+ *2+| 3   4   5
#    ---------------------------------------
# P   7 | 6   5   5 | 4   3   3 | 2-  3   4
# Q   8 | 7   6   6 | 5   4   4 | 3   2   3
# J   9 | 8   7   7 | 6   5   5 | 4   3+  3+

sg1s2a = [[0, 3], [3, 6], [6, 9]]

def test_levenshtein_align_1s2a():
    assert levenshtein_align_fast(s1s2, t1s2, sg1s2a) == \
        [[0, 3], [3, 6], [6, 9]]
    assert levenshtein_align(s1s2, t1s2, sg1s2a) == \
        [[0, 3], [3, 6], [6, 9]]

def test_levenshtein_seg_1s2a():
    assert levenshtein_seg_fast(s1s2, t1s2, sg1s2a) == \
        [[3, 1], [3, 1], [3, 1]]
    assert levenshtein_seg(s1s2, t1s2, sg1s2a) == \
        [[3, 1], [3, 1], [3, 1]]

def test_levenshtein_seg_head_1s2a():
    assert levenshtein_seg_fast(s1s2, t1s2, sg1s2a, head=True) == \
        [[3, 1], [3, 1], [3, 1]]
    assert levenshtein_seg(s1s2, t1s2, sg1s2a, head=True) == \
        [[3, 1], [3, 1], [3, 1]]


#--------------------------------------------------------------------
# Test Levenshtein segment alignment and distance for x1d1
#--------------------------------------------------------------------

s1d1 = "J K L M N O P Q R".split()
t1d1 = "  K L M   O P Q  ".split()

# x1d1a                                 :
#    s = "J K L M N O P Q R".split()    :
#    t = "  K L M   O P Q  ".split()    :
# segs   |^    |  ^  |    ^|            :
# type    D       D       D             :
#                                       :
# s\t     K   L   M   O   P   Q         :
#     j >                               :
#  i *0+| 1   2 | 3   4 | 5   6         :
#    ---------------------------        :
# J   1 | 1-  2 | 3   4 | 5   6         :
# K   2 | 1   2 | 3   4 | 5   6         :
# L   3 | 2  *1+| 2   3 | 4   5         :
#    ---------------------------        :
# M   4 | 3   2 | 1-  2 | 3   4         :
# N   5 | 4   3 | 2   2 | 3   4         :
# O   6 | 5   4 | 3  *2+| 3   4         :
#    ---------------------------        :
# P   7 | 6   5 | 4   3 | 2-  3         :
# Q   8 | 7   6 | 5   4 | 3   2         :
# R   9 | 8   7 | 6   5 | 4   3+        :

sg1d1a = [[0, 3], [3, 6], [6, 9]]

def test_levenshtein_align_1d1a():
    assert levenshtein_align_fast(s1d1, t1d1, sg1d1a) == \
        [[0, 2], [2, 4], [4, 6]]
    assert levenshtein_align(s1d1, t1d1, sg1d1a) == \
        [[0, 2], [2, 4], [4, 6]]

def test_levenshtein_seg_1d1a():
    assert levenshtein_seg_fast(s1d1, t1d1, sg1d1a) == \
        [[3, 1], [3, 1], [3, 1]]
    assert levenshtein_seg(s1d1, t1d1, sg1d1a) == \
        [[3, 1], [3, 1], [3, 1]]

def test_levenshtein_seg_head_1d1a():
    assert levenshtein_seg_fast(s1d1, t1d1, sg1d1a, head=True) == \
        [[3, 1], [3, 1], [3, 1]]
    assert levenshtein_seg(s1d1, t1d1, sg1d1a, head=True) == \
        [[3, 1], [3, 1], [3, 1]]


# x1d1b                                 :
#    s = "J K L M N O P Q R".split()    :
#    t = "  K L M   O P Q  ".split()    :
# segs   |^      |^|      ^|            :
# type    D       D       D             :
#                                       :
# s\t     K   L   M   O   P   Q         :
#     j >                               :
#  i *0+| 1   2   3 | 4 | 5   6         :
#  v ---------------------------        :
# J   1 | 1-  2   3 | 4 | 5   6         :
# K   2 | 1   2   3 | 4 | 5   6         :
# L   3 | 2   1   2 | 3 | 4   5         :
# M   4 | 3   2  *1+| 2 | 3   4         :
#    ---------------------------        :
# N   5 | 4   3  *2 | 2+| 3   4         :
#    ---------------------------        :
# O   6 | 5   4   3 | 2-  3   4         :
# P   7 | 6   5   4 | 3   2   3         :
# Q   8 | 7   6   5 | 4   3   2         :
# R   9 | 8   7   6 | 5   4   3+        :

sg1d1b = [[0, 4], [4, 5], [5, 9]]

def test_levenshtein_align_1d1b():
    assert levenshtein_align_fast(s1d1, t1d1, sg1d1b) == \
        [[0, 3], [3, 3], [3, 6]]
    assert levenshtein_align(s1d1, t1d1, sg1d1b) == \
        [[0, 3], [3, 3], [3, 6]]
        # [[0, 3], [3, 4], [3, 6]]
    #                ^ ^   Correction of upper boundary overshoot

def test_levenshtein_seg_1d1b():
    assert levenshtein_seg_fast(s1s1, t1s1, sg1d1b) == \
        [[4, 1], [1, 1], [4, 1]]
    assert levenshtein_seg(s1s1, t1s1, sg1d1b) == \
        [[4, 1], [1, 1], [4, 1]]

def test_levenshtein_seg_head_1d1b():
    assert levenshtein_seg_fast(s1d1, t1d1, sg1d1b, head=True) == \
        [[4, 1], [1, 1], [4, 1]]
    assert levenshtein_seg(s1d1, t1d1, sg1d1b, head=True) == \
        [[4, 1], [1, 1], [4, 1]]


# x1d1c                                 :
#    s = "J K L M N O P Q R".split()    :
#    t = "  K L M   O P Q  ".split()    :
# segs   |^      |^       ^|            :
# type    D       D       D             :
#                                       :
# s\t     K   L   M   O   P   Q         :
#     j >                               :
#  i *0+| 1   2   3 | 4   5   6         :
#  v ---------------------------        :
# J   1 | 1-  2   3 | 4   5   6         :
# K   2 | 1   2   3 | 4   5   6         :
# L   3 | 2   1   2 | 3   4   5         :
# M   4 | 3   2  *1+| 2   3   4         :
#    ---------------------------        :
# N   5 | 4   3   2 | 2-  3   4         :
# O   6 | 5   4   3 | 2   3   4         :
# P   7 | 6   5   4 | 3   2   3         :
# Q   8 | 7   6   5 | 4   3   2         :
# R   9 | 8   7   6 | 5   4   3+        :

sg1d1c = [[0, 4], [4, 9]]

def test_levenshtein_align_1d1c():
    assert levenshtein_align_fast(s1d1, t1d1, sg1d1c) == \
        [[0, 3], [3, 6]]
    assert levenshtein_align(s1d1, t1d1, sg1d1c) == \
        [[0, 3], [3, 6]]

def test_levenshtein_seg_1d1c():
    assert levenshtein_seg_fast(s1s1, t1s1, sg1d1c) == \
        [[4, 1], [5, 2]]
    assert levenshtein_seg(s1s1, t1s1, sg1d1c) == \
        [[4, 1], [5, 2]]

def test_levenshtein_seg_head_1d1c():
    assert levenshtein_seg_fast(s1d1, t1d1, sg1d1c, head=True) == \
        [[4, 1], [5, 2]]
    assert levenshtein_seg(s1d1, t1d1, sg1d1c, head=True) == \
        [[4, 1], [5, 2]]


# x1d1d                                 :
#    s = "J K L M N O P Q R".split()    :
#    t = "  K L M   O P Q  ".split()    :
# segs   |^      |^|      ^|            :
# type    D       D       D             :
#                                       :
# s\t     K   L   M   O   P   Q         :
#     j >                               :
#  i *0+| 1   2   3 | 4 | 5   6         :
#  v ---------------------------        :
# J   1 | 1-  2   3 | 4 | 5   6         :
# K   2 | 1   2   3 | 4 | 5   6         :
# L   3 | 2   1   2 | 3 | 4   5         :
# M   4 | 3   2  *1+| 2 | 3   4         :
#    ---------------------------        :
# N   5 | 4   3  *2 | 2+| 3   4         :
#    ---------------------------        :
# O   6 | 5   4   3 | 2-  3   4         :
# P   7 | 6   5   4 | 3   2   3         :
# Q   8 | 7   6   5 | 4   3   2         :
# R   9 | 8   7   6 | 5   4   3+        :

sg1d1d = [[0, 4], [4, 5]]

def test_levenshtein_align_1d1d():
    assert levenshtein_align_fast(s1d1, t1d1, sg1d1d) == \
        [[0, 3], [3, 3]]
    assert levenshtein_align(s1d1, t1d1, sg1d1d) == \
        [[0, 3], [3, 3]]
        # [[0, 3], [3, 4]]
    #                ^ ^   Correction of upper boundary overshoot

def test_levenshtein_seg_1d1d():
    assert levenshtein_seg_fast(s1s1, t1s1, sg1d1d) == \
        [[4, 1], [1, 1]]
    assert levenshtein_seg(s1s1, t1s1, sg1d1d) == \
        [[4, 1], [1, 1]]

def test_levenshtein_seg_head_1d1d():
    assert levenshtein_seg_fast(s1d1, t1d1, sg1d1d, head=True) == \
        [[4, 1], [1, 1]]
    assert levenshtein_seg(s1d1, t1d1, sg1d1d, head=True) == \
        [[4, 1], [1, 1]]


#--------------------------------------------------------------------
# Test Levenshtein segment alignment and distance for x1i1
#--------------------------------------------------------------------

s1i1 = "  K L M   O P Q  ".split()
t1i1 = "J K L M N O P Q R".split()

# x1i1a                                         :
#    s = "  K L M   O P Q  ".split()            :
#    t = "J K L M N O P Q R".split()            :
# segs    ^|   |  ^  |   |^                     :
# type    I       I       I                     :
#                                               :
# s\t j   J   K   L   M   N   O   P   Q   R     :
#     j >                                       :
#  i  0+|*1 | 2   3 | 4   5   6 | 7   8 | 9     :
#  v ---------------------------------------    :
# K   1 | 1 | 1-  2 | 3   4   5 | 6   7 | 8     :
# L   2 | 2 | 2  *1+| 2   3   4 | 5   6 | 7     :
#    ---------------------------------------    :
# M   3 | 3 | 3   2 | 1-  2   3 | 4   5 | 6     :
# O   4 | 4 | 4   3 | 2   2  *2+| 3   4 | 5     :
#    ---------------------------------------    :
# P   5 | 5 | 5   4 | 3   3   3 | 2-  3 | 4     :
# Q   6 | 6 | 6   5 | 4   4   4 | 3   2+| 3     :

sg1i1a = [[0, 2], [2, 4], [4, 6]]

def test_levenshtein_align_1i1a():
    assert levenshtein_align_fast(s1i1, t1i1, sg1i1a) == \
        [[1, 3], [3, 6], [6, 8]]
    assert levenshtein_align(s1i1, t1i1, sg1i1a) == \
        [[1, 3], [3, 6], [6, 8]]

def test_levenshtein_seg_1i1a():
    assert levenshtein_seg_fast(s1i1, t1i1, sg1i1a) == \
        [[2, 0], [2, 1], [2, 0]]
    assert levenshtein_seg(s1i1, t1i1, sg1i1a) == \
        [[2, 0], [2, 1], [2, 0]]

def test_levenshtein_seg_head_1i1a():
    assert levenshtein_seg_fast(s1i1, t1i1, sg1i1a, head=True) == \
        [[2, 1], [2, 1], [2, 0]]
    assert levenshtein_seg(s1i1, t1i1, sg1i1a, head=True) == \
        [[2, 1], [2, 1], [2, 0]]


# x1i1b                                         :
#    s = "  K L M   O P Q  ".split()            :
#    t = "J K L M N O P Q R".split()            :
# segs    ^|     |^| |   |^                     :
# type    I       I       I                     :
#                                               :
# s\t     J   K   L   M   N   O   P   Q   R     :
#     j >                                       :
#  i  0+|*1 | 2   3   4 | 5 | 6 | 7   8 | 9     :
#  v ---------------------------------------    :
# K   1 | 1 | 1-  2   3 | 4 | 5 | 6   7 | 8     :
# L   2 | 2 | 2   1   2 | 3 | 4 | 5   6 | 7     :
# M   3 | 3 | 3   2   1+|*2 | 3 | 4   5 | 6     :
#    ---------------------------------------    :
# O   4 | 4 | 4   3   2 | 2 |*2+| 3   4 | 5     :
#    ---------------------------------------    :
# P   5 | 5 | 5   4   3 | 3 | 3 | 2-  3 | 4     :
# Q   6 | 6 | 6   5   4 | 4 | 4 | 3   2+| 3     :

sg1i1b = [[0, 3], [3, 4], [4, 6]]

def test_levenshtein_align_1i1b():
    assert levenshtein_align_fast(s1i1, t1i1, sg1i1b) == \
        [[1, 4], [5, 6], [6, 8]]
    assert levenshtein_align(s1i1, t1i1, sg1i1b) == \
        [[1, 4], [5, 6], [6, 8]]

def test_levenshtein_seg_1i1b():
    assert levenshtein_seg_fast(s1i1, t1i1, sg1i1b) == \
        [[3, 0], [1, 0], [2, 0]]
    assert levenshtein_seg(s1i1, t1i1, sg1i1b) == \
        [[3, 0], [1, 0], [2, 0]]

def test_levenshtein_seg_head_1i1b():
    assert levenshtein_seg_fast(s1i1, t1i1, sg1i1b, head=True) == \
        [[3, 1], [1, 1], [2, 0]]
    assert levenshtein_seg(s1i1, t1i1, sg1i1b, head=True) == \
        [[3, 1], [1, 1], [2, 0]]


# x1i1c
#    s = "  K L M   O P Q  ".split()
#    t = "J K L M N O P Q R".split()
# segs    ^|     |^|     |^
# type    I       I       I
#                                               :
# s\t     J   K   L   M   N   O   P   Q   R     :
#     j >                                       :
#  i  0+|*1 | 2   3   4 | 5 | 6   7   8 | 9     :
#  v ---------------------------------------    :
# K   1 | 1 | 1-  2   3 | 4 | 5   6   7 | 8     :
# L   2 | 2 | 2   1   2 | 3 | 4   5   6 | 7     :
# M   3 | 3 | 3   2   1+|*2 | 3   4   5 | 6     :
#    ---------------------------------------    :
# O   4 | 4 | 4   3   2 | 2 | 2-  3   4 | 5     :
# P   5 | 5 | 5   4   3 | 3 | 3   2   3 | 4     :
# Q   6 | 6 | 6   5   4 | 4 | 4   3   2+| 3     :

sg1i1c = [[0, 3], [3, 6]]

def test_levenshtein_align_1i1c():
    assert levenshtein_align_fast(s1i1, t1i1, sg1i1c) == \
        [[1, 4], [5, 8]]
    assert levenshtein_align(s1i1, t1i1, sg1i1c) == \
        [[1, 4], [5, 8]]

def test_levenshtein_seg_1i1c():
    assert levenshtein_seg_fast(s1i1, t1i1, sg1i1c) == \
        [[3, 0], [3, 0]]
    assert levenshtein_seg(s1i1, t1i1, sg1i1c) == \
        [[3, 0], [3, 0]]

def test_levenshtein_seg_head_1i1c():
    assert levenshtein_seg_fast(s1i1, t1i1, sg1i1c, head=True) == \
        [[3, 1], [3, 1]]
    assert levenshtein_seg(s1i1, t1i1, sg1i1c, head=True) == \
        [[3, 1], [3, 1]]


#--------------------------------------------------------------------
# Test Levenshtein segment alignment and distance for x1sdi1
#--------------------------------------------------------------------

s1sdi1 = "  J K L   N O   Q".split()
t1sdi1 = "X J   L M N X P Q".split()

# x1sdi1a
#    s = "  J K L   N O   Q".split()
#    t = "X J   L M N X P Q".split()
# segs    ^|  ^  |^|  ^ ^  |
# type    I   D   I   S I
#
# s\t      X   J   L   M   N   X   P   Q
#      j >
#   i  0+|*1 | 2   3 | 4 | 5   6   7   8                d0 (i = 0)
#   v -----------------------------------
# J    1 | 1 | 1-  2 | 3 | 4   5   6   7    d1 (i = 0), d0 (i = 1)
# K    2 | 2 | 2   2 | 3 | 4   5   6   7    d1 (i = 1), d0 (i = 2)
# L    3 | 3 | 3   2+|*3 | 4   5   6   7    d1 (i = 2), d0 (i = 3)
#     -----------------------------------
# N    4 | 4 | 4   3 | 3 | 3-  4   5   6    d1 (i = 3), d0 (i = 4)
# O    5 | 5 | 5   4 | 4 | 4   4   5   6    d1 (i = 4), d0 (i = 5)
# Q    6 | 6 | 6   5 | 5 | 5   5   5   5+   d1 (i = 5)

sg1sdi1a = [[0, 3], [3, 6]]

def test_levenshtein_align_1sdi1a_all_normal():
    assert levenshtein_align_fast(s1sdi1, t1sdi1, sg1sdi1a) == \
        [[1, 3], [4, 8]]
    assert levenshtein_align(s1sdi1, t1sdi1, sg1sdi1a) == \
        [[1, 3], [4, 8]]

def test_levenshtein_seg_1sdi1a_all_normal():
    assert levenshtein_seg_fast(s1sdi1, t1sdi1, sg1sdi1a) == \
        [[3, 1], [3, 2]]
    assert levenshtein_seg(s1sdi1, t1sdi1, sg1sdi1a) == \
        [[3, 1], [3, 2]]

def test_levenshtein_seg_head_1sdi1a_all_normal():
    assert levenshtein_seg_fast(s1sdi1, t1sdi1, sg1sdi1a, head=True) == \
        [[3, 2], [3, 3]]
    assert levenshtein_seg(s1sdi1, t1sdi1, sg1sdi1a, head=True) == \
        [[3, 2], [3, 3]]


# x1sdi1b
#    s = "  J K L   N O   Q".split()
#    t = "X J   L M N X P Q".split()
# segs    ^| |^   ^  |^ ^  |
# type    I   D   I   S I
#
# s\t      X   J   L   M   N   X   P   Q
#      j >
#   i  0+|*1 | 2 | 3   4   5 | 6   7   8
#   v -----------------------------------
# J    1 | 1 |*1+| 2   3   4 | 5   6   7
#     -----------------------------------
# K    2 | 2 | 2 | 2-  3   4 | 5   6   7
# L    3 | 3 | 3 | 2   3   4 | 5   6   7
# N    4 | 4 | 4 | 3   3  *3+| 4   5   6
#     -----------------------------------
# O    5 | 5 | 5 | 4   4   4 | 4-  5   6
# Q    6 | 6 | 6 | 5   5   5 | 5   5   5+

sg1sdi1b = [[0, 1], [1, 4], [4, 6]]

def test_levenshtein_align_1sdi1b_with_diff():
    assert levenshtein_align_fast(s1sdi1, t1sdi1, sg1sdi1b) == \
        [[1, 2], [2, 5], [5, 8]]
    assert levenshtein_align(s1sdi1, t1sdi1, sg1sdi1b) == \
        [[1, 2], [2, 5], [6, 8]]
    # Note the difference ^

def test_levenshtein_seg_1sdi1b_with_diff():
    assert levenshtein_seg_fast(s1sdi1, t1sdi1, sg1sdi1b) == \
        [[1, 0], [3, 2], [2, 2]]
    assert levenshtein_seg(s1sdi1, t1sdi1, sg1sdi1b) == \
        [[1, 0], [3, 2], [2, 1]]
    # Note the difference    ^

def test_levenshtein_seg_head_1sdi1b_all_normal():
    assert levenshtein_seg_fast(s1sdi1, t1sdi1, sg1sdi1b, head=True) == \
        [[1, 1], [3, 2], [2, 2]]
    assert levenshtein_seg(s1sdi1, t1sdi1, sg1sdi1b, head=True) == \
        [[1, 1], [3, 2], [2, 2]]


# x1sdi1c
#    s = "  J K L   N O   Q".split()
#    t = "X J   L M N X P Q".split()
# segs    ^|  ^|  ^   ^|^| |
# type    I   D   I   S I
#
# s\t      X   J   L   M   N   X   P   Q
#      j >
#   i  0+|*1 | 2   3 | 4   5   6 | 7 | 8
#   v -----------------------------------
# J    1 | 1 | 1-  2 | 3   4   5 | 6 | 7
# K    2+| 2+|*2   2+| 3   4   5 | 6 | 7
#     -----------------------------------
# L    3 | 3 | 3 | 2-  3   4   5 | 6 | 7
# N    4 | 4 | 4 | 3   3   3   4 | 5 | 6
# O    5 | 5 | 5 | 4   4   4   4+|*5 | 6
#     -----------------------------------
# Q    6 | 6 | 6 | 5   5   5   5 | 5 | 5+

sg1sdi1c = [[0, 2], [2, 5], [5, 6]]

def test_levenshtein_align_1sdi1c_with_diff():
    assert levenshtein_align_fast(s1sdi1, t1sdi1, sg1sdi1c) == \
        [[1, 2], [2, 6], [7, 8]]
    assert levenshtein_align(s1sdi1, t1sdi1, sg1sdi1c) == \
        [[1, 2], [2, 6], [7, 8]]
        # [[1, 3], [2, 6], [7, 8]]
    #        ^ ^   Correction of upper boundary overshoot

def test_levenshtein_seg_1sdi1c_all_normal():
    assert levenshtein_seg_fast(s1sdi1, t1sdi1, sg1sdi1c) == \
        [[2, 1], [3, 2], [1, 0]]
    assert levenshtein_seg(s1sdi1, t1sdi1, sg1sdi1c) == \
        [[2, 1], [3, 2], [1, 0]]

def test_levenshtein_seg_head_1sdi1c_all_normal():
    assert levenshtein_seg_fast(s1sdi1, t1sdi1, sg1sdi1c, head=True) == \
        [[2, 2], [3, 2], [1, 1]]
    assert levenshtein_seg(s1sdi1, t1sdi1, sg1sdi1c, head=True) == \
        [[2, 2], [3, 2], [1, 1]]


#--------------------------------------------------------------------
# Test Levenshtein segment alignment and distance for x1sdi12
#--------------------------------------------------------------------

s1sdi2 = "J K L M N O   Q".split()
t1sdi2 = "J R L M   O P Q".split()

# x1sdi2a
#    s = "J K L M N O   Q".split()
#    t = "J R L M   O P Q".split()
# segs   |  ^  |  ^|  ^  |
# type      S     D   I
#
# s\t j   J   R   L   M   O   P   Q
#     j >
#  i *0+| 1   2   3 | 4   5 | 6   7
#  v -------------------------------
# J   1 | 0-  1   2 | 3   4 | 5   6
# K   2 | 1   1   2 | 3   4 | 5   6
# L   3 | 2   2  *1+| 2   3 | 4   5
#    -------------------------------
# M   4 | 3   3   2 | 1-  2 | 3   4
# N   5 | 4   4   3 |*2   2+| 3   4
#    -------------------------------
# O   6 | 5   5   4 | 3 | 2-  3   4
# Q   7 | 6   6   5 | 4 | 3   3   3+

sg1sdi2a = [[0, 3], [3, 5], [5, 7]]

def test_levenshtein_align_1sdi2a_with_diff():
    assert levenshtein_align_fast(s1sdi2, t1sdi2, sg1sdi2a) == \
        [[0, 3], [3, 4], [4, 7]]
    assert levenshtein_align(s1sdi2, t1sdi2, sg1sdi2a) == \
        [[0, 3], [3, 4], [4, 7]]
        # [[0, 3], [3, 5], [4, 7]]
    #                ^ ^   Correction of upper boundary overshoot

def test_levenshtein_seg_fast_1sdi2a_all_normal():
    assert levenshtein_seg_fast(s1sdi2, t1sdi2, sg1sdi2a) == \
        [[3, 1], [2, 1], [2, 1]]
    assert levenshtein_seg(s1sdi2, t1sdi2, sg1sdi2a) == \
        [[3, 1], [2, 1], [2, 1]]

def test_levenshtein_seg_fast_head_1sdi2a_all_normal():
    assert levenshtein_seg_fast(s1sdi2, t1sdi2, sg1sdi2a, head=True) == \
        [[3, 1], [2, 1], [2, 1]]
    assert levenshtein_seg(s1sdi2, t1sdi2, sg1sdi2a, head=True) == \
        [[3, 1], [2, 1], [2, 1]]


# x1sdi2b
#    s = "J K L M N O   Q".split()
#    t = "J R L M   O P Q".split()
# segs   |  ^|    ^  |^| |
# type      S     D   I
#
# s\t j   J   R   L   M   O   P   Q
#     j >
#  i *0+| 1   2 | 3   4   5 | 6 | 7
#  v -------------------------------
# J   1 | 0-  1 | 2   3   4 | 5 | 6
# K   2 | 1  *1+| 2   3   4 | 5 | 6
#    -------------------------------
# L   3 | 2   2 | 1-  2   3 | 4 | 5
# M   4 | 3   3 | 2   1   2 | 3 | 4
# N   5 | 4   4 | 3   2   2 | 3 | 4
# O   6 | 5   5 | 4   3   2+|*3 | 4
#    -------------------------------
# Q   7 | 6   6 | 5   4   3 | 3 | 3+

sg1sdi2b = [[0, 2], [2, 6], [6, 7]]

def test_levenshtein_align_1sdi2b_all_normal():
    assert levenshtein_align_fast(s1sdi2, t1sdi2, sg1sdi2b) == \
        [[0, 2], [2, 5], [6, 7]]
    assert levenshtein_align(s1sdi2, t1sdi2, sg1sdi2b) == \
        [[0, 2], [2, 5], [6, 7]]

def test_levenshtein_seg_fast_1sdi2b_all_normal():
    assert levenshtein_seg_fast(s1sdi2, t1sdi2, sg1sdi2b) == \
        [[2, 1], [4, 1], [1, 0]]
    assert levenshtein_seg(s1sdi2, t1sdi2, sg1sdi2b) == \
        [[2, 1], [4, 1], [1, 0]]

def test_levenshtein_seg_fast_head_1sdi2b_all_normal():
    assert levenshtein_seg_fast(s1sdi2, t1sdi2, sg1sdi2b, head=True) == \
        [[2, 1], [4, 1], [1, 1]]
    assert levenshtein_seg(s1sdi2, t1sdi2, sg1sdi2b, head=True) == \
        [[2, 1], [4, 1], [1, 1]]


#--------------------------------------------------------------------
# Test Levenshtein segment alignment and distance for x1sdi3
#--------------------------------------------------------------------

s1sdi3 = "  J K L   N O P Q".split()
t1sdi3 = "X J   L M N X   Q".split()

# x1sdi3a
#    s = "  J K L   N O P Q".split()
#    t = "X J   L M N X   Q".split()
# segs    ^|  ^  |^|  ^ ^  |
# type    I   D   I   S D
#
# s\t j   X   J   L   M   N   X   Q
#     j >
#  i  0+|*1 | 2   3 | 4 | 5   6   7
#  v -------------------------------
# J   1 | 1 | 1-  2 | 3 | 4   5   6
# K   2 | 2 | 2   2 | 3 | 4   5   6
# L   3 | 3 | 3   2+|*3 | 4   5   6
#    -------------------------------
# N   4 | 4 | 4   3 | 3 | 3-  4   5
# O   5 | 5 | 5   4 | 4 | 4   4   5
# P   6 | 6 | 6   5 | 5 | 5   5   5
# Q   7 | 7 | 7   6 | 6 | 6   6   5+

sg1sdi3a = [[0, 3], [3, 7]]

def test_levenshtein_align_1sdi3a_all_normal():
    assert levenshtein_align_fast(s1sdi3, t1sdi3, sg1sdi3a) == \
        [[1, 3], [4, 7]]
    assert levenshtein_align(s1sdi3, t1sdi3, sg1sdi3a) == \
        [[1, 3], [4, 7]]

def test_levenshtein_seg_fast_1sdi3a_all_normal():
    assert levenshtein_seg_fast(s1sdi3, t1sdi3, sg1sdi3a) == \
        [[3, 1], [4, 2]]
    assert levenshtein_seg(s1sdi3, t1sdi3, sg1sdi3a) == \
        [[3, 1], [4, 2]]

def test_levenshtein_seg_fast_head_1sdi3a_all_normal():
    assert levenshtein_seg_fast(s1sdi3, t1sdi3, sg1sdi3a, head=True) == \
        [[3, 2], [4, 3]]
    assert levenshtein_seg(s1sdi3, t1sdi3, sg1sdi3a, head=True) == \
        [[3, 2], [4, 3]]


# x1sdi3b
#    s = "  J K L   N O P Q".split()
#    t = "X J   L M N X   Q".split()
# segs    ^|  ^   ^  |^ ^  |
# type    I   D   I   S D
#
# s\t j   X   J   L   M   N   X   Q
#     j >
#  i  0+|*1 | 2   3   4   5 | 6   7
#  v -------------------------------
# J   1 | 1 | 1-  2   3   4 | 5   6
# K   2 | 2 | 2   2   3   4 | 5   6
# L   3 | 3 | 3   2   3   4 | 5   6
# N   4 | 4 | 4   3   3  *3+| 4   5
#    -------------------------------
# O   5 | 5 | 5   4   4   4 | 4-  5
# P   6 | 6 | 6   5   5   5 | 5   5
# Q   7 | 7 | 7   6   6   6 | 6   5+

sg1sdi3b = [[0, 4], [4, 7]]

def test_levenshtein_align_1sdi3b_all_normal():
    assert levenshtein_align_fast(s1sdi3, t1sdi3, sg1sdi3b) == \
        [[1, 5], [5, 7]]
    assert levenshtein_align(s1sdi3, t1sdi3, sg1sdi3b) == \
        [[1, 5], [5, 7]]

def test_levenshtein_seg_fast_1sdi3b_all_normal():
    assert levenshtein_seg_fast(s1sdi3, t1sdi3, sg1sdi3b) == \
        [[4, 2], [3, 2]]
    assert levenshtein_seg(s1sdi3, t1sdi3, sg1sdi3b) == \
        [[4, 2], [3, 2]]

def test_levenshtein_seg_fast_head_1sdi3b_all_normal():
    assert levenshtein_seg_fast(s1sdi3, t1sdi3, sg1sdi3b, head=True) == \
        [[4, 3], [3, 2]]
    assert levenshtein_seg(s1sdi3, t1sdi3, sg1sdi3b, head=True) == \
        [[4, 3], [3, 2]]


#--------------------------------------------------------------------
# Test Levenshtein segment alignment and distance for x1sdi4
#--------------------------------------------------------------------

s1sdi4 = "J K   M N O   Q R".split()
t1sdi4 = "K K L M   O P Q R".split()

# x1sdi4a
#    s = "J K   M N O   Q R".split()
#    t = "K K L M   O P Q R".split()
# segs   |^  |^|  ^  |^|   |
# type    S   S   D   I
#
# s\t     K   K   L   M   O   P   Q   R
#     j >
#  i  0+| 1   2 | 3 | 4   5 | 6 | 7   8
#  v -----------------------------------
# J   1 | 1-  2 | 3 | 4   5 | 6 | 7   8
# K   2 | 1   1+|*2 | 3   4 | 5 | 6   7
#    -----------------------------------
# M   3 | 2   2 | 2 | 2-  3 | 4 | 5   6
# N   4 | 3   3 | 3 | 3   3 | 4 | 5   6
# O   5 | 4   4 | 4 | 4   3+|*4 | 5   6
#    -----------------------------------
# Q   6 | 5   5 | 5 | 5   4 | 4 | 4-  5
# R   7 | 6   6 | 6 | 6   5 | 5 | 5   4+

sg1sdi4a = [[0, 2], [2, 5], [5, 7]]

def test_levenshtein_align_1sdi4a_all_normal():
    assert levenshtein_align_fast(s1sdi4, t1sdi4, sg1sdi4a) == \
        [[0, 2], [3, 5], [6, 8]]
    assert levenshtein_align(s1sdi4, t1sdi4, sg1sdi4a) == \
        [[0, 2], [3, 5], [6, 8]]

def test_levenshtein_seg_fast_1sdi4a_all_normal():
    assert levenshtein_seg_fast(s1sdi4, t1sdi4, sg1sdi4a) == \
        [[2, 1], [3, 1], [2, 0]]
    assert levenshtein_seg(s1sdi4, t1sdi4, sg1sdi4a) == \
        [[2, 1], [3, 1], [2, 0]]

def test_levenshtein_seg_fast_head_1sdi4a_all_normal():
    assert levenshtein_seg_fast(s1sdi4, t1sdi4, sg1sdi4a, head=True) == \
        [[2, 1], [3, 2], [2, 1]]
    assert levenshtein_seg(s1sdi4, t1sdi4, sg1sdi4a, head=True) == \
        [[2, 1], [3, 2], [2, 1]]


# x1sdi4b
#    s = "J K   M N O   Q R".split()
#    t = "K K L M   O P Q R".split()
# segs   |^   ^  |^|  ^    |
# type    S   S   D   I
#
# s\t     K   K   L   M   O   P   Q   R
#     j >
#  i  0+| 1   2   3   4 | 5 | 6   7   8
#  v -----------------------------------
# J   1 | 1-  2   3   4 | 5 | 6   7   8
# K   2 | 1   1   2   3 | 4 | 5   6   7
# M   3 | 2   2   2  *2+| 3 | 4   5   6
#    -----------------------------------
# N   4 | 3   3   3  *3 | 3+| 4   5   6
#    -----------------------------------
# O   5 | 4   4   4   4 | 3-  4   5   6
# Q   6 | 5   5   5   5 | 4   4   4   5
# R   7 | 6   6   6   6 | 5   5   5   4+

sg1sdi4b = [[0, 3], [3, 4], [4, 7]]

def test_levenshtein_align_1sdi4b_all_normal():
    assert levenshtein_align_fast(s1sdi4, t1sdi4, sg1sdi4b) == \
        [[0, 4], [4, 4], [4, 8]]
    assert levenshtein_align(s1sdi4, t1sdi4, sg1sdi4b) == \
        [[0, 4], [4, 4], [4, 8]]
        # [[0, 4], [4, 5], [4, 8]]
    #                ^ ^   Correction of upper boundary overshoot

def test_levenshtein_seg_fast_1sdi4b_all_normal():
    assert levenshtein_seg_fast(s1sdi4, t1sdi4, sg1sdi4b) == \
        [[3, 2], [1, 1], [3, 1]]
    assert levenshtein_seg(s1sdi4, t1sdi4, sg1sdi4b) == \
        [[3, 2], [1, 1], [3, 1]]

def test_levenshtein_seg_fast_head_1sdi4b_all_normal():
    assert levenshtein_seg_fast(s1sdi4, t1sdi4, sg1sdi4b, head=True) == \
        [[3, 2], [1, 1], [3, 1]]
    assert levenshtein_seg(s1sdi4, t1sdi4, sg1sdi4b, head=True) == \
        [[3, 2], [1, 1], [3, 1]]


#--------------------------------------------------------------------
# Test Levenshtein segment alignment and distance for x1sdi5
#--------------------------------------------------------------------

s1sdi5 = "  J K L   N O P Q".split()
t1sdi5 = "X Y K L M N   Z Q".split()

# x1sdi5a
#    s = "  J K L   N O P Q".split()
#    t = "X Y K L M N   Z Q".split()
# segs    ^|^    |^|  ^ ^  |
# type    I S     I   D S
#
# s\t j   X   Y   K   L   M   N   Z   Q
#     j >
#  i *0+| 1   2   3   4 | 5 | 6   7   8
#  v -----------------------------------
# J   1 | 1-  2   3   4 | 5 | 6   7   8
# K   2 | 2   2   2   3 | 4 | 5   6   7
# L   3 | 3   3   3   2+|*3 | 4   5   6
#    -----------------------------------
# N   4 | 4   4   4   3 | 3 | 3-  4   5
# O   5 | 5   5   5   4 | 4 | 4   4   5
# P   6 | 6   6   6   5 | 5 | 5   5   5
# Q   7 | 7   7   7   6 | 6 | 6   6   5+

sg1sdi5a = [[0, 3], [3, 7]]

def test_levenshtein_align_1sdi5a_all_normal():
    assert levenshtein_align_fast(s1sdi5, t1sdi5, sg1sdi5a) == \
        [[0, 4], [5, 8]]
    assert levenshtein_align(s1sdi5, t1sdi5, sg1sdi5a) == \
        [[1, 4], [5, 8]]
    #     ^      Note the difference

def test_levenshtein_seg_fast_1sdi5a_with_diff():
    assert levenshtein_seg_fast(s1sdi5, t1sdi5, sg1sdi5a) == \
        [[3, 2], [4, 2]]
    #        ^   Note the difference
    # This extra distance is caused by the min of d1 in Line J.
    assert levenshtein_seg(s1sdi5, t1sdi5, sg1sdi5a) == \
        [[3, 1], [4, 2]]
    #        ^   This is the correct distance.

def test_levenshtein_seg_fast_head_1sdi5a_all_normal():
    assert levenshtein_seg_fast(s1sdi5, t1sdi5, sg1sdi5a, head=True) == \
        [[3, 2], [4, 3]]
    assert levenshtein_seg(s1sdi5, t1sdi5, sg1sdi5a, head=True) == \
        [[3, 2], [4, 3]]


# x1sdi5b
#    s = "  J K L   N O P Q".split()
#    t = "X Y K L M N   Z Q".split()
# segs    ^ ^|   |^|  ^ ^  |
# type    I S     I   D S
#
# s\t     X   Y   K   L   M   N   Z   Q
#     j >
#  i *0+| 1   2 | 3   4 | 5 | 6   7   8
#  v -----------------------------------
# J   1 | 1+ *2 | 3   4 | 5 | 6   7   8
#    -----------------------------------
# K   2 | 2   2 | 2-  3 | 4 | 5   6   7
# L   3 | 3   3 | 3   2+|*3 | 4   5   6
#    -----------------------------------
# N   4 | 4   4 | 4   3 | 3 | 3-  4   5
# O   5 | 5   5 | 5   4 | 4 | 4   4   5
# P   6 | 6   6 | 6   5 | 5 | 5   5   5
# Q   7 | 7   7 | 7   6 | 6 | 6   6   5+

sg1sdi5b = [[1, 3], [3, 7]]

def test_levenshtein_align_1sdi5b_all_normal():
    assert levenshtein_align_fast(s1sdi5, t1sdi5, sg1sdi5b) == \
        [[2, 4], [5, 8]]
    assert levenshtein_align(s1sdi5, t1sdi5, sg1sdi5b) == \
        [[2, 4], [5, 8]]

def test_levenshtein_seg_fast_1sdi5b_all_normal():
    assert levenshtein_seg_fast(s1sdi5, t1sdi5, sg1sdi5b) == \
        [[2, 0], [4, 2]]
    assert levenshtein_seg(s1sdi5, t1sdi5, sg1sdi5b) == \
        [[2, 0], [4, 2]]

def test_levenshtein_seg_fast_head_1sdi5b_with_diff():
    assert levenshtein_seg_fast(s1sdi5, t1sdi5, sg1sdi5b, head=True) == \
        [[2, 1], [4, 3]]
    #        ^    Note the difference
    #     Caused by the leading error.
    assert levenshtein_seg(s1sdi5, t1sdi5, sg1sdi5b, head=True) == \
        [[2, 1], [4, 3]]
    #        ^    Note the difference
    #     Caused by the shifting.


#--------------------------------------------------------------------
# Test Levenshtein segment alignment and distance for x2s1
#--------------------------------------------------------------------

s2s1 = "J K L M N O P Q".split()
t2s1 = "X Y L M N O N K".split()

# x2s1a
#    s = "J K L M N O P Q".split()
#    t = "X Y L M N O N K".split()
# segs   |^ ^    |    ^ ^|
# type    S S         S S
#
# s\t     X   Y   L   M   N   O   N   K     :
#     j >                                   :
#  i *0+| 1   2   3   4 | 5   6   7   8     :
#  v -----------------------------------    :
# J   1 | 1-  2   3   4 | 5   6   7   8     :
# K   2 | 2   2   3   4 | 5   6   7   7     :
# L   3 | 3   3   2   3 | 4   5   6   7     :
# M   4 | 4   4   3  *2+| 3   4   5   6     :
#    -----------------------------------    :
# N   5 | 5   5   4   3 | 2-  3   4   5     :
# O   6 | 6   6   5   4 | 3   2   3   4     :
# P   7 | 7   7   6   5 | 4   3   3   4     :
# Q   8 | 8   8   7   6 | 5   4   4   4+    :

sg2s1a = [[0, 4], [4, 8]]

def test_levenshtein_align_2s1a():
    assert levenshtein_align_fast(s2s1, t2s1, sg2s1a) == \
        [[0, 4], [4, 8]]
    assert levenshtein_align(s2s1, t2s1, sg2s1a) == \
        [[0, 4], [4, 8]]

def test_levenshtein_seg_2s1a():
    assert levenshtein_seg_fast(s2s1, t2s1, sg2s1a) == \
        [[4, 2], [4, 2]]
    assert levenshtein_seg(s2s1, t2s1, sg2s1a) == \
        [[4, 2], [4, 2]]

def test_levenshtein_seg_head_2s1a():
    assert levenshtein_seg_fast(s2s1, t2s1, sg2s1a, head=True) == \
        [[4, 2], [4, 2]]
    assert levenshtein_seg(s2s1, t2s1, sg2s1a, head=True) == \
        [[4, 2], [4, 2]]


# x2s1b                                     :
#    s = "J K L M N O P Q".split()          :
#    t = "X Y L M N O N K".split()          :
# segs   |^ ^|        ^ ^|                  :
# type    S S         S S                   :
#                                           :
# s\t     X   Y   L   M   N   O   N   K     :
#     j >                                   :
#  i *0+| 1   2 | 3   4   5   6   7   8     :
#  v -----------------------------------    :
# J   1 | 1-  2 | 3   4   5   6   7   8     :
# K   2 | 2  *2+| 3   4   5   6   7   7     :
#    -----------------------------------    :
# L   3 | 3   3 | 2-  3   4   5   6   7     :
# M   4 | 4   4 | 3   2   3   4   5   6     :
# N   5 | 5   5 | 4   3   2   3   4   5     :
# O   6 | 6   6 | 5   4   3   2   3   4     :
# P   7 | 7   7 | 6   5   4   3   3   4     :
# Q   8 | 8   8 | 7   6   5   4   4   4+    :

sg2s1b = [[0, 2], [2, 8]]

def test_levenshtein_align_2s1b():
    assert levenshtein_align_fast(s2s1, t2s1, sg2s1b) == \
        [[0, 2], [2, 8]]
    assert levenshtein_align(s2s1, t2s1, sg2s1b) == \
        [[0, 2], [2, 8]]

def test_levenshtein_seg_2s1b():
    assert levenshtein_seg_fast(s2s1, t2s1, sg2s1b) == \
        [[2, 2], [6, 2]]
    assert levenshtein_seg(s2s1, t2s1, sg2s1b) == \
        [[2, 2], [6, 2]]

def test_levenshtein_seg_head_2s1b():
    assert levenshtein_seg_fast(s2s1, t2s1, sg2s1b, head=True) == \
        [[2, 2], [6, 2]]
    assert levenshtein_seg(s2s1, t2s1, sg2s1b, head=True) == \
        [[2, 2], [6, 2]]


#--------------------------------------------------------------------
# Test Levenshtein segment alignment and distance for x2d1
#--------------------------------------------------------------------

s2d1 = "J K L M N O P Q R".split()
t2d1 = "    L M     P Q  ".split()

# x2d1a                                 :
#    s = "J K L M N O P Q R".split()    :
#    t = "    L M     P Q  ".split()    :
# segs   |^ ^  |  ^ ^  |  ^|            :
# type    D D     D D     D             :
#                                       :
# s\t     L   M   P   Q                 :
#     j >                               :
#  i *0+| 1 | 2   3 | 4                 :
#  v -------------------                :
# J   1 | 1-| 2   3 | 4                 :
# J   2 | 2 | 2   3 | 4                 :
# L   3 |*2+| 3   3 | 4                 :
#    -------------------                :
# M   4 | 3 | 2-  3 | 4                 :
# N   5 | 4 | 3   3 | 4                 :
# O   6 | 5 | 4   4 | 4                 :
# P   7 | 6 | 5  *4+| 5                 :
#    -------------------                :
# Q   8 | 7 | 6   5 | 4-                :
# R   9 | 8 | 7   6 | 5+                :

sg2d1a = [[0, 3], [3, 7], [7, 9]]

def test_levenshtein_align_2d1a():
    assert levenshtein_align_fast(s2d1, t2d1, sg2d1a) == \
        [[0, 1], [1, 3], [3, 4]]
    assert levenshtein_align(s2d1, t2d1, sg2d1a) == \
        [[0, 1], [1, 3], [3, 4]]

def test_levenshtein_seg_2d1a():
    assert levenshtein_seg_fast(s2d1, t2d1, sg2d1a) == \
        [[3, 2], [4, 2], [2, 1]]
    assert levenshtein_seg(s2d1, t2d1, sg2d1a) == \
        [[3, 2], [4, 2], [2, 1]]

def test_levenshtein_seg_head_2d1a():
    assert levenshtein_seg_fast(s2d1, t2d1, sg2d1a, head=True) == \
        [[3, 2], [4, 2], [2, 1]]
    assert levenshtein_seg(s2d1, t2d1, sg2d1a, head=True) == \
        [[3, 2], [4, 2], [2, 1]]


# x2d1b                                 :
#    s = "J K L M N O P Q R".split()    :
#    t = "    L M     P Q  ".split()    :
# segs   |^ ^|    ^|^     ^|            :
# type    D D     D D     D             :
#                                       :
# s\t     L   M   P   Q                 :
#     j >                               :
#  i *0+| 1   2 | 3 | 4                 :
#  v -------------------                :
# J   1 | 1-  2 | 3 | 4                 :
# K  *2 | 2   2+| 3 | 4                 :
#    -------------------                :
# L   3 | 2-  3   3 | 4                 :
# M   4 | 3   2   3 | 4                 :
# N   5 | 4   3  *3+| 4                 :
#    -------------------                :
# O   6 | 5   4   4 | 4-                :
# P   7 | 6   5   4 | 5                 :
# Q   8 | 7   6   5 | 4-                :
# R   9 | 8   7   6 | 5+                :

sg2d1b = [[0, 2], [2, 5], [5, 9]]

def test_levenshtein_align_2d1b():
    assert levenshtein_align_fast(s2d1, t2d1, sg2d1b) == \
        [[0, 0], [0, 3], [3, 4]]
    assert levenshtein_align(s2d1, t2d1, sg2d1b) == \
        [[0, 0], [0, 3], [3, 4]]
    #                ^    ^  Note the difference from ideal case

def test_levenshtein_seg_2d1b():
    assert levenshtein_seg_fast(s2d1, t2d1, sg2d1b) == \
        [[2, 2], [3, 1], [4, 2]]
    assert levenshtein_seg(s2d1, t2d1, sg2d1b) == \
        [[2, 2], [3, 1], [4, 2]]

def test_levenshtein_seg_head_2d1b():
    assert levenshtein_seg_fast(s2d1, t2d1, sg2d1b, head=True) == \
        [[2, 2], [3, 1], [4, 2]]
    assert levenshtein_seg(s2d1, t2d1, sg2d1b, head=True) == \
        [[2, 2], [3, 1], [4, 2]]


#--------------------------------------------------------------------
# Test Levenshtein segment alignment and distance for x2d2
#--------------------------------------------------------------------

s2d2 = "J K L M N O P".split()
t2d2 = "    L M N    ".split()

# x2d2a
#    s = "J K L M N O P".split()
#    t = "    L M N    ".split()
# segs   |^ ^  |    ^ ^|
# type    D D       D D
#
# s\t     L   M   N
#     j >
#  i *0+| 1 | 2   3
#  v ---------------
# J   1 | 1-| 2   3
# K   2 | 2 | 2   3
# L   3 |*2+| 3   3
#    ---------------
# M   4 | 3 | 2-  3
# N   5 | 4 | 3   2
# O   6 | 5 | 4   3
# P   7 | 6 | 5   4+

sg2d2a = [[0, 3], [3, 7]]

def test_levenshtein_align_2d2a():
    assert levenshtein_align_fast(s2d2, t2d2, sg2d2a) == \
        [[0, 1], [1, 3]]
    assert levenshtein_align(s2d2, t2d2, sg2d2a) == \
        [[0, 1], [1, 3]]

def test_levenshtein_seg_fast_2d2a():
    assert levenshtein_seg_fast(s2d2, t2d2, sg2d2a) == \
        [[3, 2], [4, 2]]
    assert levenshtein_seg(s2d2, t2d2, sg2d2a) == \
        [[3, 2], [4, 2]]

def test_levenshtein_seg_fast_head_2d2a():
    assert levenshtein_seg_fast(s2d2, t2d2, sg2d2a, head=True) == \
        [[3, 2], [4, 2]]
    assert levenshtein_seg(s2d2, t2d2, sg2d2a, head=True) == \
        [[3, 2], [4, 2]]


#--------------------------------------------------------------------
# Test Levenshtein segment alignment and distance for x2i1
#--------------------------------------------------------------------

s2i1 = "    L M N     Q R".split()
t2i1 = "J K L M N O P Q R".split()

# x2i1a                                         :
#    s = "    L M N     Q R".split()            :
#    t = "J K L M N O P Q R".split()            :
# segs    ^ ^|     |^ ^|   |                    :
# type    I I       I I                         :
#                                               :
# s\t j   J   K   L   M   N   O   P   Q   R     :
#     j >                                       :
#  i *0+| 1   2   3   4   5 | 6   7   8   9     :
#  v ---------------------------------------    :
# L   1 | 1-  2   2   3   4 | 5   6   7   8     :
# M   2 | 2   2   3   2   3 | 4   5   6   7     :
# N   3 | 3   3   3   3  *2+| 3   4   5   6     :
#    ---------------------------------------    :
# Q   4 | 4   4   4   4   3 | 3-  4   4   5     :
# R   5 | 5   5   5   5   4 | 4   4   5   4+    :

sg2i1a = [[0, 3], [3, 5]]

def test_levenshtein_align_2i1a():
    assert levenshtein_align_fast(s2i1, t2i1, sg2i1a) == \
        [[0, 5], [5, 9]]
#       [[2, 5], [7, 9]]    # <- ideal result
    assert levenshtein_align(s2i1, t2i1, sg2i1a) == \
        [[2, 5], [7, 9]]

def test_levenshtein_seg_fast_2i1a():
    assert levenshtein_seg_fast(s2i1, t2i1, sg2i1a) == \
        [[3, 2], [2, 2]]
# Note       ^       ^
#     Tight WER fails due to shifted min d1
    assert levenshtein_seg(s2i1, t2i1, sg2i1a) == \
        [[3, 0], [2, 0]]

def test_levenshtein_seg_fast_head_2i1a():
    assert levenshtein_seg_fast(s2i1, t2i1, sg2i1a, head=True) == \
        [[3, 2], [2, 2]]
    assert levenshtein_seg(s2i1, t2i1, sg2i1a, head=True) == \
        [[3, 2], [2, 2]]


# x2i1b                                         :
#    s = "    L M N     Q R".split()            :
#    t = "J K L M N O P Q R".split()            :
# segs    ^ ^|   |  ^ ^    |                    :
# type    I I       I I                         :
#                                               :
# s\t j   J   K   L   M   N   O   P   Q   R     :
#     j >                                       :
#  i *0+| 1   2   3   4 | 5   6   7   8   9     :
#  v ---------------------------------------    :
# L   1 | 1-  2   2   3 | 4   5   6   7   8     :
# M   2 | 2   2   3  *2+| 3   4   5   6   7     :
#    ---------------------------------------    :
# N   3 | 3   3   3   3 | 2-  3   4   5   6     :
# Q   4 | 4   4   4   4 | 3   3   4   4   5     :
# R   5 | 5   5   5   5 | 4   4   4   5   4+    :

sg2i1b = [[0, 2], [2, 5]]

def test_levenshtein_align_2i1b():
    assert levenshtein_align_fast(s2i1, t2i1, sg2i1b) == \
        [[0, 4], [4, 9]]
#       [[2, 4], [4, 9]]    # <- ideal result
    assert levenshtein_align(s2i1, t2i1, sg2i1b) == \
        [[2, 4], [4, 9]]

def test_levenshtein_seg_fast_2i1b():
    assert levenshtein_seg_fast(s2i1, t2i1, sg2i1b) == \
        [[2, 2], [3, 2]]
# Note       ^       ^
#     Tight WER fails due to shifted min d1
    assert levenshtein_seg(s2i1, t2i1, sg2i1b) == \
        [[2, 0], [3, 2]]

def test_levenshtein_seg_fast_head_2i1b():
    assert levenshtein_seg_fast(s2i1, t2i1, sg2i1b, head=True) == \
        [[2, 2], [3, 2]]
    assert levenshtein_seg(s2i1, t2i1, sg2i1b, head=True) == \
        [[2, 2], [3, 2]]


#--------------------------------------------------------------------
# Test Levenshtein segment alignment and distance for x3s1
#--------------------------------------------------------------------

s3s1di1 = "  J K L M N O P Q R".split()
t3s1di1 = "K J   L M N N K J R".split()

# x3s1di1a
#    s = "  J K L M N O P Q R".split()
#    t = "K J   L M N N K J R".split()
# segs   |^   ^    |  ^ ^ ^  |
# type    I   D       S S S
#
# s\t     B   A   C   D   E   E   B   A   I     :
#     j >                                       :
#  i  0+|*1 | 2   3   4 | 5   6   7   8   9     :
#  v  --------------------------------------    :
# A   1 | 1 | 1-  2   3 | 4   5   6   7   8     :
# B   2 | 1 | 2   2   3 | 4   5   5   6   7     :
# C   3 | 2 | 2   2   3 | 4   5   6   6   7     :
# D   4 | 3 | 3   3  *2+| 3   4   5   6   7     :
#     --------------------------------------    :
# E   5 | 4 | 4   4   3 | 2-  3   4   5   6     :
# F   6 | 5 | 5   5   4 | 3   3   4   5   6     :
# G   7 | 6 | 6   6   5 | 4   4   4   5   6     :
# H   8 | 7 | 7   7   6 | 5   5   5   5   6     :
# I   9 | 8 | 8   8   7 | 6   6   6   6   5+    :

sg3s1di1a = [[0, 4], [4, 9]]

def test_levenshtein_align_3s1di1a():
    assert levenshtein_align_fast(s3s1di1, t3s1di1, sg3s1di1a) == \
        [[1, 4], [4, 9]]
    assert levenshtein_align(s3s1di1, t3s1di1, sg3s1di1a) == \
        [[1, 4], [4, 9]]

def test_levenshtein_seg_3s1di1a():
    assert levenshtein_seg_fast(s3s1di1, t3s1di1, sg3s1di1a) == \
        [[4, 1], [5, 3]]
    assert levenshtein_seg(s3s1di1, t3s1di1, sg3s1di1a) == \
        [[4, 1], [5, 3]]

def test_levenshtein_seg_head_3s1di1a():
    assert levenshtein_seg_fast(s3s1di1, t3s1di1, sg3s1di1a, head=True) == \
        [[4, 2], [5, 3]]
    assert levenshtein_seg(s3s1di1, t3s1di1, sg3s1di1a, head=True) == \
        [[4, 2], [5, 3]]


#--------------------------------------------------------------------
# Special tests without matchings
#--------------------------------------------------------------------

def test_levenshtein_seg_special_test1():
    """Test levenshtein_seg with the following lists."""
    s = "J  ".split()
    t = "K L".split()
# segs  |^|^
# type   S I
    segs = [[0, 1]]
    assert levenshtein_seg_fast(s, t, segs) == [[1, 1]]
    assert levenshtein_seg(s, t, segs) == [[1, 1]]
    assert levenshtein_seg_fast(s, t, segs, head=True) == [[1, 1]]
    assert levenshtein_seg(s, t, segs, head=True) == [[1, 2]]


def test_levenshtein_seg_special_test2():
    """Test levenshtein_seg with the following lists."""
    s = "J K".split()
    t = "L  ".split()
# segs  |^|^
# type   S D
    segs = [[0, 1]]
    assert levenshtein_seg_fast(s, t, segs) == [[1, 1]]
    assert levenshtein_seg(s, t, segs) == [[1, 1]]
    assert levenshtein_seg_fast(s, t, segs, head=True) == [[1, 1]]
    assert levenshtein_seg(s, t, segs, head=True) == [[1, 1]]


def test_levenshtein_seg_head_st3():
    """Test levenshtein_seg with the following lists."""
    s = "J K  ".split()
    t = "L M N".split()
# segs   ^|^|^
# type   S S I
    segs = [[1, 2]]
    assert levenshtein_seg_fast(s, t, segs) == [[1, 1]]
    assert levenshtein_seg(s, t, segs) == [[1, 1]]
    assert levenshtein_seg_fast(s, t, segs, head=True) == [[1, 1]]
    assert levenshtein_seg(s, t, segs, head=True) == [[1, 2]]
