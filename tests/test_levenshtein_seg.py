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
# 1. char s/t---source/target or ref/hyp
# 2. num  n (1/2/3)---Up to n consecutive
#        substitutions/deletions/insertions
# 3. char s/d/i---substitution/deletion/insertion
# 4. num  m---case number for unique s and t sequences
# 5. char a/b/c---case number for the same s and t sequences

###############################################################
# Notations in the distance table:
# ^ = substitution/deletion/insertion.
# | = boundary of segments.
# + = minimum value(s) of d1 for a given i corresponding to the upper
#       boundary of a segment before swapping d0 and d1.
# - = minimum value of d1 with the max index for a given i corresponding
#       to the lower boundary of a segment before swapping d0 and d1.
# * = (before the number) base value used for no-head seg distance.


############################################
# x1sdi
#    s = "  J K L   N O   Q".split()
#    t = "X J   L M N X P Q".split()
# segs    ^|  ^  |^|  ^ ^  |
# type    I   D   I   S I
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
# Q    6 | 6 | 6   5 | 5 | 5+  5+  5+  5+   d1 (i = 5)

s1sdi = "  J K L   N O   Q".split()
t1sdi = "X J   L M N X P Q".split()

def test_levenshtein_align_1sdi():
    """Test levenshtein_align_fast with the above lists."""
    segs = [[0, 3], [3, 6]]
    assert levenshtein_align_fast(s1sdi, t1sdi, segs) == \
        [[1, 3], [4, 8]]
    assert levenshtein_align(s1sdi, t1sdi, segs) == \
        [[1, 3], [4, 8]]

def test_levenshtein_seg_1sdi():
    """Test levenshtein_seg with the above lists."""
    segs = [[0, 3], [3, 6]]
    assert levenshtein_seg_fast(s1sdi, t1sdi, segs) == \
        [[3, 1], [3, 2]]
    assert levenshtein_seg(s1sdi, t1sdi, segs) == \
        [[3, 1], [3, 2]]

def test_levenshtein_seg_head_1sdi():
    """Test levenshtein_seg with the above lists."""
    segs = [[0, 3], [3, 6]]
    assert levenshtein_seg_fast(s1sdi, t1sdi, segs, head=True) == \
        [[3, 2], [3, 3]]
    assert levenshtein_seg(s1sdi, t1sdi, segs, head=True) == \
        [[3, 2], [3, 3]]


############################################
# x1s1a
#    s = "J K L M N O P Q R".split()
#    t = "Z K L M Y O P Q X".split()
# segs   |^    |  ^  |    ^|
# type    S       S       S
#                                         i = 0   1   2   3   4   5   6   7   8
# s\t j   Z   K   L   M   Y   O   P   Q   X   :   :   :   :   :   :   :   :   :
# i  *0+| 1   2   3 | 4   5   6 | 7   8   9   d0  :   :   :   :   :   :   :   :
#    ---------------------------------------  :   :   :   :   :   :   :   :   :
# J   1 | 1-  2   3 | 4   5   6 | 7   8   9   d1  d0  :   :   :   :   :   :   :
# K   2 | 2   1   2 | 3   4   5 | 6   7   8       d1  d0  :   :   :   :   :   :
# L   3 | 3   2  *1+| 2   3   4 | 5   6   7           d1  d0  :   :   :   :   :
#    ---------------------------------------              :   :   :   :   :   :
# M   4 | 4   3   2 | 1-  2   3 | 4   5   6               d1  d0  :   :   :   :
# N   5 | 5   4   3 | 2   2   3 | 4   5   6                   d1  d0  :   :   :
# O   6 | 6   5   4 | 3   3  *2+| 3   4   5                       d1  d0  :   :
#    ---------------------------------------                          :   :   :
# P   7 | 7   6   5 | 4   4   3 | 2-  3   4                           d1  d0  :
# Q   8 | 8   7   6 | 5   5   4 | 3   2   3                               d1  d0
# R   9 | 9   8   7 | 6   6   5 | 4   3+  3+                                  d1

s1s1 = "J K L M N O P Q R".split()
t1s1 = "Z K L M Y O P Q X".split()

def test_levenshtein_align_fast_1s1a():
    """Test levenshtein_align_fast with the above lists."""
    segs = [[0, 3], [3, 6], [6, 9]]
    assert levenshtein_align_fast(s1s1, t1s1, segs) == \
        [[0, 3], [3, 6], [6, 9]]
    assert levenshtein_align(s1s1, t1s1, segs) == \
        [[0, 3], [3, 6], [6, 9]]

def test_levenshtein_seg_fast_1s1a():
    """Test levenshtein_seg with the above lists."""
    segs = [[0, 3], [3, 6], [6, 9]]
    assert levenshtein_seg_fast(s1s1, t1s1, segs) == \
        [[3, 1], [3, 1], [3, 1]]
    assert levenshtein_seg(s1s1, t1s1, segs) == \
        [[3, 1], [3, 1], [3, 1]]

