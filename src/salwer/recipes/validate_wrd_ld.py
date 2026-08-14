import csv
from datetime import datetime
import os
from pathlib import Path
import shutil
from typing import List, Tuple

import numpy as np


# Parameters used in the simulation
MIN_WORD = 5        # mimimum words in a cue
MAX_WORD = 20       # maximum words in a cue
MAX_NUM_ERR = 4     # maximum number of errs
lower_c = "a b c d e f g h i j k l m n o p q r s t u v w x y z "
ALPHABET = lower_c.split() + lower_c.upper().split()    # alphabet of sim
ALPH_SIZE = len(ALPHABET)                               # size of alphabet
ERRS = ["sub", "del", "ins"]            # Errors/edits
NEXT = ["sub", "del", "ins", "noe"]     # noe = no error
# All prob lists below are in the order of Prob of sub, del, and ins:
P0 = [0.3, 0.2, 0.5]        # Prob for creating the first error
# PE = 0.7                    # Prob for creating a next error
# P_TS = [0.6, 0.2, 0.2]      # Transition prob from sub to other errors
# P_TD = [0.3, 0.5, 0.2]      # Transition prob from del to other errors
# P_TI = [0.2, 0.1, 0.7]      # Transition prob from ins to other errors
P_S = [0.4, 0.1, 0.2, 0.3]      # Transition prob from sub to other errors
P_D = [0.2, 0.5, 0.0, 0.3]      # Transition prob from del to other errors
P_I = [0.2, 0.0, 0.5, 0.3]      # Transition prob from ins to other errors

rng = np.random.default_rng(42)


#--------------------------------------------------------------
# Lower level error creation functions
def _substitute(
    s:list[str], t:list[str], e:list[str],
    ind_err:int,    # index for the error
) -> tuple[list[str], list[str], list[str], int]:
    err_val = t[ind_err]
    while err_val == s[ind_err]:
        err_val = random_word()
    t[ind_err] = err_val
    e[ind_err] = "S"
    return s, t, e, ind_err


def _delete(
    s:list[str], t:list[str], e:list[str],
    ind_err:int,    # index for the error
) -> tuple[list[str], list[str], list[str], int]:
    t[ind_err] = " "
    e[ind_err] = "D"
    return s, t, e, ind_err


def _insert(
    s:list[str], t:list[str], e:list[str],
    ind_err:int,    # index for the error
) -> tuple[list[str], list[str], list[str], int]:
    len_s = len(s)
    if ind_err == 0:
        err_val = s[ind_err]
        while err_val == s[ind_err]:
            err_val = random_word()
        s = [" "] + s
        t = [err_val] + t
        e = ["I"] + e
    elif ind_err == len_s:
        err_val = s[ind_err-1]
        while err_val == s[ind_err-1]:
            err_val = random_word()
        s = s + [" "]
        t = t + [err_val]
        e = e + ["I"]
    elif ind_err < len_s:
        err_val = t[ind_err]
        while err_val == s[ind_err-1] or err_val == s[ind_err]:
            err_val = random_word()
        s = s[0:ind_err] + [" "] + s[ind_err:]
        t = t[0:ind_err] + [err_val] + t[ind_err:]
        e = e[0:ind_err] + ["I"] + e[ind_err:]
    return s, t, e, ind_err
#--------------------------------------------------------------


#--------------------------------------------------------------
# Mid level error creation functions
def error_type(
    e:list[str],    # sequence of error
    index:int
) -> str:
    mapping = {
        "S": "sub",
        "D": "del",
        "I": "ins",
    }

    if not 0 <= index < len(e):
        raise IndexError(f"Index {index} is out of range")

    try:
        return mapping[e[index]]
    except KeyError:
        raise ValueError(f"Unknown error type: {repr(e[index])}")


def first_error_type() -> str:
    error_type = rng.choice(ERRS, p=P0)  # single draw
    return error_type


def next_error_type(current_err:str) -> str:
    if current_err == "sub":
        return rng.choice(NEXT, p=P_S)
    elif current_err == "del":
        return rng.choice(NEXT, p=P_D)
    elif current_err == "ins":
        return rng.choice(NEXT, p=P_I)
    else:
        raise ValueError(f"Unknown error type in next_error_type()")


def random_cue(size_of_cue:int) -> List[str]:
    inds = rng.integers(0, ALPH_SIZE, size=size_of_cue)
    return np.array(ALPHABET)[inds]


def random_size_of_cue() -> int:
    size = rng.integers(MIN_WORD, MAX_WORD+1)       # single draw
    return size


def random_word() -> str:
    ind = rng.integers(0, ALPH_SIZE)
    return ALPHABET[ind]
#--------------------------------------------------------------


