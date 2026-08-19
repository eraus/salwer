"""Test functions used for validating word-level LD function."""

import pytest

from .levenshtein_word_validation import (
    first_error_type,
    next_error_type,
    random_cue,
    random_size_of_cue,
    random_word,

    add_errors,
    add_first_error,
    add_next_error,

    attribute_wl_gld,
    find_sub_index,
    find_sub_ins_index_num_of_sub,

    verify_s_t_e,
)
from .helpers import assert_wlst_eq


#--------------------------------------------------------------------
# Test Levenshtein distance with empty lists
#--------------------------------------------------------------------

def test_10_first_errors():
    ten_errs = [first_error_type() for _ in range(10)]
    print(f"\nTen first errors: {" ".join(ten_errs)}")


def test_10_next_errors():
    ten_errs_after_sub = [next_error_type("sub") for _ in range(10)]
    print(f"\nTen errors after sub: {" ".join(ten_errs_after_sub)}")
    ten_errs_after_del = [next_error_type("del") for _ in range(10)]
    print(f"Ten errors after del: {" ".join(ten_errs_after_del)}")
    ten_errs_after_ins = [next_error_type("ins") for _ in range(10)]
    print(f"Ten errors after ins: {" ".join(ten_errs_after_ins)}")


def test_10_random_cues():
    print()
    for size in range(5, 15):
        print(random_cue(size))


def test_10_random_sizes():
    ten_sizes = [str(random_size_of_cue()) for _ in range(10)]
    print(f"\nTen random sizes: {", ".join(ten_sizes)}")


def test_10_random_words():
    ten_words = [random_word() for _ in range(10)]
    print(f"\nTen random words: {", ".join(ten_words)}")


#-----------------------------------------------------
def test_10_add_first_errors():
    s = "A B C".split()
    for _ in range(10):
        ss, t, e, ind_err = add_first_error(s)
        print(f"\ns: {ss}\nt: {t}\ne: {e}\nind_err: {ind_err}")


def test_15_add_next_errors():
    s = "A B C D".split()
    for _ in range(15):
        ss, t, e, ind_err = add_first_error(s)
        ss, t, e, ind_err, num_err = add_next_error(ss, t, e, ind_err)
        print(f"\ns: {ss}\nt: {t}\ne: {e}\nnum_err: {num_err}")


def test_10_add_errors():
    s = "A B C D E".split()
    for _ in range(10):
        ss, t, e, num_err = add_errors(s)
        print(f"\ns: {ss}\nt: {t}\ne: {e}\nnum_err: {num_err}")



#-----------------------------------------------------
def test_find_sub_index1():
    e = ["S", "S", " ", " ", " ", "S", "S", " ", " "]
#  index: 0    1    2    3    4    5    6    7    8
    exp_ind_lst = [[0, 2], [5, 7]]
    assert find_sub_index(e) == exp_ind_lst


def test_find_sub_index2():
    e = [" ", "S", " ", "D", " ", "S", "I", " ", "I"]
#  index: 0    1    2    3    4    5    6    7    8
    exp_ind_lst = [[1, 2]]
    assert find_sub_index(e) == exp_ind_lst

def test_find_sub_index2():
    e = [' ', ' ', 'I', 'I', 'S', 'S', ' ', ' ']
#  index: 0    1    2    3    4    5    6    7    8
    exp_ind_lst = []
    assert find_sub_index(e) == exp_ind_lst

#-----------------------------------------------------
def test_find_sub_ins_index_num_of_sub1():
    e = ["I", "I", "S", " ", " ", "I", "S", "I", "S"]
#  index: 0    1    2    3    4    5    6    7    8
    exp_ind_num_lst = [[0, 3, 1], [5, 9, 2]]
    assert find_sub_ins_index_num_of_sub(e) == exp_ind_num_lst


def test_find_sub_ins_index_num_of_sub2():
    e = [" ", "S", " ", "D", " ", "S", "I", " ", "I"]
#  index: 0    1    2    3    4    5    6    7    8
    exp_ind_num_lst = [[5, 7, 1], [8, 9, 0]]
    assert find_sub_ins_index_num_of_sub(e) == exp_ind_num_lst


