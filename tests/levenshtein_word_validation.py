import csv
from datetime import datetime
import os
from pathlib import Path
import shutil
from typing import List, Tuple

import numpy as np
import pytest

from salwer.levenshtein import (
    levenshtein,
    levenshtein_word,
    levenshtein_gld
)


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
P_S = [0.4, 0.1, 0.2, 0.3]  # Transition prob from sub to other errors
P_D = [0.2, 0.5, 0.0, 0.3]  # Transition prob from del to other errors
P_I = [0.2, 0.0, 0.5, 0.3]  # Transition prob from ins to other errors

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
    s = list(np.array(ALPHABET)[inds])
    return [str(ele) for ele in s]

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



def attribute_wl_gld(
    s:list[str],    # source sequence
    e:list[str],    # error indicator sequence
) -> list[list]:
    m = len(e)
    wlst = [[0.0] * 2 for _ in range(m)]  # wlst = word list

    # Attribute del errors:
    for ind, word in enumerate(e):
        wlst[ind][0] = s[ind]       # assign each element of s
        if word == "D":
            wlst[ind][1] = 1.0

    # Attribute sub only errors:
    sub_inds = find_sub_index(e)
    for inds in sub_inds:
        for ind in range(inds[0], inds[1]):
            wlst[ind][1] = 1.0

    # Attribute sub-ins errors:
    sub_ins_ind_num_sub_list = find_sub_ins_index_num_of_sub(e)
    for sub_ins_ind_num_sub in sub_ins_ind_num_sub_list:
        # length of the entire sub_ins sequence; used for indexes
        len_seq = 1.0 * (sub_ins_ind_num_sub[1] - sub_ins_ind_num_sub[0])
        sub_share = len_seq - 1  # share of blame by the subs.
        if sub_ins_ind_num_sub[2] == 0:  # no subs. in ins. sequence
            if sub_ins_ind_num_sub[0] == 0:        # head insertion
                wlst[sub_ins_ind_num_sub[1]][1] += len_seq
            elif sub_ins_ind_num_sub[1] == m:      # tail insertion
                wlst[sub_ins_ind_num_sub[0] - 1][1] += len_seq
            else:                       # normal insertion
                wlst[sub_ins_ind_num_sub[0] - 1][1] += len_seq/2
                wlst[sub_ins_ind_num_sub[1]][1] += len_seq/2
        else:   # there are subs. in sub-ins sequence
            if sub_ins_ind_num_sub[0] == 0:        # head insertion
                wlst[sub_ins_ind_num_sub[1]][1] += 0.5  # for anchor
                each_share = (sub_share + 0.5) / sub_ins_ind_num_sub[2]
            elif sub_ins_ind_num_sub[1] == m:      # tail insertion
                wlst[sub_ins_ind_num_sub[0] - 1][1] += 0.5
                each_share = (sub_share + 0.5) / sub_ins_ind_num_sub[2]
            else:                       # normal insertion
                wlst[sub_ins_ind_num_sub[0] - 1][1] += 0.5
                wlst[sub_ins_ind_num_sub[1]][1] += 0.5
                each_share = sub_share / sub_ins_ind_num_sub[2]
            # Update LD for elements corresponding to subs.
            for ind in range(sub_ins_ind_num_sub[0], sub_ins_ind_num_sub[1]):
                if e[ind] == "S":
                    wlst[ind][1] += each_share
    # Remove empty elements:
    reduced_wlst = []
    for pair in wlst:
        c, _ = pair[0], pair[1]
        if c != " ":
            reduced_wlst.append(pair)

    return reduced_wlst


# Find the indexes of subs. from the e sequence: Two examples:
# Example 1: subs. w/o ins.:
#    e = ["S", "S", " ", " ", " ", "S", "S", " ", " "]
#  index:  0    1    2    3    4    5    6    7    8
#    exp_ind_lst = [[0, 2], [5, 7]]
#
# Example 2: sub. connected to ins.:
#    e = [" ", "S", " ", "D", " ", "S", "I", " ", "I"]
#  index:  0    1    2    3    4    5    6    7    8
#    exp_ind_lst = [[1, 2]]
def find_sub_index(
    e:list[str],    # error indicator sequence
) -> list[list[int]]:
    m = len(e)
    sub_ind_list = []
    ind = 0
    while ind < m:
        # Skip all spaces and "D"'s.
        while ind < m and (e[ind] == " " or e[ind] == "D"):
            ind += 1
        if ind >= m:
            break

        # Find start and end of sequence of "I" or "S".
        group_start = ind
        has_ins = False
        while ind < m and e[ind] != " " and e[ind] != "D":
            if e[ind] == "I":
                has_ins = True      # sequence with "I"
            ind += 1
        group_end = ind

        if not has_ins:
            sub_ind_list.append([group_start, group_end])
    return sub_ind_list


# Find the indexes of sub.-including ins. plus number of subs: Two examples:
# Example 1: head inserts and consecutive inserts:
#    e = ["I", "I", "S", " ", " ", "I", "S", "I", "S"]
#  index:  0    1    2    3    4    5    6    7    8
#    exp_ind_lst = [[0, 3, 1], [5, 9, 2]]
#
# Example 2: middle insert and tail insert:
#    e = [" ", "S", " ", "D", " ", "S", "I", " ", "I"]
#  index:  0    1    2    3    4    5    6    7    8
#    exp_ind_lst = [[5, 7, 1], [8, 9, 0]]
def find_sub_ins_index_num_of_sub(
    e:list[str],    # error indicator sequence
) -> list[list[int]]:
    m = len(e)
    sub_ins_ind_list = []
    to_find_bgn_sub_ins:bool = True     # flag to find begin index
    num_subs = 0
    num_ins = 0
    for ind, word in enumerate(e):
        if to_find_bgn_sub_ins:
            if word == "S":
                num_subs += 1
                sub_ins_bgn_ind = ind
                to_find_bgn_sub_ins = False   # need to find end index
            elif word == "I":
                num_ins += 1
                sub_ins_bgn_ind = ind
                to_find_bgn_sub_ins = False   # need to find end index
                if ind == m-1:      # find end index at end of list
                    sub_ins_end_ind = ind+1
                    if num_ins:
                        sub_ins_ind_list.append(
                            [sub_ins_bgn_ind, sub_ins_end_ind, num_subs]
                        )
        else:
            if word == " " or word == "D": # find end index before end of list
                sub_ins_end_ind = ind
                to_find_bgn_sub_ins = True
                if num_ins:
                    sub_ins_ind_list.append(
                        [sub_ins_bgn_ind, sub_ins_end_ind, num_subs]
                    )
                num_subs = 0
            else:
                if word == "S":     # find another 'S'
                    num_subs += 1
                elif word == "I":   # find another 'I'.
                    num_ins += 1
                if ind == m-1:      # find end index at end of list
                    sub_ins_end_ind = ind+1
                    if num_ins:
                        sub_ins_ind_list.append(
                            [sub_ins_bgn_ind, sub_ins_end_ind, num_subs]
                        )
    return sub_ins_ind_list


def verify_s_t_e(   # verify the s, t, and e sequences
    s:list[str],    # source sequence
    t:list[str],    # target sequence
    e:list[str],    # error indicator sequence
) -> bool:
    ss = [ele for ele in s if ele != " "]
    tt = [ele for ele in t if ele != " "]
    ee = [ele for ele in e if ele != " "]
    ld_err = levenshtein(ss, tt)
    ee_err = len(ee)
    # print(f"{ld_err = }; {ee_err = }")
    return ld_err == ee_err