#--------------------------------------------------------------
# Top level error creation functions
def add_error(
    s:list[str],        # source sequence
) -> tuple[list[str], list[str], list[str], int]:
    s, t, e, ind_err = add_first_error(s)
    s, t, e, ind_err, num_err = add_next_error(s, t, e, ind_err)
    return s, t, e, num_err


def add_first_error(
    s:list[str],        # source sequence
) -> tuple[list[str], list[str], list[str], int]:
    len_s = len(s)
    t = s.copy()
    e = [" " for _ in range(len_s)]

    err_type = first_error_type()
    if err_type == "sub":
        ind_err = rng.integers(0, len_s)
        return _substitute(s, t, e, ind_err)
    elif err_type == "del":
        ind_err = rng.integers(0, len_s)
        return _delete(s, t, e, ind_err)
    elif err_type == "ins":
        ind_err = rng.integers(0, len_s+1)  # note the tail
        return _insert(s, t, e, ind_err)
    else:
        raise ValueError("Unknown error from first_error()")


def add_next_error(
    s:list[str],    # source sequence
    t:list[str],    # target sequence
    e:list[str],    # error indicator sequence
    ind_err:int,    # index for the error
    num_err:int = 1,    # number of errors
) -> tuple[list[str], list[str], list[str], int, int]:
    err_type = error_type(e, ind_err)
    next_err_type = next_error_type(err_type)
    if (
        next_err_type == "noe"
        or num_err >= MAX_NUM_ERR
        or ind_err >= len(s) - 1 and (
            next_err_type == "sub" or next_err_type == "del")
    ):
        return s, t, e, ind_err, num_err

    ind_err += 1
    num_err += 1
    if next_err_type == "sub":
        s, t, e, ind_err = _substitute(s, t, e, ind_err)
    elif next_err_type == "del":
        s, t, e, ind_err = _delete(s, t, e, ind_err)
    elif next_err_type == "ins":
        s, t, e, ind_err = _insert(s, t, e, ind_err)
    else:
        raise ValueError("Unknown error from first_error()")

    return add_next_error(s, t, e, ind_err, num_err)
#--------------------------------------------------------------


#--------------------------------------------------------------
# LD calculation functions
#--------------------------------------------------------------
def attribute_errors(
    s:list[str],    # source sequence
    e:list[str],    # error indicator sequence
) -> list[list]:
    m = len(e)
    wlst = [[0] * 2 for _ in range(m)]  # wlst = word list

    # Attribute del and sub errors:
    for ind, word in enumerate(e):
        wlst[ind][0] = s[ind]       # assign each element of s
        if word == "D" or word == "S":
            wlst[ind][1] = 2

    # Attribute insertion errors:
    ins_ind_list = find_insert_index(e)
    for ins_inds in ins_ind_list:
        num_insert = ins_inds[1] - ins_inds[0]
        if ins_inds[0] == 0:        # head insertion
            wlst[ins_inds[1]][1] += 2 * num_insert
        elif ins_inds[1] == m:      # tail insertion
            wlst[ins_inds[0] - 1][1] += 2 * num_insert
        else:                       # normal insertion
            wlst[ins_inds[0] - 1][1] += num_insert
            wlst[ins_inds[1]][1] += num_insert

    # Remove empty elements:
    reduced_wlst = []
    for pair in wlst:
        c, _ = pair[0], pair[1]
        if c != " ":
            reduced_wlst.append(pair)

    return reduced_wlst


# Find the indexes of inserts from the e sequence: Two examples:
# Example 1: head inserts and consecutive inserts:
#    e = ["I", "I", " ", " ", " ", "I", "I", " ", " "]
#  index:  0    1    2    3    4    2    6    7    8
#    exp_ind_lst = [[0, 2], [5, 7]]
#
# Example 2: middle insert and tail insert:
#    e = [" ", "S", " ", "D", " ", "S", "I", " ", "I"]
#  index:  0    1    2    3    4    2    6    7    8
#    exp_ind_lst = [[6, 7], [8, 9]]
# Note that the end index for the later case is off the range.
def find_insert_index(
    e:list[str],    # error indicator sequence
) -> list[list[int]]:
    m = len(e)
    ins_ind_list = []
    to_find_bgn_ins:bool = True     # flag to find begin index
    for ind, word in enumerate(e):
        if to_find_bgn_ins and word == "I":
            ins_bgn_ind = ind
            to_find_bgn_ins = False   # need to find end index
        if not to_find_bgn_ins:
            if word != "I":     # find end index before end of list
                ins_end_ind = ind
                to_find_bgn_ins = True
                ins_ind_list.append([ins_bgn_ind, ins_end_ind])
            if ind == m-1:      # find end index at end of list
                ins_end_ind = ind+1
                ins_ind_list.append([ins_bgn_ind, ins_end_ind])
    return ins_ind_list



