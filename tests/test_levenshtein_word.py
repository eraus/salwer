"""Test functions for edit distance calculations."""

import pytest

from salwer.levenshtein import (
    levenshtein_seg,
    levenshtein_word_raw,
    levenshtein_word,
)


# When we calculate the word-level Levenshtein distance using the seg-based
# approach, we need to use the head version, which includes the leading
# drift (hallucination).


# Single consecutive substitution error case:

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
    """Test word-level Levenshtein distance using seg-based approach."""
    segs = [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 9]]
    assert levenshtein_seg(s0, t0, segs, head=True) == \
        [[1, 0], [1, 0], [1, 1], [1, 0], [1, 0], [1, 1], [3, 0]]

def test_levenshtein_word_raw_0():
    """Test word-level Levenshtein distance using word-based approach."""
    assert levenshtein_word_raw(s0, t0) == \
        [["A", 0], ["B", 0], ["A", 1],
         ["D", 0], ["E", 0], ["B", 1],
         ["G", 0], ["H", 0], ["I", 0]]

def test_levenshtein_word_0():
    """Test word-level Levenshtein distance using word-based approach."""
    assert levenshtein_word(s0, t0) == \
        [["A", 0], ["B", 0], ["A", 1],
         ["D", 0], ["E", 0], ["B", 1],
         ["G", 0], ["H", 0], ["I", 0]]

# Single-deletion from source case:

# s = "A B C D E F G H I".split()
# t = "A B   D E   G H I".split()
#
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
    """Test word-level Levenshtein distance using seg-based approach."""
    segs = [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 9]]
    assert levenshtein_seg(s1, t1, segs, head=True) == \
        [[1, 0], [1, 0], [1, 1], [1, 0], [1, 0], [1, 1], [3, 0]]

def test_levenshtein_word_raw_1():
    """Test word-level Levenshtein distance using word-based approach."""
    assert levenshtein_word_raw(s1, t1) == \
        [["A", 0], ["B", 0], ["C", 1],
         ["D", 0], ["E", 0], ["F", 1],
         ["G", 0], ["H", 0], ["I", 0]]

def test_levenshtein_word_1():
    """Test word-level Levenshtein distance using word-based approach."""
    assert levenshtein_word(s1, t1) == \
        [["A", 0], ["B", 0], ["C", 1],
         ["D", 0], ["E", 0], ["F", 1],
         ["G", 0], ["H", 0], ["I", 0]]

# Single insertation to the source case (only one prefix drift):

# s = "A B   D E   G H I".split()
# t = "A B C D E F G H I".split()
#
# s\t j   A   B   C   D   E   F   G   H   I
# i   0+| 1   2 | 3 | 4   5 | 6 | 7   8   9
#    ---|-------|---|-------|---|-----------
# A   1 | 0-  1 | 2 | 3   4 | 5 | 6   7   8
# B   2 | 1   0+| 1*| 2   3 | 4 | 5   6   7
#    ---|-------|---|-------|---|-----------
# D   3 | 2   1 | 1 | 1-  2 | 3 | 4   5   6
# E   4 | 3   2 | 2 | 2   1+| 2*| 3   4   5
#    ---|-------|---|-------|---|-----------
# G   5 | 4   3 | 3 | 3   2 | 2 | 2-  3   4
# H   6 | 5   4 | 4 | 4   3 | 3 | 3   2   3
# I   7 | 6   5 | 5 | 5   4 | 4 | 4   3   2+

s2 = "A B   D E   G H I".split()
t2 = "A B C D E F G H I".split()

def test_levenshtein_seg_head_2():
    """Test word-level Levenshtein distance using seg-based approach."""
    segs = [[0, 1], [1, 2], [2, 3], [3, 4], [4, 7]]
    assert levenshtein_seg(s2, t2, segs, head=True) == \
        [[1, 0], [1, 0], [1, 1], [1, 0], [3, 1]]

def test_levenshtein_word_raw_2():
    """Test word-level Levenshtein distance using word-based approach."""
    assert levenshtein_word_raw(s2, t2) == \
        [["A", 0], ["B", 0], ["D", 1],
         ["E", 0], ["G", 1], ["H", 0],
         ["I", 0]]

def test_levenshtein_word_2():
    """Test word-level Levenshtein distance using word-based approach."""
    assert levenshtein_word(s2, t2) == \
        [["A", 0], ["B", 0], ["D", 1],
         ["E", 0], ["G", 1], ["H", 0],
         ["I", 0]]


# Another single insertation to the source case (only one prefix drift):

# s = "  B C D E   G H I".split()
# t = "A B C D E F G H I".split()
#
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
    """Test word-level Levenshtein distance using seg-based approach."""
    segs = [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 7]]
    assert levenshtein_seg(s3, t3, segs, head=True) == \
        [[1, 1], [1, 0], [1, 0], [1, 0], [1, 1], [2, 0]]

