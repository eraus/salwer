## Import from Python standard library
from collections import Counter

def word_count_of_cue(text):
    # Split the string into words and count them
    word_list = text.split()
    return dict(Counter(word_list))


def merge_word_count_dicts(dict1, dict2):
    merged = dict(Counter(dict1) + Counter(dict2))
    return dict(sorted(merged.items(), key=lambda item: item[1], reverse=True))


def word_dict_of_cue(text):
    # Split the string into words and count them