def test_levenshtein_seg_fast_head_1s1a():
    """Test levenshtein_seg with the above lists."""
    segs = [[0, 3], [3, 6], [6, 9]]
    assert levenshtein_seg_fast(s1s1, t1s1, segs, head=True) == \
        [[3, 1], [3, 1], [3, 1]]
    assert levenshtein_seg(s1s1, t1s1, segs, head=True) == \
        [[3, 1], [3, 1], [3, 1]]


############################################
# x1s1b
#    s = "J K L M N O P Q R".split()
#    t = "Z K L M Y O P Q X".split()
# segs   |^      |^       ^|
# type    S       S       S
#                                         i = 0   1   2   3   4   5   6   7   8
# s\t j   Z   K   L   M   Y   O   P   Q   X   :   :   :   :   :   :   :   :   :
# i  *0+| 1   2   3   4 | 5   6   7   8   9   d0  :   :   :   :   :   :   :   :
#    ---------------------------------------  :   :   :   :   :   :   :   :   :
# J   1 | 1-  2   3   4 | 5   6   7   8   9   d1  d0  :   :   :   :   :   :   :
# K   2 | 2   1   2   3 | 4   5   6   7   8       d1  d0  :   :   :   :   :   :
# L   3 | 3   2   1   2 | 3   4   5   6   7           d1  d0  :   :   :   :   :
# M   4 | 4   3   2  *1+| 2   3   4   5   6               d1  d0  :   :   :   :
#    ---------------------------------------              :   :   :   :   :   :
# N   5 | 5   4   3   2 | 2-  3   4   5   6                   d1  d0  :   :   :
# O   6 | 6   5   4   3 | 3   2   3   4   5                       d1  d0  :   :
# P   7 | 7   6   5   4 | 4   3   2   3   4                           d1  d0  :
# Q   8 | 8   7   6   5 | 5   4   3   2   3                               d1  d0
# R   9 | 9   8   7   6 | 6   5   4   3+  3+                                  d1

def test_levenshtein_align_fast_1s1b():
    """Test levenshtein_align_fast with the above lists."""
    segs = [[0, 4], [4, 9]]
    assert levenshtein_align_fast(s1s1, t1s1, segs) == \
        [[0, 4], [4, 9]]
    assert levenshtein_align(s1s1, t1s1, segs) == \
        [[0, 4], [4, 9]]

def test_levenshtein_seg_fast_1s1b():
    """Test levenshtein_seg with the above lists."""
    segs = [[0, 4], [4, 9]]
    assert levenshtein_seg_fast(s1s1, t1s1, segs) == \
        [[4, 1], [5, 2]]
    assert levenshtein_seg(s1s1, t1s1, segs) == \
        [[4, 1], [5, 2]]

def test_levenshtein_seg_fast_head_1s1b():
    """Test levenshtein_seg with the above lists."""
    segs = [[0, 4], [4, 9]]
    assert levenshtein_seg_fast(s1s1, t1s1, segs, head=True) == \
        [[4, 1], [5, 2]]
    assert levenshtein_seg(s1s1, t1s1, segs, head=True) == \
        [[4, 1], [5, 2]]


############################################
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

s1s2 = "J K J M N K P Q J".split()
t1s2 = "J K L M N O P Q R".split()

def test_levenshtein_align_fast_1s2():
    """Test levenshtein_align_fast with the above lists."""
    segs = [[0, 3], [3, 6], [6, 9]]
    assert levenshtein_align_fast(s1s2, t1s2, segs) == \
        [[0, 3], [3, 6], [6, 9]]
    assert levenshtein_align(s1s2, t1s2, segs) == \
        [[0, 3], [3, 6], [6, 9]]

def test_levenshtein_seg_fast_1s2():
    """Test levenshtein_seg with the above lists."""
    segs = [[0, 3], [3, 6], [6, 9]]
    assert levenshtein_seg_fast(s1s2, t1s2, segs) == \
        [[3, 1], [3, 1], [3, 1]]
    assert levenshtein_seg(s1s2, t1s2, segs) == \
        [[3, 1], [3, 1], [3, 1]]

def test_levenshtein_seg_fast_head_1s2():
    """Test levenshtein_seg with the above lists."""
    segs = [[0, 3], [3, 6], [6, 9]]
    assert levenshtein_seg_fast(s1s2, t1s2, segs, head=True) == \
        [[3, 1], [3, 1], [3, 1]]
    assert levenshtein_seg(s1s2, t1s2, segs, head=True) == \
        [[3, 1], [3, 1], [3, 1]]


