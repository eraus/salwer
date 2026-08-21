"""Test function used for validating word-level LD function."""

from salwer.from_aligned import attribute_wl_gld
from salwer.levenshtein import levenshtein_gld
from salwer.word_dict import (
    word_dict_of_cue,
    merge_word_dicts,
)
from .random_s_t_creation import (
    random_size_of_cue, random_cue,
    add_errors, verify_s_t_e,
)
from .helpers import wlst_approx_eq


def test_validate_wrd_ld_fun():
    """Validate the word-level GLD function levenshtein_gld.

    To run it, use: `pytest tests/validate_levenshtein_word.py`
    """

    num_examples = 1000  # total examples to run
    same_cases = []
    diff_cases = []
    err_cases = []
    sim_dict_direct = {}
    sim_dict_wrd_ld = {}
    for i in range(num_examples):
        s = random_cue(random_size_of_cue())
        s, t, e, _ = add_errors(s)
        ss = [ele for ele in s if ele != " "]
        tt = [ele for ele in t if ele != " "]
        if not verify_s_t_e(s, t, e):
            continue

        direct_cal = attribute_wl_gld(s, e)
        wrd_ld_cal = levenshtein_gld(ss, tt, err_limit=100)
        if wlst_approx_eq(direct_cal, wrd_ld_cal):
            same_cases.append(direct_cal)
        else:
            diff_cases.append([direct_cal, wrd_ld_cal, s, t, e, ss, tt])

        direct_err = [err[1] for err in direct_cal]
        wrd_ld_err = [err[1] for err in wrd_ld_cal]

        if sum(direct_err) != sum(wrd_ld_err):
            err_cases.append([direct_cal, wrd_ld_cal, s, t, e, ss, tt])

        cue_dict_direct = word_dict_of_cue(direct_cal)
        cue_dict_wrd_ld = word_dict_of_cue(wrd_ld_cal)
        sim_dict_direct = merge_word_dicts(sim_dict_direct, cue_dict_direct)
        sim_dict_wrd_ld = merge_word_dicts(sim_dict_wrd_ld, cue_dict_wrd_ld)


    print(f"\nThe following are inconsistent cases:")
    for case in diff_cases:
        print(f"direct_cal = {case[0]}")
        print(f"wrd_ld_cal = {case[1]}")
        print(f"s  = {case[2]}")
        print(f"t  = {case[3]}")
        print(f"e  = {case[4]}")
        print(f"ss = {case[5]}")
        print(f"tt = {case[6]}\n")

    print(f"Skipped cases: {num_examples - len(same_cases) - len(diff_cases)}")
    print(f"Number of consistent cases: {len(same_cases)}")
    print(f"Number of inconsistent cases: {len(diff_cases)}")

    print(f"\nNumber of error cases: {len(err_cases)}")
    for case in err_cases:
        print(f"direct_cal = {case[0]}")
        print(f"wrd_ld_cal = {case[1]}")
        print(f"s  = {case[2]}")
        print(f"t  = {case[3]}")
        print(f"e  = {case[4]}")
        print(f"ss = {case[5]}")
        print(f"tt = {case[6]}\n")

    total_num_err = 0.0
    total_relative_err = 0.0
    for word in dict(sorted(sim_dict_direct.items())):
        occurance, error_direct = sim_dict_direct[word]
        total_num_err += error_direct
        _, error_wrd_ld = sim_dict_wrd_ld[word]
        delta_err = error_direct - error_wrd_ld
        total_err = (error_direct + error_wrd_ld) / 2
        total_num_err += error_wrd_ld
        total_relative_err += delta_err
        relative_err = 2*delta_err / (error_direct + error_wrd_ld)
        print(f"{word = }; {occurance = }; "
              f"total_err: {(total_err):.2f}; "
              f"delta_err: {abs(delta_err):.2f}; "
              f"relative_err: {abs(relative_err):.4f}")

    print(f"Total number of err: {(total_num_err/2):.2f}; "
          f"Sum of error difference: {abs(total_relative_err):.2f}")