def validate_wrd_ld_fun_(num_examples: int):
    """Calculate word-level WER between ref and hyp transcripts.

    Arguments:
    -   num_examples: int = 1000. The number of simulation examples.
    """




    # dir_wrd_dict = {}

    # hyp_dir = Path(hyp_dir)
    # ref_dir = Path(ref_dir)

    # for file in hyp_dir.glob("*.txt"):
    #     if file.is_file():
    #         hyp_file = str(file)
    #         ref_file = str(ref_dir / f"{file.stem}.cns")
    #         file_wrd_dict = word_dict_of_file(
    #             ref_file, hyp_file,
    #             level, fn_cls, seg, err_limit
    #         )
    #         dir_wrd_dict = merge_word_dicts(dir_wrd_dict, file_wrd_dict)

    # os.makedirs('log', exist_ok=True)
    # csv_filename = \
    #     f"log/word-dict-{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.csv"
    # with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
    #     csvfile.write(f"# ref_dir: {ref_dir}\n")
    #     csvfile.write(f"# hyp_dir: {hyp_dir}\n")
    #     csvfile.write(f"# level: {level}\n")
    #     csvfile.write(f"# fn_cls: {fn_cls}\n")
    #     csvfile.write(f"# seg: {seg}\n")
    #     writer = csv.writer(csvfile)
    #     writer.writerow(['Word', 'Occurrence x 2', 'Error x 2', 'WER'])
    #     for word in sorted(dir_wrd_dict.keys(),
    #                        key=lambda w: (-dir_wrd_dict[w][0], w)):
    #         occurance, error = dir_wrd_dict[word]
    #         wer = f"{(error/(2*occurance)):.4f}"
    #         writer.writerow([word, 2*occurance, error, wer])
    # shutil.copy(csv_filename, 'log/word-dict.csv')

    # total_word, total_dist = 0, 0
    # for word in sorted(dir_wrd_dict.keys(),
    #                    key=lambda w: (-dir_wrd_dict[w][0], w)):
    #     total_word += dir_wrd_dict[word][0]
    #     total_dist += dir_wrd_dict[word][1]

    # print(f"\nAverage WER: {(total_dist/(2*total_word)):.4f} "
    #       f"based on {total_word} words. ")



# def word_dict_of_file(
#     ref_file: str,
#     hyp_file: str,
#     level: int,
#     fn_cls: str,
#     seg: str,
#     err_limit: int,
# ):
#     ref_text = read_file_to_text(ref_file)
#     ref_ann = Transcripts.from_ref_cns_text(ref_text, level)
#     hyp_text = read_file_to_text(hyp_file)
#     hyp_ann = Transcripts.from_asr_pred_text(hyp_text)

#     print(f"{ref_file = }; {hyp_file = }------------------------------------")
#     if len(ref_ann.cues) != len(hyp_ann.cues):
#         raise ValueError(
#             f"Num of cues mismatch: {len(ref_ann.cues)} vs {len(hyp_ann.cues)}!"
#         )

#     return word_dict_of_ann(ref_ann, hyp_ann, fn_cls, seg, err_limit)


# def word_dict_of_ann(
#     ref_ann: Transcripts,
#     hyp_ann: Transcripts,
#     fn_cls: str,
#     seg: str,
#     err_limit: int,
# ):
#     file_wrd_dict = {}
#     for i in range(len(ref_ann.cues)):
#         ref_cue = ref_ann.cues[i]
#         hyp_cue = hyp_ann.cues[i]
#         cue_class = _cue_class(ref_cue.cns)
#         if fn_cls != "all" and cue_class != fn_cls:
#             continue

#         ref_cue.txt = _clean_transcript(ref_cue.txt)
#         hyp_cue.txt = _clean_transcript(hyp_cue.txt)
#         cue_wrd_list = levenshtein_word(
#             ref_cue.txt.split(), hyp_cue.txt.split(), err_limit)

#         if seg != "all":
#             cue_seg_ranges = _cue_seg_ranges(ref_cue.txt, ref_cue.cns, seg)
#             cue_wrd_list = _get_seg_wrd_list(cue_wrd_list, cue_seg_ranges)

#         cue_wrd_dict = word_dict_of_cue(cue_wrd_list)
#         file_wrd_dict = merge_word_dicts(file_wrd_dict, cue_wrd_dict)
#     return file_wrd_dict


# def _get_seg_wrd_list(cue_wrd_list, cue_seg_ranges):
#     result = []
#     for start, end in cue_seg_ranges:
#         result.extend(cue_wrd_list[start:end])
#     return result