############################################
# x1d1a
#    s = "J K L M N O P Q R".split()
#    t = "  K L M   O P Q  ".split()
# segs   |^    |  ^  |    ^|
# type    D       D       D
#
# s\t j   K   L   M   O   P   Q
# i  *0+| 1   2 | 3   4 | 5   6
#    ---------------------------
# J   1 | 1-  2 | 3   4 | 5   6
# K   2 | 1   2 | 3   4 | 5   6
# L   3 | 2  *1+| 2   3 | 4   5
#    ---------------------------
# M   4 | 3   2 | 1-  2 | 3   4
# N   5 | 4   3 | 2   2 | 3   4
# O   6 | 5   4 | 3  *2+| 3   4
#    ---------------------------
# P   7 | 6   5 | 4   3 | 2-  3
# Q   8 | 7   6 | 5   4 | 3   2
# R   9 | 8   7 | 6   5 | 4   3+

s1d1 = "J K L M N O P Q R".split()
t1d1 = "  K L M   O P Q  ".split()

def test_levenshtein_align_fast_1d1a():
    """Test levenshtein_align_fast with the above lists."""
    segs = [[0, 3], [3, 6], [6, 9]]
    assert levenshtein_align_fast(s1d1, t1d1, segs) == \
        [[0, 2], [2, 4], [4, 6]]
    assert levenshtein_align(s1d1, t1d1, segs) == \
        [[0, 2], [2, 4], [4, 6]]

def test_levenshtein_seg_fast_1d1a():
    """Test levenshtein_seg with the above lists."""
    segs = [[0, 3], [3, 6], [6, 9]]
    assert levenshtein_seg_fast(s1d1, t1d1, segs) == \
        [[3, 1], [3, 1], [3, 1]]
    assert levenshtein_seg(s1d1, t1d1, segs) == \
        [[3, 1], [3, 1], [3, 1]]

def test_levenshtein_seg_fast_head_1d1a():
    """Test levenshtein_seg with the above lists."""
    segs = [[0, 3], [3, 6], [6, 9]]
    assert levenshtein_seg_fast(s1d1, t1d1, segs, head=True) == \
        [[3, 1], [3, 1], [3, 1]]
    assert levenshtein_seg(s1d1, t1d1, segs, head=True) == \
        [[3, 1], [3, 1], [3, 1]]


############################################
# x1d1b
#    s = "J K L M N O P Q R".split()
#    t = "  K L M   O P Q  ".split()
# segs   |^      |^       ^|
# type    D       D       D
#
# s\t j   K   L   M   O   P   Q
# i  *0+| 1   2   3 | 4   5   6
#    ---------------------------
# J   1 | 1-  2   3 | 4   5   6
# K   2 | 1   2   3 | 4   5   6
# L   3 | 2   1   2 | 3   4   5
# M   4 | 3   2  *1+| 2   3   4
#    ---------------------------
# N   5 | 4   3   2 | 2-  3   4
# O   6 | 5   4   3 | 2   3   4
# P   7 | 6   5   4 | 3   2   3
# Q   8 | 7   6   5 | 4   3   2
# R   9 | 8   7   6 | 5   4   3+

def test_levenshtein_align_fast_1d1b():
    """Test levenshtein_align_fast with the above lists."""
    segs = [[0, 4], [4, 9]]
    assert levenshtein_align_fast(s1d1, t1d1, segs) == \
        [[0, 3], [3, 6]]
    assert levenshtein_align(s1d1, t1d1, segs) == \
        [[0, 3], [3, 6]]

def test_levenshtein_seg_fast_1d1b():
    """Test levenshtein_seg with the above lists."""
    segs = [[0, 4], [4, 9]]
    assert levenshtein_seg_fast(s1s1, t1s1, segs) == \
        [[4, 1], [5, 2]]
    assert levenshtein_seg(s1s1, t1s1, segs) == \
        [[4, 1], [5, 2]]

def test_levenshtein_seg_fast_head_1d1b():
    """Test levenshtein_seg with the above lists."""
    segs = [[0, 4], [4, 9]]
    assert levenshtein_seg_fast(s1d1, t1d1, segs, head=True) == \
        [[4, 1], [5, 2]]
    assert levenshtein_seg(s1d1, t1d1, segs, head=True) == \
        [[4, 1], [5, 2]]


############################################
# x1i1a
#    s = "  K L M   O P Q  ".split()
#    t = "J K L M N O P Q R".split()
# segs    ^|   |  ^  |   |^
# type    I       I       I
#                                         i = 0   1   2   3   4   5
# s\t j   J   K   L   M   N   O   P   Q   R   :   :   :   :   :   :
# i   0+|*1 | 2   3 | 4   5   6 | 7   8 | 9   d0  :   :   :   :   :
#    ---------------------------------------  :   :   :   :   :   :
# K   1 | 1 | 1-  2 | 3   4   5 | 6   7 | 8   d1  d0  :   :   :   :
# L   2 | 2 | 2  *1+| 2   3   4 | 5   6 | 7       d1  d0  :   :   :
#    ---------------------------------------          :   :   :   :
# M   3 | 3 | 3   2 | 1-  2   3 | 4   5 | 6           d1  d0  :   :
# O   4 | 4 | 4   3 | 2   2+ *2+| 3   4 | 5               d1  d0  :
#    ---------------------------------------                  :   :
# P   5 | 5 | 5   4 | 3   3   3 | 2-  3 | 4                   d1  d0
# Q   6 | 6 | 6   5 | 4   4   4 | 3   2+| 3                       d1

