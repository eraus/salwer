"""Test functions used for validating word-level LD function."""

from salwer.recipes.validate_wrd_ld import (
    first_error_type,
    next_error_type,
    random_cue,
    random_size_of_cue,
    random_word,

    add_error,
    add_first_error,
    add_next_error,
)


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
        ss, t, e, num_err = add_error(s)
        print(f"\ns: {ss}\nt: {t}\ne: {e}\nnum_err: {num_err}")

#     print(" ".join(["a", "b", " ", "c"]))