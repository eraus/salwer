"""Test functions for obtaining Word Dict"""

from salwer.word_dict import (
    word_count_of_cue,
    merge_word_count_dicts
)


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