s1i1 = "  K L M   O P Q  ".split()
t1i1 = "J K L M N O P Q R".split()

def test_levenshtein_align_1i1a():
    """Test levenshtein_align_fast with the above lists."""
    segs = [[0, 2], [2, 4], [4, 6]]
    assert levenshtein_align_fast(s1i1, t1i1, segs) == \
        [[1, 3], [3, 6], [6, 8]]
    assert levenshtein_align(s1i1, t1i1, segs) == \
        [[1, 3], [3, 6], [6, 8]]

def test_levenshtein_seg_fast_1i1a():
    """Test levenshtein_seg with the above lists."""
    segs = [[0, 2], [2, 4], [4, 6]]
    assert levenshtein_seg_fast(s1i1, t1i1, segs) == \
        [[2, 0], [2, 1], [2, 0]]
    assert levenshtein_seg(s1i1, t1i1, segs) == \
        [[2, 0], [2, 1], [2, 0]]

def test_levenshtein_seg_fast_head_1i1a():
    """Test levenshtein_seg with the above lists."""
    segs = [[0, 2], [2, 4], [4, 6]]
    assert levenshtein_seg_fast(s1i1, t1i1, segs, head=True) == \
        [[2, 1], [2, 1], [2, 0]]
    assert levenshtein_seg(s1i1, t1i1, segs, head=True) == \
        [[2, 1], [2, 1], [2, 0]]


############################################
# x1i1b
#    s = "  K L M   O P Q  ".split()
#    t = "J K L M N O P Q R".split()
# segs    ^|     |^|     |^
# type    I       I       I
#                                         i = 0   1   2   3   4   5
# s\t j   J   K   L   M   N   O   P   Q   R   :   :   :   :   :   :
# i   0+|*1 | 2   3   4 | 5 | 6   7   8 | 9   d0  :   :   :   :   :
#    ---------------------------------------  :   :   :   :   :   :
# K   1 | 1 | 1-  2   3 | 4 | 5   6   7 | 8   d1  d0  :   :   :   :
# L   2 | 2 | 2   1   2 | 3 | 4   5   6 | 7       d1  d0  :   :   :
# M   3 | 3 | 3   2   1+|*2 | 3   4   5 | 6           d1  d0  :   :
#    ---------------------------------------          :   :   :   :
# O   4 | 4 | 4   3   2 | 2 | 2-  3   4 | 5               d1  d0  :
# P   5 | 5 | 5   4   3 | 3 | 3   2   3 | 4                   d1  d0
# Q   6 | 6 | 6   5   4 | 4 | 4   3   2+| 3                       d1

s1i1 = "  K L M   O P Q  ".split()
t1i1 = "J K L M N O P Q R".split()

def test_levenshtein_align_1i1b():
    """Test levenshtein_align functions with the above lists."""
    segs = [[0, 3], [3, 6]]
    assert levenshtein_align_fast(s1i1, t1i1, segs) == \
        [[1, 4], [5, 8]]
    assert levenshtein_align(s1i1, t1i1, segs) == \
        [[1, 4], [5, 8]]

def test_levenshtein_seg_fast_1i1b():
    """Test levenshtein_seg with the above lists."""
    segs = [[0, 3], [3, 6]]
    assert levenshtein_seg_fast(s1i1, t1i1, segs) == \
        [[3, 0], [3, 0]]
    assert levenshtein_seg(s1i1, t1i1, segs) == \
        [[3, 0], [3, 0]]

def test_levenshtein_seg_fast_head_1i1b():
    """Test levenshtein_seg with the above lists."""
    segs = [[0, 3], [3, 6]]
    assert levenshtein_seg_fast(s1i1, t1i1, segs, head=True) == \
        [[3, 1], [3, 1]]
    assert levenshtein_seg(s1i1, t1i1, segs, head=True) == \
        [[3, 1], [3, 1]]


############################################
# x1sdi1a
#    s = "J K L M N O   Q".split()
#    t = "J R L M   O P Q".split()
# segs   |  ^  |  ^|  ^  |
# type      S     D   I
#                                 i = 0   1   2   3   4   5   6
# s\t j   J   R   L   M   O   P   Q   :   :   :   :   :   :   :
# i  *0+| 1   2   3 | 4 | 5   6   7   d0  :   :   :   :   :   :
#    -------------------------------  :   :   :   :   :   :   :
# J   1 | 0-  1   2 | 3 | 4   5   6   d1  d0  :   :   :   :   :
# K   2 | 1   1   2 | 3 | 4   5   6       d1  d0  :   :   :   :
# L   3 | 2   2   1+| 2 | 3   4   5           d1  d0  :   :   :
#    -------------------------------
# M   4 | 3   3   2 | 1-| 2   3   4               d1  d0  :   :
# N   5 | 4   4   3 |*2+| 2+  3   4                   d1  d0  :
#    -------------------------------
# O   6 | 5   5   4 | 3 | 2-  3   4                       d1  d0
# Q   7 | 6   6   5 | 4 | 3   3+  3+                          d1

