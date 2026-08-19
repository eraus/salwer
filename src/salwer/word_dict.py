## Import from Python standard library
from collections import Counter

def word_count_of_cue(text):
    # Split string into words (key) and count them (value) into a dict.
    # See test_word_count_of_cue() for an example.
    word_list = text.split()
    return dict(Counter(word_list))


def merge_word_count_dicts(dict1, dict2):
    # Merge two word count dicts: words (key) and count them (value).
    # See test_merge_word_count_dicts() for an example.
    merged = dict(Counter(dict1) + Counter(dict2))
    # dict is sorted in the descending order of the value, the count
    return dict(sorted(merged.items(), key=lambda item: item[1], reverse=True))


def word_dict_of_cue(wrd_list):
    # Convert a list of [word, GLD] into a dict of {word: [word count, GLD]}
    # Note that GLD can be float.
    wrd_dict = {}
    for word, value in wrd_list:
        if word == 0:
            print(f"{word = }")
            continue
        if word not in wrd_dict:
            wrd_dict[word] = [0, 0]
        wrd_dict[word][0] += 1
        wrd_dict[word][1] += value
    return wrd_dict


def merge_word_dicts(dict1, dict2):
    # Merge two words dicts of the format {word: [word count, GLD]} into one.
    merged = {}
    all_keys = set(dict1) | set(dict2)
    for key in all_keys:
        list1 = dict1.get(key, [0, 0])
        list2 = dict2.get(key, [0, 0])
        merged[key] = [list1[0] + list2[0], list1[1] + list2[1]]
    return dict(sorted(merged.items(), key=lambda item: item[1], reverse=True))