def test_find_sub_ins_index_num_of_sub3():
    e = ["I", "S", " ", "D", " ", "S", "I", "I", "S"]
#  index: 0    1    2    3    4    5    6    7    8
    exp_ind_num_lst = [[0, 2, 1], [5, 9, 2]]
    assert find_sub_ins_index_num_of_sub(e) == exp_ind_num_lst


#-----------------------------------------------------------------
def test_attribute_wl_gld_1_dels():
    s = ["J", "K", "L", "M", "N", "O"]
#   t = ["J", " ", "L", " ", "N", " "]
    e = [" ", "D", " ", "D", " ", "D"]
    exp_wlst = [["J", 0.0], ["K", 1.0], ["L", 0.0],
                ["M", 1.0], ["N", 0.0], ["O", 1.0]]
    out_wlst = attribute_wl_gld(s, e)
    out_wlst_w = [e[0] for e in out_wlst]
    out_wlst_n = [e[1] for e in out_wlst]
    exp_wlst_w = [e[0] for e in exp_wlst]
    exp_wlst_n = [e[1] for e in exp_wlst]
    assert out_wlst_w == exp_wlst_w
    assert out_wlst_n == pytest.approx(exp_wlst_n)




def test_attribute_wl_ld_1_subs_index():
    e = [" ", "S", " ", "S", " ", "S"]
    exp_ind_lst = [[1, 2], [3, 4], [5, 6]]
    assert find_sub_index(e) == exp_ind_lst


def test_attribute_wl_gld_1_subs():
    s = ["J", "K", "L", "M", "N", "O"]
#   t = ["J", " ", "L", " ", "N", " "]
    e = [" ", "S", " ", "S", " ", "S"]
    # exp_wlst = [["J", 0], ["K", 2], ["L", 0], ["M", 2], ["N", 0], ["O", 2]]
    exp_wlst = [["J", 0.0], ["K", 1.0], ["L", 0.0],
                ["M", 1.0], ["N", 0.0], ["O", 1.0]]
    assert_wlst_eq(attribute_wl_gld(s, e), exp_wlst)


def test_attribute_wl_gld_2_subs():
    s = ["J", "K", "L", "M", "N", "O"]
#   t = ["J", " ", "L", " ", "N", " "]
    e = [" ", "S", "S", "S", " ", "S"]
    exp_wlst = [["J", 0.0], ["K", 1.0], ["L", 1.0],
                ["M", 1.0], ["N", 0.0], ["O", 1.0]]
    # exp_wlst = [["J", 0], ["K", 2], ["L", 2], ["M", 2], ["N", 0], ["O", 2]]
    # assert attribute_wl_ld(s, e) == exp_wlst
    assert_wlst_eq(attribute_wl_gld(s, e), exp_wlst)

def test_find_sub_index_num_of_sub4():
    e = [" ", "S", "I", "S", " ", "S"]
#  index: 0    1    2    3    4    5
    exp_ind_num_lst = [[5, 6]]
    assert find_sub_index(e) == exp_ind_num_lst


def test_find_sub_ins_index_num_of_sub4():
    e = [" ", "S", "I", "S", " ", "S"]
#  index: 0    1    2    3    4    5
    exp_ind_num_lst = [[1, 4, 2]]
    assert find_sub_ins_index_num_of_sub(e) == exp_ind_num_lst


def test_attribute_wl_gld_1_ins_subs():
    s = ["J", "K", " ", "M", "N", "O"]
#   t = ["J", "N", "L", "Q", "N", "Q"]
    e = [" ", "S", "I", "S", " ", "S"]
    exp_wlst = [["J", 0.5], ["K", 1.0], ["M", 1.0], ["N", 0.5], ["O", 1.0]]
    # assert attribute_wl_ld(s, e) == exp_wlst
    assert_wlst_eq(attribute_wl_gld(s, e), exp_wlst)


def test_find_sub_index_num_of_sub5():
    e = [" ", "S", "I", "S", " ", "S", "I"]
