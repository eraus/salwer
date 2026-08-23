"""Helper functions used for testing word-list functions having floats."""

import pytest


def assert_word_list_eq(fnc_word_list, exp_word_list):
    fnc_word_list_w = [e[0] for e in fnc_word_list]
    fnc_word_list_n = [e[1] for e in fnc_word_list]
    exp_word_list_w = [e[0] for e in exp_word_list]
    exp_word_list_n = [e[1] for e in exp_word_list]
    assert fnc_word_list_w == exp_word_list_w
    assert fnc_word_list_n == pytest.approx(exp_word_list_n)


def word_dict_approx_eq(fnc_word_dict, exp_word_dict):
    if fnc_word_dict.keys() != exp_word_dict.keys():
        return False
    for key in fnc_word_dict:
        if fnc_word_dict[key] != pytest.approx(exp_word_dict[key]):
            return False
    return True


def word_list_approx_eq(fnc_word_list, exp_word_list):
    fnc_word_list_w = [e[0] for e in fnc_word_list]
    fnc_word_list_n = [e[1] for e in fnc_word_list]
    exp_word_list_w = [e[0] for e in exp_word_list]
    exp_word_list_n = [e[1] for e in exp_word_list]
    return (
        fnc_word_list_w == exp_word_list_w
        and fnc_word_list_n == pytest.approx(exp_word_list_n)
    )
