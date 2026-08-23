import itertools

import numpy as np
# import pytest

from salwer.levenshtein import levenshtein


# Parameters used in the simulation
MIN_WORD = 5        # mimimum words in a cue
MAX_WORD = 20       # maximum words in a cue
MAX_NUM_ERR = 4     # maximum number of errs
lower_c = "a b c d e f g h i j k l m n o p q r s t u v w x y z "
ALPHABET = lower_c.split() + lower_c.upper().split()    # alphabet of sim
ALPH_SIZE = len(ALPHABET)                               # size of alphabet
VOCAB = [                       # Vocabulary used for sim
    ''.join(p)
    for k in range(1, 3)
    for p in itertools.product(ALPHABET, repeat=k)
]
VOCAB_SIZE = len(VOCAB)                                 # size of
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


def random_cue(size_of_cue:int, use_large_voc:bool=False) -> list[str]:
    if use_large_voc:
        inds = rng.integers(0, VOCAB_SIZE, size=size_of_cue)
    else:
        inds = rng.integers(0, ALPH_SIZE, size=size_of_cue)
    s = list(np.array(VOCAB)[inds])
    return [str(ele) for ele in s]


def random_size_of_cue() -> int:
    size = rng.integers(MIN_WORD, MAX_WORD+1)       # single draw
    return size


def random_word() -> str:
    ind = rng.integers(0, ALPH_SIZE)
    return VOCAB[ind]
#--------------------------------------------------------------


#--------------------------------------------------------------
# Top level error creation functions
def add_errors(
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
# Other functions
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