#  index: 0    1    2    3    4    5
    exp_ind_num_lst = []
    assert find_sub_index(e) == exp_ind_num_lst


def test_find_sub_ins_index_num_of_sub5():
    e = [" ", "S", "I", "S", " ", "S", "I"]
#  index: 0    1    2    3    4    5
    exp_ind_num_lst = [[1, 4, 2], [5, 7, 1]]
    assert find_sub_ins_index_num_of_sub(e) == exp_ind_num_lst

def test_attribute_wl_gld_2_ins_subs():
    s = ["J", "K", " ", "M", "N", "O", " "]
#   t = ["J", "N", "L", "Q", "N", "Q"]
    e = [" ", "S", "I", "S", " ", "S", "I"]
    exp_wlst = [["J", 0.5], ["K", 1.0], ["M", 1.0], ["N", 1.0], ["O", 1.5]]
    # assert attribute_wl_ld(s, e) == exp_wlst
    assert_wlst_eq(attribute_wl_gld(s, e), exp_wlst)

# direct_cal = [['z', 0.0], ['B', 0.0], ['N', 0.0], ['J', 0.0], ['S', 0.0], ['t', 0.5], ['A', 1.5], ['w', 2.5], ['V', 0.5], ['p', 0.0]]
# wrd_ld_cal = [['z', 0.0], ['B', 0.0], ['N', 0.0], ['J', 0.0], ['S', 0.0], ['t', 0.5], ['A', 1.5], ['w', 1.5], ['V', 0.5], ['p', 0.0]]
# s  = ['z', 'B', 'N', 'J', 'S', 't', ' ', ' ', 'A', 'w', 'V', 'p']
# t  = ['z', 'B', 'N', 'J', 'S', 't', 'r', 'S', 'B', 'Z', 'V', 'p']
# e  = [' ', ' ', ' ', ' ', ' ', ' ', 'I', 'I', 'S', 'S', ' ', ' ']
# ss = ['z', 'B', 'N', 'J', 'S', 't', 'A', 'w', 'V', 'p']
# tt = ['z', 'B', 'N', 'J', 'S', 't', 'r', 'S', 'B', 'Z', 'V', 'p']


#-----------------------------------------------------

def test_find_sub_index1_num_of_sub5():
#  index: 0    1    2    3    4    5
    e = ["I", "I", "S", " ", " ", "I", "I", "S", " "]
    exp_ind_num_lst = []
    assert find_sub_index(e) == exp_ind_num_lst


# The following tests are paired
def test_find_ins_index1():
#   s =  "          L    M    N              Q    R".split()
#   t =  "J    K    L    M    N    O    P    P    R".split()
    e = ["I", "I", "S", " ", " ", "I", "I", "S", " "]
#  index: 0    1    2    3    4    5
    exp_ind_num_lst = [[0, 3, 1], [5, 8, 1]]
    assert find_sub_ins_index_num_of_sub(e) == exp_ind_num_lst

def test_attribute_errors1():
    s = [" ", " ", "L", "M", "N", " ", " ", "Q", "R"]
#   t =  "J    K    J    M    N    O    P    P    R".split()
    e = ["I", "I", "S", " ", " ", "I", "I", "S", " "]
    exp_wlst = [["L", 2.5], ["M", 0.5], ["N", 0.5], ["Q", 2.0], ["R", 0.5]]
    assert_wlst_eq(attribute_wl_gld(s, e), exp_wlst)

#-----------------------------------------------------
def test_verify_s_t_e_1():
    s = ["J", "K", "L", "M", "N", "O", " ", "Q", " "]
    t = ["J", "R", "L", " ", "N", "L", "P", "Q", "R"]
    e = [" ", "S", " ", "D", " ", "S", "I", " ", "I"]
    exp_bool = True
    assert verify_s_t_e(s, t, e) == exp_bool


#-----------------------------------------------------
def test_verify_s_t_e_2():
    s = [' ', 'A', 'B', 'C', 'D']
    t = ['A', 'I', 'B', 'C', 'D']
    e = ['I', 'S', ' ', ' ', ' ']
    exp_bool = False
    assert verify_s_t_e(s, t, e) == exp_bool
