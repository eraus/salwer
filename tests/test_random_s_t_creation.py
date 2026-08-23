"""Test functions used for validating word-level LD function."""

import pytest

from .random_s_t_creation import (
    first_error_type,
    next_error_type,
    random_cue,
    random_size_of_cue,
    random_word,
    #
    add_errors,
    add_first_error,
    add_next_error,
    #
    verify_s_t_e,
    #
    VOCAB
)


#--------------------------------------------------------------------
# Test for verifications only
#--------------------------------------------------------------------

def test_print_first60_vocab():
    first60 = VOCAB[: 60]
    print(f"\nFirst 60 words: {" ".join(first60)}")


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


def test_10_random_cues_small_voc():
    print()
    for size in range(5, 15):
        print(random_cue(size, use_large_voc=False))


def test_10_random_cues_large_voc():
    print()
    for size in range(5, 15):
        print(random_cue(size, use_large_voc=True))


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
