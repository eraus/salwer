"""Test functions for Levenshtein distance calculations."""

from salwer.levenshtein import (
    _levenshtein_full_mem,
    _levenshtein,
    _levenshtein_one_list,
)


# Tests for _levenshtein_full_mem

def test_levenshtein_full_mem_two_empty_lists():
    """Test edit distance with empty lists."""
    assert _levenshtein_full_mem([], []) == 0


def test_levenshtein_full_mem_single_empty_list():
    """Test edit distance with one deletion."""
    s = ["a", "b", "c"]
    t = []
    assert _levenshtein_full_mem(s, t) == 3
    assert _levenshtein_full_mem(t, s) == 3

def test_levenshtein_full_mem_identical_lists():
    """Test edit distance when lists are identical."""
    s = ["a", "b", "c"]
    t = ["a", "b", "c"]
    assert _levenshtein_full_mem(s, t) == 0


def test_levenshtein_full_mem_single_deletion():
    """Test edit distance with one deletion."""
    s = ["a", "b", "c"]
    t = ["a", "c"]
    assert _levenshtein_full_mem(s, t) == 1


def test_levenshtein_full_mem_single_insertion():
    """Test edit distance with one deletion."""
    s = ["a", "c"]
    t = ["a", "b", "c"]
    assert _levenshtein_full_mem(s, t) == 1


def test_levenshtein_full_mem_single_substitute():
    """Test edit distance when lists are identical."""
    s = ["a", "b", "c"]
    t = ["a", "d", "c"]
    assert _levenshtein_full_mem(s, t) == 1
    assert _levenshtein_full_mem(t, s) == 1


def test_levenshtein_full_mem_no_common_elements():
    """Test edit distance when lists are identical."""
    s = ["a", "b"]
    t = ["c", "d"]
    assert _levenshtein_full_mem(s, t) == 2
    assert _levenshtein_full_mem(t, s) == 2


# Brief tests for _levenshtein

def test_levenshtein_empty_lists():
    """Test edit distance with empty lists."""
    assert _levenshtein([], []) == 0


def test_levenshtein_identical_lists():
    """Test edit distance when lists are identical."""
    s = ["a", "b", "c"]
    t = ["a", "b", "c"]
    assert _levenshtein(s, t) == 0


def test_levenshtein_single_deletion():
    """Test edit distance with one deletion."""
    s = ["a", "b", "c"]
    t = ["a", "c"]
    assert _levenshtein(s, t) == 1
    assert _levenshtein(t, s) == 1


# Brief tests for _levenshtein_one_list

def test_levenshtein_one_list_empty_lists():
    """Test edit distance with empty lists."""
    assert _levenshtein_one_list([], []) == 0


def test_levenshtein_one_list_identical_lists():
    """Test edit distance when lists are identical."""
    s = ["a", "b", "c"]
    t = ["a", "b", "c"]
    assert _levenshtein_one_list(s, t) == 0


def test_levenshtein_one_list_single_deletion():
    """Test edit distance with one deletion."""
    s = ["a", "b", "c"]
    t = ["a", "c"]
    assert _levenshtein_one_list(s, t) == 1
    assert _levenshtein_one_list(t, s) == 1


### Alignment testing

def test_levenshtein_prefix_hallucination_removal():
    """Test edit distance with one deletion."""
    s = "climb and maintain one zero thousand".split()
    t = "uh yeah tower said climb maintain one zero thousand".split()
    assert _levenshtein(s, t) == 5
    assert _levenshtein(s, t[1:]) == 4
    assert _levenshtein(s, t[2:]) == 3
    assert _levenshtein(s, t[3:]) == 2
    assert _levenshtein(s, t[4:]) == 1
    assert _levenshtein(s, t[5:]) == 2

