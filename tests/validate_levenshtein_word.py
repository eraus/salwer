"""Test function used for validating word-level LD function."""

import numpy as np

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
from .helpers import word_dict_approx_eq, word_list_approx_eq


def test_validate_wrd_ld_fun(request):
    """Validate the word-level GLD function levenshtein_gld.

    Ground truth (gdt) = Result from attribute_wl_gld
    Hyphothsis (hyp) = Result from levenshtein_gld
    To run it, use:
    pytest tests/validate_levenshtein_word.py --num-trials 10000

    Default value of the --num-trials option is 1000.
    """

    num_trials = request.config.getoption("--num-trials")
    # Numerical numbers correspond to Case number, used in the for i loop.
    num1_skipped = 0
    num2_same_cases, same_cases = 0, []
    num3_same_dict_cases, same_dict_cases = 0, []
    num4_diff_dict_cases, diff_dict_cases = 0, []
    num5_more_err_cases, more_err_cases = 0, []

    gdt_dict_sim = {}
    hyp_dict_sim = {}
    total_gld, more_gld = 0.0, 0.0

    for i in range(num_trials):
        s0 = random_cue(random_size_of_cue())       # base s sequence
        s, t, e, _ = add_errors(s0)     # aligned s and t seqs with err seq
        s_ns = [ele for ele in s if ele != " "]     # s seq; ns = no space
        t_ns = [ele for ele in t if ele != " "]     # t seq w/o space element

        if not verify_s_t_e(s, t, e):
    # Case 1: Skip the trial if Global LD is not the same as sum(GDT LD).
            num1_skipped += 1
            continue

        # Find GDT and HYP word lists:
        gdt_wlst = attribute_wl_gld(s, e)
        hyp_wlst = levenshtein_gld(s_ns, t_ns, err_limit=100)

        # Collect GDT and HYP word dicts:
        gdt_dict = word_dict_of_cue(gdt_wlst)
        hyp_dict = word_dict_of_cue(hyp_wlst)
        gdt_dict_sim = merge_word_dicts(gdt_dict_sim, gdt_dict)
        hyp_dict_sim = merge_word_dicts(hyp_dict_sim, hyp_dict)

        gdt_gld = [idem[1] for idem in gdt_wlst]
        total_gdt_gld = sum(gdt_gld)
        total_gld += total_gdt_gld

        if word_list_approx_eq(gdt_wlst, hyp_wlst):  # GDT WLST == HYP WLST
    # Case 2: GDT and HYP word lists are the same
            num2_same_cases += 1
            same_cases.append(gdt_wlst)
        else:       # GDT WLST != HYP WLST; check further
            if word_dict_approx_eq(gdt_dict, hyp_dict):  # Same word dict
    # Case 3: GDT and HYP word lists differ but dicts are the same
                num3_same_dict_cases += 1
                same_dict_cases.append(
                    [gdt_wlst, hyp_wlst, s, t, e, s_ns, t_ns])
            else:
    # Case 4: GDT and HYP word dicts differ but HYP has no additional errs
                num4_diff_dict_cases += 1
                diff_dict_cases.append(
                    [gdt_wlst, hyp_wlst, s, t, e, s_ns, t_ns])

                hyp_gld = [item[1] for item in hyp_wlst]
                total_hyp_gld = sum(hyp_gld)
                if not -0.01 < total_gdt_gld - total_hyp_gld < 0.01:
    # Case 5: HYP word dict has more errors than GDT word dict
                    num5_more_err_cases += 1
                    more_gld = more_gld + total_hyp_gld - total_gdt_gld
                    more_err_cases.append(
                        [gdt_wlst, hyp_wlst, s, t, e, s_ns, t_ns])

    # Print final results:
    print("\nTrials that have different word lists but same word dicts:")
    _print_trial_cases(same_dict_cases)
    print("\n\nTrials that have different word dicts:")
    _print_trial_cases(diff_dict_cases)
    print("\n\nTrials that have additional GLD:")
    _print_trial_cases(more_err_cases)

    print("Summary of results---------------------------------------------")
    print(f"Total number of trials: {num_trials}")
    print(f"Total number of skipped cases: {num1_skipped}")
    print(f"Total number of consistent cases: {num2_same_cases}")
    print(f"Total num of diff list / same dict cases: {num3_same_dict_cases}")
    print(f"Total num of diff dict cases: {num4_diff_dict_cases}")
    print(f"Total num of additional err cases: {num5_more_err_cases}")
    print(f"Total ground truth GLD: {(total_gld):.2f}; "
          f"Total addition errors: {more_gld:.2f}")

    print("\nSummary of statistics----------------------------------")
    # wer = np.array
    for word in dict(sorted(gdt_dict_sim.items())):
        word_occ, word_gdt_gld = gdt_dict_sim[word]
        _, word_hyp_gld = hyp_dict_sim[word]
        delta_err = word_hyp_gld - word_gdt_gld
        relative_err = delta_err / word_gdt_gld if word_gdt_gld != 0 else 0.0
        print(f"{word = };  {word_occ = };  "
              f"word GLD = {(word_gdt_gld):7.2f};  "
              f"delta GLD = {(delta_err):5.2f};  "
              f"relative GLD = {(relative_err):7.4f}")


def _print_trial_cases(case_list):
    for case in case_list:
        print(f"gdt_wlst = {case[0]}")
        print(f"hyp_wlst = {case[1]}")
        print(f"s  = {case[2]}")
        print(f"t  = {case[3]}")
        print(f"e  = {case[4]}")
        print(f"ss = {case[5]}")
        print(f"tt = {case[6]}\n")