s1sdi1 = "J K L M N O   Q".split()
t1sdi1 = "J R L M   O P Q".split()

def test_levenshtein_align_1sdi1():
    """Test levenshtein_align functions with the above lists."""
    segs = [[0, 3], [3, 5], [5, 7]]
    assert levenshtein_align_fast(s1sdi1, t1sdi1, segs) == \
        [[0, 3], [3, 5], [4, 7]]
    # Note           ^ this should be 4; caused by training source
    assert levenshtein_align(s1sdi1, t1sdi1, segs) == \
        [[0, 3], [3, 5], [4, 7]]

def test_levenshtein_seg_fast_1sdi1():
    """Test levenshtein_seg with the above lists."""
    segs = [[0, 3], [3, 5], [5, 7]]
    assert levenshtein_seg_fast(s1sdi1, t1sdi1, segs) == \
        [[3, 1], [2, 1], [2, 1]]
    assert levenshtein_seg(s1sdi1, t1sdi1, segs) == \
        [[3, 1], [2, 1], [2, 1]]

def test_levenshtein_seg_fast_head_1sdi1():
    """Test levenshtein_seg with the above lists."""
    segs = [[0, 3], [3, 5], [5, 7]]
    assert levenshtein_seg_fast(s1sdi1, t1sdi1, segs, head=True) == \
        [[3, 1], [2, 1], [2, 1]]
    assert levenshtein_seg(s1sdi1, t1sdi1, segs, head=True) == \
        [[3, 1], [2, 1], [2, 1]]


############################################
# x1sdi2
#    s = "  J K L   N O P Q".split()
#    t = "X J   L M N X   Q".split()
# segs    ^|  ^  |^|  ^ ^  |
# type    I   D   I   S D
#                                 i = 0   1   2   3   4   5   6
# s\t j   X   J   L   M   N   X   Q   :   :   :   :   :   :   :
# i   0+|*1 | 2   3 | 4 | 5   6   7   d0  :   :   :   :   :   :
#    -------------------------------  :   :   :   :   :   :   :
# J   1 | 1 | 1-  2 | 3 | 4   5   6   d1  d0  :   :   :   :   :
# K   2 | 2 | 2   2 | 3 | 4   5   6       d1  d0  :   :   :   :
# L   3 | 3 | 3   2+|*3 | 4   5   6           d1  d0  :   :   :
#    -------------------------------          :   :   :   :   :
# N   4 | 4 | 4   3 | 3 | 3-  4   5               d1  d0  :   :
# O   5 | 5 | 5   4 | 4 | 4   4   5                   d1  d0  :
# P   6 | 6 | 6   5 | 5 | 5   5   5                       d1  d0
# Q   7 | 7 | 7   6 | 6 | 6   6   5+                          d1

s1sdi2 = "  J K L   N O P Q".split()
t1sdi2 = "X J   L M N X   Q".split()

def test_levenshtein_seg_fast_1sdi2():
    """Test levenshtein_seg with the above lists."""
    segs = [[0, 3], [3, 7]]
    assert levenshtein_seg_fast(s1sdi2, t1sdi2, segs) == \
        [[3, 1], [4, 2]]
    assert levenshtein_seg(s1sdi2, t1sdi2, segs) == \
        [[3, 1], [4, 2]]

def test_levenshtein_seg_fast_head_1sdi2():
    """Test levenshtein_seg with the above lists."""
    segs = [[0, 3], [3, 7]]
    assert levenshtein_seg_fast(s1sdi2, t1sdi2, segs, head=True) == \
        [[3, 2], [4, 3]]
    assert levenshtein_seg(s1sdi2, t1sdi2, segs, head=True) == \
        [[3, 2], [4, 3]]


############################################
# x1sdi3
#    s = "J K   M N O   Q R".split()
#    t = "K K L M   O P Q R".split()
# segs   |^  |^|  ^  |^|   |
# type    S   S   D   I
#                                     i = 0   1   2   3   4   5   6
# s\t j   K   K   L   M   O   P   Q   R   :   :   :   :   :   :   :
# i   0+| 1   2 | 3 | 4   5 | 6 | 7   8   d0  :   :   :   :   :   :
#    -----------------------------------  :   :   :   :   :   :   :
# J   1 | 1-  2 | 3 | 4   5 | 6 | 7   8   d1  d0  :   :   :   :   :
# K   2 | 1+  1+|*2 | 3   4 | 5 | 6   7       d1  d0  :   :   :   :
#    -----------------------------------          :   :   :   :   :
# M   3 | 2   2 | 2 | 2-  3 | 4 | 5   6           d1  d0  :   :   :
# N   4 | 3   3 | 3 | 3   3 | 4 | 5   6               d1  d0  :   :
# O   5 | 4   4 | 4 | 4   3+|*4 | 5   6                   d1  d0  :
#    -----------------------------------                      :   :
# Q   6 | 5   5 | 5 | 5   4 | 4 | 4-  5                       d1  d0
# R   7 | 6   6 | 6 | 6   5 | 5 | 5   4+                          d1

