"""Test functions for obtaining Word Dict"""

from salwer.word_dict import (
    word_count_of_cue,
    merge_word_count_dicts,
    word_dict_of_cue,
    merge_word_dicts,
)
from salwer.recipes.calculate_wrd_wer import _get_seg_wrd_list


# Tests for word_count_of_cue
def test_word_count_of_cue():
    """Test word_count_of_cue for a given text string."""
    text = "the quick brown fox jumps over the lazy dog the quick brown fox"
    wrd_dict = {'the': 3, 'quick': 2, 'brown': 2, 'fox': 2, 'jumps': 1,
                'over': 1, 'lazy': 1, 'dog': 1}
    assert word_count_of_cue(text) == wrd_dict


# Tests for merge_word_count_dicts
def test_merge_word_count_dicts():
    """Test merge_word_count_dicts for two given text strings."""
    wrd_dict1 = {'the': 3, 'quick': 2, 'brown': 2, 'fox': 2, 'jumps': 1,
                'over': 1, 'lazy': 1, 'dog': 1}
    wrd_dict2 = {'the': 3, 'quick': 2, 'brown': 2, 'fox': 2, 'jumps': 1,
                'over': 1, 'lazy': 1, 'dog': 1, 'slow': 5}
    wrd_dict = {'the': 6, 'slow': 5, 'quick': 4, 'brown': 4, 'fox': 4, 'jumps': 2,
                'over': 2, 'lazy': 2, 'dog': 2}
    assert merge_word_count_dicts(wrd_dict1, wrd_dict2) == wrd_dict


# Tests for word_dict_of_cue
def test_word_dict_of_cue():
    """Test word_dict_of_cue for a given list of words and levenshtein dists."""
    wrd_list = [
        ["A", 2], ["B", 1], ["D", 1], ["A", 1],
        ["E", 2], ["F", 1], ["H", 1], ["I", 0],
        ["E", 2], ["F", 1], ["H", 1], ["I", 0],
    ]
    wrd_dict = {
        "A": [2, 3], "B": [1, 1], "D": [1, 1],
        "E": [2, 4], "F": [2, 2], "H": [2, 2], "I": [2, 0],
    }
    assert word_dict_of_cue(wrd_list) == wrd_dict


# Tests for merge_word_count_dicts
def test_merge_word_dicts():
    """Test merge_word_dicts."""
    wrd_dict1 = {
        "A": [2, 3], "B": [1, 1], "D": [1, 1],
        "E": [2, 4], "F": [2, 2], "H": [2, 2], "I": [2, 0],
    }
    wrd_dict2 = {
        "A": [2, 3], "B": [1, 1], "D": [1, 1], "C": [4, 3],
        "E": [2, 4], "F": [2, 2], "H": [2, 2]
    }
    wrd_dict3 = {
        "A": [4, 6], "B": [2, 2], "D": [2, 2], "C": [4, 3],
        "E": [4, 8], "F": [4, 4], "H": [4, 4], "I": [2, 0],
    }
    assert merge_word_dicts(wrd_dict1, wrd_dict2) == wrd_dict3


def test__get_seg_wrd_list():
    cue_wrd_list = [
        ["A", 2], ["B", 1], ["C", 3],
        ["D", 4], ["E", 5],
    ]
    cue_seg_ranges = [
        [0, 2], [3, 5],
    ]
    result = _get_seg_wrd_list(cue_wrd_list, cue_seg_ranges)
    expected = [
        ["A", 2], ["B", 1],
        ["D", 4], ["E", 5],
    ]
    assert result == expected