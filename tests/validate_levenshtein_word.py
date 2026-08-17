"""Test functions used for validating word-level LD function."""

import pytest

from salwer.levenshtein import levenshtein_gld
from .levenshtein_word_validation import (
    random_cue,
    random_size_of_cue,
    add_error,
    attribute_wl_gld,
    verify_s_t_e,
)
from .helpers import wlst_approx_eq


def test_validate_wrd_ld_fun_():
    """Calculate word-level WER between ref and hyp transcripts.

    Arguments:
    -   num_examples: int = 1000. The number of simulation examples.
    """

    num_examples = 80
    good_cases = []
    bad_cases = []
    for i in range(num_examples):
        s = random_cue(random_size_of_cue())
        s, t, e, _ = add_error(s)
        ss = [ele for ele in s if ele != " "]
        tt = [ele for ele in t if ele != " "]
        if not verify_s_t_e(s, t, e):
            continue
        print(f"{i = }")
        print(f"{ss = }")
        print(f"{tt = }")
        direct_cal = attribute_wl_gld(s, e)
        wrd_ld_cal = levenshtein_gld(ss, tt, err_limit=100)

        if wlst_approx_eq(direct_cal, wrd_ld_cal):
            good_cases.append(direct_cal)
        else:
            bad_cases.append([direct_cal, wrd_ld_cal, s, t, e, ss, tt])

    print(f"Number of good cases: {len(good_cases)}")
    print(f"Number of bad cases: {len(bad_cases)}")

    for case in bad_cases:
        print(f"direct_cal = {case[0]}")
        print(f"wrd_ld_cal = {case[1]}")
        print(f"s  = {case[2]}")
        print(f"t  = {case[3]}")
        print(f"e  = {case[4]}")
        print(f"ss = {case[5]}")
        print(f"tt = {case[6]}\n")

    print(f"Skipped cases: {num_examples - len(good_cases) - len(bad_cases)}")
    print(f"Number of good cases: {len(good_cases)}")
    print(f"Number of bad cases: {len(bad_cases)}")


# def test_errer_generate_issues():
#     for i in range(1000):
#         s = random_cue(random_size_of_cue())
#         s, t, e, num_err = add_error(s)
#         if not verify_s_t_e(s, t, e):
#             print(f"Error generation has issue at {i = }")
#             print(f"s: {s}\nt: {t}\ne: {e}\nnum_err: {num_err}")
#             break


#    s = "      M N M    ".split()
#    t = "J K L M N O P Q".split()
#         ^ ^ ^     ^ ^ ^


# def test_basic():
# #     for i in range(1000):
#     print(" ".join(["a", "b", " ", "c"]))

# @app.command("validate-word-LD-func")
# @app.command("vwl")
# def validate_wrd_ld_fun(

#     num_examples: int = typer.Option(
#         1000, "--nexamples",
#         help=(
#             "Choose limit of error (edit) for each word. Note that this is "
#             "doubled result, meaning 3 => max 150% WER for each word."
#         )
#     ),
# ):
#     """Validate the word-level LD calculation function via simulation.

#     We did not provide theoretical proof that the word-level LD caucluation
#     algorithm works. Here, we use simulation to validate it.

#     Arguments:
#     -   num_examples: int = 1000. The number of simulation examples.

#     Example:
#     -  salwer vwl --nexamples 2000
#     """

#     return validate_wrd_ld_fun_(num_examples)