s1sdi3 = "J K   M N O   Q R".split()
t1sdi3 = "K K L M   O P Q R".split()

def test_levenshtein_seg_fast_1sdi3():
    """Test levenshtein_seg with the above lists."""
    segs = [[0, 2], [2, 5], [5, 7]]
    assert levenshtein_seg_fast(s1sdi3, t1sdi3, segs) == \
        [[2, 1], [3, 1], [2, 0]]
    assert levenshtein_seg(s1sdi3, t1sdi3, segs) == \
        [[2, 1], [3, 1], [2, 0]]

def test_levenshtein_seg_fast_head_1sdi3():
    """Test levenshtein_seg with the above lists."""
    segs = [[0, 2], [2, 5], [5, 7]]
    assert levenshtein_seg_fast(s1sdi3, t1sdi3, segs, head=True) == \
        [[2, 1], [3, 2], [2, 1]]
    assert levenshtein_seg(s1sdi3, t1sdi3, segs, head=True) == \
        [[2, 1], [3, 2], [2, 1]]


############################################
# x1sdi4a
#    s = "  J K L   N O P Q".split()
#    t = "X Y K L M N   Z Q".split()
# segs    ^|^    |^|  ^ ^  |
# type    I S     I   D S
#
# s\t j   X   Y   K   L   M   N   Z   Q
# i  *0+| 1   2   3   4 | 5 | 6   7   8
#    -----------------------------------
# J   1 | 1-  2   3   4 | 5 | 6   7   8
# K   2 | 2   2   2   3 | 4 | 5   6   7
# L   3 | 3   3   3   2+|*3 | 4   5   6
#    -----------------------------------
# N   4 | 4   4   4   3 | 3 | 3-  4   5
# O   5 | 5   5   5   4 | 4 | 4   4   5
# P   6 | 6   6   6   5 | 5 | 5   5   5
# Q   7 | 7   7   7   6 | 6 | 6   6   5+

s1sdi4 = "  J K L   N O P Q".split()
t1sdi4 = "X Y K L M N   Z Q".split()

def test_levenshtein_seg_fast_1sdi4a():
    """Test levenshtein_seg with the above lists."""
    segs = [[0, 3], [3, 7]]
    assert levenshtein_seg_fast(s1sdi4, t1sdi4, segs) == \
        [[3, 2], [4, 2]]
# Note       ^
#     This extra distance is caused by the min of d1 in Line A
    assert levenshtein_seg(s1sdi4, t1sdi4, segs) == \
        [[3, 1], [4, 2]]
# Note       ^
#     This is the correct distance.

def test_levenshtein_seg_fast_head_1sdi4a():
    """Test levenshtein_seg with the above lists."""
    segs = [[0, 3], [3, 7]]
    assert levenshtein_seg_fast(s1sdi4, t1sdi4, segs, head=True) == \
        [[3, 2], [4, 3]]
    assert levenshtein_seg(s1sdi4, t1sdi4, segs, head=True) == \
        [[3, 2], [4, 3]]


############################################
# x1sdi4b
#    s = "  J K L   N O P Q".split()
#    t = "X Y K L M N   Z Q".split()
# segs    ^ ^|   |^|  ^ ^  |
# type    I S     I   D S
#
# s\t j   X   Y   K   L   M   N   Z   Q
# i  *0+| 1   2 | 3   4 | 5 | 6   7   8
#    -----------------------------------
# J   1 | 1+ *2 | 3   4 | 5 | 6   7   8
#    -----------------------------------
# K   2 | 2   2 | 2-  3 | 4 | 5   6   7
# L   3 | 3   3 | 3   2+|*3 | 4   5   6
#    -----------------------------------
# N   4 | 4   4 | 4   3 | 3 | 3-  4   5
# O   5 | 5   5 | 5   4 | 4 | 4   4   5
# P   6 | 6   6 | 6   5 | 5 | 5   5   5
# Q   7 | 7   7 | 7   6 | 6 | 6   6   5+

def test_levenshtein_seg_fast_1sdi4b():
    """Test levenshtein_seg with the above lists."""
    segs = [[1, 3], [3, 7]]
    assert levenshtein_seg_fast(s1sdi4, t1sdi4, segs) == \
        [[2, 0], [4, 2]]
    assert levenshtein_seg(s1sdi4, t1sdi4, segs) == \
        [[2, 0], [4, 2]]

