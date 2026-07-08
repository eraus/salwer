"""Test functions for Levenshtein distance calculations."""

from salwer.levenshtein import (
    levenshtein_2d,
    levenshtein,
    levenshtein_1d,
)

# Test Levenshtein distance with empty lists
def test_levenshtein_two_empty_lists():
    """Test Levenshtein distance with two empty lists."""
    assert levenshtein_2d([], []) == 0
    assert levenshtein_1d([], []) == 0
    assert levenshtein([], []) == 0


def test_levenshtein_single_empty_list():
    """Test Levenshtein distance with one empty list."""
    s = "J K L".split()
    t = []
    assert levenshtein_2d(s, t) == 3
    assert levenshtein_2d(t, s) == 3
    assert levenshtein_1d(s, t) == 3
    assert levenshtein_1d(t, s) == 3
    assert levenshtein(s, t) == 3
    assert levenshtein(t, s) == 3


# Test Levenshtein distance with identical lists
def test_levenshtein_identical_lists():
    """Test Levenshtein distance when the lists are identical."""
    s = "J K L".split()
    t = "J K L".split()
    assert levenshtein_2d(s, t) == 0
    assert levenshtein_1d(s, t) == 0
    assert levenshtein(s, t) == 0


# Test Levenshtein distance with partial differences
def test_levenshtein_single_substitute():
    """Test Levenshtein distance when there is one substitution."""
    s = "J K L".split()
    t = "J M L".split()
    assert levenshtein_2d(s, t) == 1
    assert levenshtein_2d(t, s) == 1
    assert levenshtein_1d(s, t) == 1
    assert levenshtein_1d(t, s) == 1
    assert levenshtein(s, t) == 1
    assert levenshtein(t, s) == 1


def test_levenshtein_single_deletion():
    """Test Levenshtein distance when there is one deletion."""
    s = "J K L".split()
    t = "J   L".split()
    assert levenshtein_2d(s, t) == 1
    assert levenshtein_1d(s, t) == 1
    assert levenshtein(s, t) == 1


def test_levenshtein_single_insertion():
    """Test Levenshtein distance when there is one deletion."""
    s = "J   L".split()
    t = "J K L".split()
    assert levenshtein_2d(s, t) == 1
    assert levenshtein_1d(s, t) == 1
    assert levenshtein(s, t) == 1


def test_levenshtein_single_sub_del_ins():
    """Test Levenshtein distance when there is one S, D, and I."""
    s = "J K L M N O   Q".split()
    t = "J R L M   O P Q".split()
    assert levenshtein_2d(s, t) == 3
    assert levenshtein_1d(s, t) == 3
    assert levenshtein(s, t) == 3


def test_levenshtein_two_substitutes():
    """Test Levenshtein distance when there are two substitutions."""
    s = "J K L M".split()
    t = "J M L N".split()
    assert levenshtein_2d(s, t) == 2
    assert levenshtein_2d(t, s) == 2
    assert levenshtein_1d(s, t) == 2
    assert levenshtein_1d(t, s) == 2
    assert levenshtein(s, t) == 2
    assert levenshtein(t, s) == 2


def test_levenshtein_two_deletions():
    """Test Levenshtein distance when there are two deletions."""
    s = "J K L M".split()
    t = "J     M".split()
    assert levenshtein_2d(s, t) == 2
    assert levenshtein_1d(s, t) == 2
    assert levenshtein(s, t) == 2


def test_levenshtein_two_insertions():
    """Test Levenshtein distance when there are two deletions."""
    s = "J     M".split()
    t = "J K L M".split()
    assert levenshtein_2d(s, t) == 2
    assert levenshtein_1d(s, t) == 2
    assert levenshtein(s, t) == 2


# Test Levenshtein distance without common elements
def test_levenshtein_no_common_elements():
    """Test Levenshtein distance when lists have not commen elements."""
    s = "J     M".split()
    t = "  K L  ".split()
    assert levenshtein_2d(s, t) == 2
    assert levenshtein_2d(t, s) == 2
    assert levenshtein_1d(s, t) == 2
    assert levenshtein_1d(t, s) == 2
    assert levenshtein(s, t) == 2
    assert levenshtein(t, s) == 2


# Test alignment with a Levenshtein algorithm
def test_levenshtein_prefix_hallucination_removal():
    """Test Levenshtein distance with alignments."""
    s = "        N O P Q R".split()
    t = "J K L M N   P Q R".split()
    assert levenshtein(s, t) == 5
    assert levenshtein(s, t[1:]) == 4
    assert levenshtein(s, t[2:]) == 3
    assert levenshtein(s, t[3:]) == 2
    assert levenshtein(s, t[4:]) == 1
    assert levenshtein(s, t[5:]) == 2