def test_levenshtein_word_raw_3():
    """Test word-level Levenshtein distance using word-based approach."""
    assert levenshtein_word_raw(s3, t3) == \
        [["B", 1], ["C", 0], ["D", 0],
         ["E", 0], ["G", 1], ["H", 0],
         ["I", 0]]

# NOTE: No issues with single-insertions.

def test_levenshtein_word_3():
    """Test word-level Levenshtein distance using word-based approach."""
    assert levenshtein_word(s3, t3) == \
        [["B", 1], ["C", 0], ["D", 0],
         ["E", 0], ["G", 1], ["H", 0],
         ["I", 0]]

# Multiple-insertation to the source case (2+ prefix drifts):

# s = "    C D E     H I".split()
# t = "A B C D E F G H I".split()
#
# s\t j   A   B   C   D   E   F   G   H   I
# i   0+| 1   2*| 3   4   5 | 6   7 | 8   9
#    ---------------------------------------
# C   1 | 1-  2 | 2-  3   4 | 5   6 | 7   8
# D   2 | 2   2 | 3   2   3 | 4   5 | 6   7
# E   3 | 3   3 | 3   3   2+| 3   4*| 5   6
#    ---------------------------------------
# H   4 | 4   4 | 4   4   3 | 3-  4 | 4-  5
# I   5 | 5   5 | 5   5   4 | 4   4 | 5   4+

s4 = "    C D E     H I".split()
t4 = "A B C D E F G H I".split()

def test_levenshtein_seg_head_4():
    """Test word-level Levenshtein distance using seg-based approach."""
    segs = [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5]]
    # print(f"{levenshtein_n_seg_size(s4, t4, segs, head=True) = }")
    assert levenshtein_seg(s4, t4, segs, head=True) == \
        [[1, 1], [1, 1], [1, 0], [1, 1], [1, 1]]

def test_levenshtein_word_raw_4():
    """Test word-level Levenshtein distance using word-based approach."""
    assert levenshtein_word_raw(s4, t4) == \
        [["C", 1], ["D", 1], ["E", 0],
         ["H", 1], ["I", 1]]

# NOTE: If we have 2+ consecutive prefix hallucination words,
# the first two words in the reference will be affected. To address this issue,
# we can remove a word in the target repeatedly until the situation is getting
# worse.

def test_levenshtein_word_4():
    """Test word-level Levenshtein distance using word-based approach."""
    assert levenshtein_word(s4, t4) == \
        [["C", 1], ["D", 1], ["E", 0],
         ["H", 1], ["I", 1]]


# 2+ deletion from the source case:

# s = "A B C D E F G H I".split()
# t = "    C D E     H I".split()
#
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
    """Test word-level Levenshtein distance using seg-based approach."""
    segs = [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 9]]
    assert levenshtein_seg(s5, t5, segs, head=True) == \
        [[1, 1], [1, 1], [1, 0], [1, 0], [1, 0], [4, 2]]

def test_levenshtein_word_raw_5():
    """Test word-level Levenshtein distance using word-based approach."""
    assert levenshtein_word_raw(s5, t5) == \
        [["A", 1], ["B", 1], ["C", 0],
         ["D", 0], ["E", 0], ["F", 1],
         ["G", 1], ["H", 0], ["I", 0]]

# NOTE: No issues with processing multiple deletion cases.

def test_levenshtein_word_5():
    """Test word-level Levenshtein distance using word-based approach."""
    assert levenshtein_word(s5, t5) == \
        [["A", 1], ["B", 1], ["C", 0],
         ["D", 0], ["E", 0], ["F", 1],
         ["G", 1], ["H", 0], ["I", 0]]


# Need to have multiple substitution cases.

# s = "A B A D E B G J K".split()
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
# J   8 | 7   6   6 | 5   4   4 | 3   3   4
# K   9 | 8   7   7 | 6   5   5 | 4   4   4+

s6 = "A B A D E B G J K".split()
t6 = "A B C D E F G H I".split()

def test_levenshtein_seg_head_6():
    """Test word-level Levenshtein distance using seg-based approach."""
    segs = [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 9]]
    assert levenshtein_seg(s6, t6, segs, head=True) == \
        [[1, 0], [1, 0], [1, 1], [1, 0], [1, 0], [1, 1], [3, 2]]

def test_levenshtein_word_raw_6():
    """Test word-level Levenshtein distance using word-based approach."""
    assert levenshtein_word_raw(s6, t6) == \
        [["A", 0], ["B", 0], ["A", 1],
         ["D", 0], ["E", 0], ["B", 1],
         ["G", 0], ["J", 1], ["K", 1]]

# NOTE: No issues with processing multiple substitution cases.

def test_levenshtein_word_6():
    """Test word-level Levenshtein distance using word-based approach."""
    assert levenshtein_word(s6, t6) == \
        [["A", 0], ["B", 0], ["A", 1],
         ["D", 0], ["E", 0], ["B", 1],
         ["G", 0], ["J", 1], ["K", 1]]