def test_levenshtein_seg_fast_head_1sdi4b():
    """Test levenshtein_seg with the above lists."""
    segs = [[1, 3], [3, 7]]
    assert levenshtein_seg_fast(s1sdi4, t1sdi4, segs, head=True) == \
        [[2, 1], [4, 3]]
# Note       ^
#     There is ambiguity about how to determine this.
    assert levenshtein_seg(s1sdi4, t1sdi4, segs, head=True) == \
        [[2, 1], [4, 3]]
# Note       ^
#     This is determined by the shifting.


############################################
# x2s1
#    s = "J K L M N O P Q".split()
#    t = "X Y L M N O N K".split()
# segs   |^ ^    |    ^ ^|
# type    S S         S S
#
# s\t j   X   Y   L   M   N   O   N   K
# i  *0+| 1   2   3   4 | 5   6   7   8
#    -----------------------------------
# J   1 | 1-  2   3   4 | 5   6   7   8
# K   2 | 2   2   3   4 | 5   6   7   7
# L   3 | 3   3   2   3 | 4   5   6   7
# M   4 | 4   4   3  *2+| 3   4   5   6
#    -----------------------------------
# N   5 | 5   5   4   3 | 2-  3   4   5
# O   6 | 6   6   5   4 | 3   2   3   4
# P   7 | 7   7   6   5 | 4   3   3   4
# Q   8 | 8   8   7   6 | 5   4+  4+  4+

s2s1 = "J K L M N O P Q".split()
t2s1 = "X Y L M N O N K".split()

def test_levenshtein_seg_fast_2s1():
    """Test levenshtein_seg with the above lists."""
    segs = [[0, 4], [4, 8]]
    assert levenshtein_seg_fast(s2s1, t2s1, segs) == \
        [[4, 2], [4, 2]]
    assert levenshtein_seg(s2s1, t2s1, segs) == \
        [[4, 2], [4, 2]]

def test_levenshtein_seg_fast_head_2s1():
    """Test levenshtein_seg with the above lists."""
    segs = [[0, 4], [4, 8]]
    assert levenshtein_seg_fast(s2s1, t2s1, segs, head=True) == \
        [[4, 2], [4, 2]]
    assert levenshtein_seg(s2s1, t2s1, segs, head=True) == \
        [[4, 2], [4, 2]]


############################################
# x2d1
#    s = "J K L M N O P Q R".split()
#    t = "    L M     P Q  ".split()
# segs   |^ ^  |  ^ ^  |  ^|
# type    D D     D D     D
#
# s\t j   L   M   P   Q
# i  *0+| 1 | 2   3 | 4
#    -------------------
# J   1 | 1-| 2   3 | 4
# J   2 | 2 | 2   3 | 4
# L   3 |*2+| 3   3 | 4
#    -------------------
# M   4 | 3 | 2-  3 | 4
# N   5 | 4 | 3   3 | 4
# O   6 | 5 | 4   4 | 4
# P   7 | 6 | 5  *4+| 5
#    -------------------
# Q   8 | 7 | 6   5 | 4-
# R   9 | 8 | 7   6 | 5+

s2d1 = "J K L M N O P Q R".split()
t2d1 = "    L M     P Q  ".split()

def test_levenshtein_seg_fast_2d1():
    """Test levenshtein_seg with the above lists."""
    segs = [[0, 3], [3, 7], [7, 9]]
    assert levenshtein_seg_fast(s2d1, t2d1, segs) == \
        [[3, 2], [4, 2], [2, 1]]
    assert levenshtein_seg(s2d1, t2d1, segs) == \
        [[3, 2], [4, 2], [2, 1]]

def test_levenshtein_seg_fast_head_2d1():
    """Test levenshtein_seg with the above lists."""
    segs = [[0, 3], [3, 7], [7, 9]]
    assert levenshtein_seg_fast(s2d1, t2d1, segs, head=True) == \
        [[3, 2], [4, 2], [2, 1]]
    assert levenshtein_seg(s2d1, t2d1, segs, head=True) == \
        [[3, 2], [4, 2], [2, 1]]


############################################
# x2d2
#    s = "J K L M N O P".split()
#    t = "    L M N    ".split()
# segs   |^ ^  |    ^ ^|
# type    D D       D D
#
# s\t j   L   M   N
# i  *0+| 1 | 2   3
#    ---------------
# J   1 | 1-| 2   3
# K   2 | 2 | 2   3
# L   3 |*2+| 3   3
#    ---------------
# M   4 | 3 | 2-  3
# N   5 | 4 | 3   2
# O   6 | 5 | 4   3
# P   7 | 6 | 5   4+

s2d2 = "J K L M N O P".split()
t2d2 = "    L M N    ".split()

def test_levenshtein_seg_fast_2d2():
    """Test levenshtein_seg with the above lists."""
    segs = [[0, 3], [3, 7]]
    assert levenshtein_seg_fast(s2d2, t2d2, segs) == \
        [[3, 2], [4, 2]]
    assert levenshtein_seg(s2d2, t2d2, segs) == \
        [[3, 2], [4, 2]]

def test_levenshtein_seg_fast_head_2d2():
    """Test levenshtein_seg with the above lists."""
    segs = [[0, 3], [3, 7]]
    assert levenshtein_seg_fast(s2d2, t2d2, segs, head=True) == \
        [[3, 2], [4, 2]]
    assert levenshtein_seg(s2d2, t2d2, segs, head=True) == \
        [[3, 2], [4, 2]]


############################################
# x2i1
#    s = "    L M N     Q R".split()
#    t = "J K L M N O P Q R".split()
# segs    ^ ^|     |^ ^|   |
# type    I I       I I
#
# s\t j   J   K   L   M   N   O   P   Q   R
# i  *0+| 1   2   3   4   5 | 6   7   8   9
#    ---------------------------------------
# L   1 | 1-  2   2   3   4 | 5   6   7   8
# M   2 | 2   2   3   2   3 | 4   5   6   7
# N   3 | 3   3   3   3  *2+| 3   4   5   6
#    ---------------------------------------
# Q   4 | 4   4   4   4   3 | 3-  4   4   5
# R   5 | 5   5   5   5   4+| 4+  4+  5   4+

s2i1 = "    L M N     Q R".split()
t2i1 = "J K L M N O P Q R".split()

def test_levenshtein_align_2i1():
    """Test levenshtein_align_fast with the above lists."""
    segs = [[0, 3], [3, 5]]
    assert levenshtein_align_fast(s2i1, t2i1, segs) == \
        [[0, 5], [5, 9]]
#       [[2, 5], [7, 9]]    # <- ideal result

def test_levenshtein_seg_fast_2i1():
    """Test levenshtein_seg with the above lists."""
    segs = [[0, 3], [3, 5]]
    assert levenshtein_seg_fast(s2i1, t2i1, segs) == \
        [[3, 2], [2, 2]]
# Note       ^       ^
#     Tight WER fails due to shifted min d1
    assert levenshtein_seg(s2i1, t2i1, segs) == \
        [[3, 0], [2, 0]]

def test_levenshtein_seg_fast_head_2i1():
    """Test levenshtein_seg with the above lists."""
    segs = [[0, 3], [3, 5]]
    assert levenshtein_seg_fast(s2i1, t2i1, segs, head=True) == \
        [[3, 2], [2, 2]]
    assert levenshtein_seg(s2i1, t2i1, segs, head=True) == \
        [[3, 2], [2, 2]]


############################################
# x3s1
#    s = "  J K L M N O P Q R".split()
#    t = "K J   L M N N K J R".split()
# segs   |^   ^    |  ^ ^ ^  |
# type    I   D       S S S
#
# s\t j   B   A   C   D   E   E   B   A   I
# i   0+|*1 | 2   3   4 | 5   6   7   8   9
#     --------------------------------------
# A   1 | 1 | 1-  2   3 | 4   5   6   7   8
# B   2 | 1 | 2   2   3 | 4   5   5   6   7
# C   3 | 2 | 2   2   3 | 4   5   6   6   7
# D   4 | 3 | 3   3  *2+| 3   4   5   6   7
#     --------------------------------------
# E   5 | 4 | 4   4   3 | 2-  3   4   5   6
# F   6 | 5 | 5   5   4 | 3   3   4   5   6
# G   7 | 6 | 6   6   5 | 4   4   4   5   6
# H   8 | 7 | 7   7   6 | 5   5   5   5   6
# I   9 | 8 | 8   8   7 | 6   6   6   6   5+

s3s1 = "  J K L M N O P Q R".split()
t3s1 = "K J   L M N N K J R".split()

def test_levenshtein_seg_fast_3s1():
    """Test levenshtein_seg with the above lists."""
    segs = [[0, 4], [4, 9]]
    assert levenshtein_seg_fast(s3s1, t3s1, segs) == \
        [[4, 1], [5, 3]]
    assert levenshtein_seg(s3s1, t3s1, segs) == \
        [[4, 1], [5, 3]]

def test_levenshtein_seg_fast_head_3s1():
    """Test levenshtein_seg with the above lists."""
    segs = [[0, 4], [4, 9]]
    assert levenshtein_seg_fast(s3s1, t3s1, segs, head=True) == \
        [[4, 2], [5, 3]]
    assert levenshtein_seg(s3s1, t3s1, segs, head=True) == \
        [[4, 2], [5, 3]]


## Special tests without matchings
# Note that the cases of levenshtein_seg are handled by the safety net code.
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
    assert levenshtein_seg(s, t, segs, head=True) == [[1, 1]]


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
    assert levenshtein_seg(s, t, segs, head=True) == [[1, 1]]
