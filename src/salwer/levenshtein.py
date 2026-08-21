"""Different algs for global, segment-, & word-level Levenshtein edit dist."""


def levenshtein_2d(
        s: list[str],
        t: list[str],
        print_ld: bool = False,
    ) -> int:
    """Full-memory implementation of the DP alg for Levenshtein edit distances.

    Args:
    -   s: list[str]. Source (reference) sequence as list of strings.
    -   t: list[str]. Target (hypothesis) sequence as list of strings.
    -   print_ld: bool = False. Print the LD table if True.

    Return:
    -   The Levenshtein edit distance (LD) between s and t.
    """

    # Initialize the 2D Levenshtein edit distance (LD) table.
    m, n = len(s), len(t)   # sizes of s and t
    d = [[0] * (n+1) for _ in range(m+1)]  # 2D LD table
    for j in range(1, n+1):
        d[0][j] = j         # first row
    for i in range(1, m+1):
        d[i][0] = i         # first column

    # Populate the 2D LD table via the DP alg.
    for i in range(m):          # row index
        for j in range(n):      # col index
            c = 0 if s[i] == t[j] else 1
            d[i+1][j+1] = min(
                d[i][j] + c,    # sub s->t
                d[i][j+1] + 1,  # del of s
                d[i+1][j] + 1,  # ins to s
            )

    if print_ld:    # print the 2D LD table as needed
        print("s\\t      " + '   '.join(t))
        print("     j >")
        i_line = "  i  0 | 1   " + '   '.join(str(num) for num in d[0][2:])
        print(i_line)
        divider = ''.join(["-"] * (len(i_line)-3))
        print("  v " + divider)
        for ch, row in zip(s, d[1:]):
            print(f"{ch}    {row[0]} | "
                  f"{'   '.join(str(num) for num in row[1:])}")

    return d[m][n]  # only return final LD result


def levenshtein(s: list[str], t: list[str]) -> int:
    """Two-list implementation of the DP alg for Levenshtein edit distance.

    Two 1D lists, d0 and d1, are used instead of one 2D list.

    Args:
    -   s: list[str]. Source (reference) sequence as list of strings.
    -   t: list[str]. Target (hypothesis) sequence as list of strings.

    Return:
    -   The Levenshtein edit distance (LD) between s and t.
    """

    # Initialize the 2 1D LD lists.
    m, n = len(s), len(t)     # sizes of s and t
    d0 = list(range(n+1))     # prev LD list
    d1 = [0] * (n+1)          # curr LD list

    for i in range(m):
        # def _update_d1(s, t, d0, d1, i, n):
        d1[0] = i + 1
        for j in range(n):
            c = 0 if s[i] == t[j] else 1
            d1[j+1] = min(
                d0[j] + c,    # sub s->t
                d0[j+1] + 1,  # del of s
                d1[j] + 1,    # ins to s
            )
        # return d1

        d0, d1 = d1, d0       # swap lists

    return d0[n]


def levenshtein_1d(s: list[str], t: list[str]) -> int:
    """Single-list implementation of the DP alg for Levenshtein edit distance.

    A single 1D list, d, is used instead of two 1D lists.

    Args:
    -   s: list[str]. Source (reference) sequence as list of strings.
    -   t: list[str]. Target (hypothesis) sequence as list of strings.

    Return:
    -   The Levenshtein edit distance (LD) between s and t.
    """

    m, n = len(s), len(t)   # sizes of s and t
    d = list(range(n+1))    # for both d0 and d1 above

    for i in range(m):
        d0j = d[0]          # d0[j] above
        d[0] = i + 1        # d1[0] above
        for j in range(n):
            d0j1 = d[j+1]   # d0[j+1] above
            c = 0 if s[i] == t[j] else 1
            d[j+1] = min(
                d0j + c,    # sub s->t
                d0j1 + 1,   # del of s
                d[j] + 1,   # ins to s
            )
            d0j = d0j1

    return d[n]


#--------------------------------------------------------------------
# Levenshtein alignment functions
#--------------------------------------------------------------------

def levenshtein_align_fast(
    s: list[str],
    t: list[str],
    segs: list[list],
) -> list[list]:
    """Segment alignment based on the alignment rules---the fast version.

    See the doc string of the levenshtein_align() function for details.
    """

    m, n = len(s), len(t)   # sizes of s and t
    d0 = list(range(n+1))   # prev LD list
    d1 = [0] * (n+1)        # curr LD list

    n_segs = len(segs)      # num of segments
    # segt = list of segments of t corresponding to segments of s, segs
    segt = [[0] * 2 for _ in range(n_segs)]
    k = 0                   # index of segs/segt

    for i in range(m):
        d1 = _update_d1(s, t, d0, d1, i, n)

        # Amend upper boundary overshoot which happens when the upper
        # boundary, _ind_v_plus_upper, is greater than _ind_v_minus - 1,
        # as shown in x1d1b in test_levenshtein_seg.py
        if k > 0 and segs[k-1][1] == i:  # just above the upper boundary
            ind_v_minus_i = _ind_v_minus_lower(d1) - 1
            if segt[k-1][1] > ind_v_minus_i:
                segt[k-1][1] = ind_v_minus_i
            if k >= n_segs: break

        # Find segment lower boundary for t based on _ind_v_minus_lower(d1).
        if segs[k][0] == i:
            segt[k][0] = _ind_v_minus_lower(d1) - 1

        # Find segment upper boundary for t based on ind_v_plus_upper(d1).
        if segs[k][1] == i + 1:
            segt[k][1] = _ind_v_plus_upper(d1)
            k += 1          # update the segment index

        d0, d1 = d1, d0

    return segt


def levenshtein_align(
    s: list[str],
    t: list[str],
    segs: list[list],
) -> list[list]:
    """Segment alignment with prefix drift removed---the normal version.

    Notations:
    -   d0: The Levenshtein distance of the previous iteration.
    -   d1: The Levenshtein distance of the current iteration.

    In the comments of the code and test case illustrations, we use notations
    for the following (here 2 is just an example; it can be any number):
    -   2-: They are the min value of d1 with the max index. They are for the
            lower boundary of a segment only. They are referred to as
            v_minus, and the corresponding index is called ind_v_minus.
    -   2+: They are also the min values of d1 with the max index. Yet, they
            are for the upper bounbdary of a segment only. They are referrred
            to as v_plus, and the corresponding index is called ind_v_plus.

    Args:
    -   s: Source (reference) sequence as list of strings.
    -   t: Target (hypothesis) sequence as list of strings.
    -   segs: list of semantic segments of s, each segment is [start, end].

    Return:
    -   segt: list of aligned segments of t, each corresponds to a segment
            in segs; so it has the same dimension as segs.
    """

    m, n = len(s), len(t)   # sizes of s and t
    d0 = list(range(n+1))   # prev LD list
    d1 = [0] * (n+1)        # curr LD list

    n_segs = len(segs)      # num of segments
    # segt = list of segments of t corresponding to segments of s, segs
    segt = [[0] * 2 for _ in range(n_segs)]
    k = 0                   # index of segs/segt

    check_shift = True      # flag for checking shift
    ss = 0   # sequence s' total shift due to update of s
    ts = 0   # sequence t's total shift; counterpart of ss

    while True:
        for i in range(m):
            # Check the prefix drift at the lower boundary of each segment.
            if  check_shift and k < n_segs and segs[k][0] == ss + i:
                # n_pd: num of prefix drift (leading ins of t compared to s).
                # r, h: sub sequences in s and t for prefix drift checking.
                n_pd, r, h = _prefix_drift_rh(s, t, i, d0)
                if n_pd:
                    # t_ind: t's index used for prefix drift checking.
                    t_ind = _ind_v_plus_lower(d0)
                    ts = ts + t_ind + n_pd  # needed for alignment
                    # update s and t and related vars for a new "for i loop"
                    s, t, m, n, d0, d1, ss, i = \
                        _update_st_vars(r, h, n_pd, ss, i)
                    check_shift = False     # no check again for this boundary
                    break

            d1 = _update_d1(s, t, d0, d1, i, n)

            # Amend upper boundary overshoot; see comments of fast version.
            if k > 0 and segs[k-1][1] == ss + i:  # just above upper boundary
                ind_v_minus_i = _ind_v_minus_lower(d1) - 1 + ts
                if segt[k-1][1] > ind_v_minus_i:
                    segt[k-1][1] = ind_v_minus_i
                if k >= n_segs: return segt  # done with all segs; exit

            # Find segment lower boundary for t, which is _ind_v_star(d1).
            if segs[k][0] == ss + i:
                segt[k][0] = _ind_v_star(d1) + ts

            # Find segment upper boundary for t based on ind_v_plus_upper(d1).
            if segs[k][1] == ss + i + 1:
                segt[k][1] = _ind_v_plus_upper(d1) + ts
                k += 1               # update the segment index
                check_shift = True   # get ready for prefix drift checking

            d0, d1 = d1, d0

        if k >= n_segs: return segt


#--------------------------------------------------------------------
# Segment-level Levenshtein edit distance calculation functions
#--------------------------------------------------------------------

def levenshtein_seg_fast(
    s: list[str],
    t: list[str],
    segs: list[list],
    tight: bool = True,
) -> list[list]:
    """Segment size and LD calculation---the fast version.

    See the doc string of the levenshtein_seg function.
    """

    base_seg_dist = _v_star if tight else _v_plus

    m, n = len(s), len(t)   # sizes of s and t
    d0 = list(range(n+1))   # prev LD list
    d1 = [0] * (n+1)        # curr LD list

    n_segs = len(segs)      # num of segments
    # segd = segment size and LD corresponding to segs
    segd = [[0] * 2 for _ in range(n_segs)]
    k = 0                   # index of segs/segt

    base_dist = 0   # base dist: v_plus or v_star

    for i in range(m):
        d1 = _update_d1(s, t, d0, d1, i, n)

        # Find the base dist at the segment lower boundary.
        if segs[k][0] == i:
            base_dist = base_seg_dist(d0, d1)

        # Find the seg size and LD at the segment upper boundary.
        if segs[k][1] == i + 1:
            segd[k][0] = segs[k][1] - segs[k][0]        # seg size
            segd[k][1] = _v_plus_upper(d1) - base_dist  # seg dist
            k += 1                  # update the segment index
            if k >= n_segs: break

        d0, d1 = d1, d0

    return segd


def levenshtein_seg(
    s: list[str],
    t: list[str],
    segs: list[list],
    tight: bool = True,
) -> list[list]:
    """Calculate size and Levenshtein dist of segments---the normal version.

    Notations:
    -   d0: The Levenshtein distance of the previous iteration.
    -   d1: The Levenshtein distance of the current iteration.

    In the comments of the code and test case illustrations, we use notations
    for the following (here 2 is just an example; it can be any number):
    -   2-: They are the min value of d1 with the max index. They are for the
            lower boundary of a segment only. They are referred to as
            v_minus, and the corresponding index is called ind_v_minus.
    -   2+: They are also the min values of d1 with the max index. Yet, they
            are for the upper bounbdary of a segment only. They are referrred
            to as v_plus, and the corresponding index is called ind_v_plus.
    -   *2: They are the value of d0 with index (ind_v_minus - 1). The value
            is referred to as v_star, and the index is ind_v_star. Used in
            segment-level LD calculation.

    Args:
    -   s: Source (reference) sequence as list of strings.
    -   t: Target (hypothesis) sequence as list of strings.
    -   segs: list of semantic segments, each segment is [start, end].
    -   tight: Boolean indicator for including prefix drift (PD, or
        hallucination) before each segment or not:
        -   True: Use tight segmemts---do not include PD (default).
        -   False: Do not use tight segments---do include PD.

    Returns:
    -   segd: segment-based result---a list of [seg_size, seg_LD] for
            all provided segments in segs. For each list:
        -   seg_size (= end - start),
        -   edit_LD between s[start:end] and the correcponding t sequence.
    """

    m, n = len(s), len(t)   # sizes of s and t
    d0 = list(range(n+1))   # prev LD list
    d1 = [0] * (n+1)        # curr LD list

    n_segs = len(segs)      # num of segments
    # segd = list of segment size and LD corresponding to segs
    segd = [[0] * 2 for _ in range(n_segs)]
    k = 0                   # index of segs/segt

    base_dist = 0           # base dist: v_plus

    check_shift = True      # flag for checking shift
    ss = 0                  # base index for s

    while True:
        for i in range(m):
            # Check the prefix drift at the lower boundary of each segment.
            if check_shift and segs[k][0] == ss + i:
                # n_pd: num of prefix drift (leading ins of t compared to s).
                # r, h: sub sequences in s and t for prefix drift checking.
                n_pd, r, h = _prefix_drift_rh(s, t, i, d0)
                if n_pd:
                    # update s and t and related vars for a new "for i loop"
                    s, t, m, n, d0, d1, ss, i = \
                        _update_st_vars(r, h, n_pd, ss, i)
                    check_shift = False     # no check again for this boundary
                    break

            d1 = _update_d1(s, t, d0, d1, i, n)

            # Find the base dist at the segment lower boundary.
            if segs[k][0] == ss + i:
                base_dist = min(d0)

            # Find the seg size and dist at the segment upper boundary.
            if segs[k][1] == ss + i + 1:
                segd[k][0] = segs[k][1] - segs[k][0]    # seg size
                segd[k][1] = min(d1) - base_dist        # seg LD
                if not tight: segd[k][1] += n_pd        # seg LD
                check_shift = True   # get ready for prefix drift checking
                k += 1
                if k >= n_segs: return segd

            d0, d1 = d1, d0


#--------------------------------------------------------------------
# Word-level Levenshtein edit distance calculation functions
#--------------------------------------------------------------------

def levenshtein_word_fast(
    s: list[str],
    t: list[str],
) -> list[list]:
    """Levenshtein dist of each word w/o examining errors---the fast version.

    This function calculates the 'raw' word-level levenshtein distance.
    The meaning of raw is two fold:

    1.  The errors (distance being one for a word) are not examined for type.
            Insertions (hallucination) can lead to issues with other words.
    2.  The error due to a hallucination is only considered as prefix drift.

    Args:
    -   s: Source (reference) sequence as list of strings.
    -   t: Target (hypothesis) sequence as list of strings.

    Returns:
    -   wlst: Word list---a list of [word, levenshtein_dist] for each word,
        where levenshtein_dist is 0 or 1.
    """

    m, n = len(s), len(t)   # sizes of s and t
    d0 = list(range(n+1))   # prev LD list
    d1 = [0] * (n+1)        # curr LD list

    # wlst = word list [[word1, LD1], ..., [wordm, LDm]]
    wlst = [[0] * 2 for _ in range(m)]
    min_d0 = 0      # v_plus, base_dist of the seg version

    for i in range(m):
        d1 = _update_d1(s, t, d0, d1, i, n)

        wlst[i][0] = s[i]             # word in s
        min_d1 = min(d1)              # _v_plus_upper(d1)
        wlst[i][1] = min_d1 - min_d0  # LD of word

        d0, d1, min_d0 = d1, d0, min_d1

    return wlst


def levenshtein_gld(
    s: list[str],
    t: list[str],
    err_limit: float = 3.0,
) -> list[list[str, float]]:
    """Generalized Levenshtein dist (GLD) of each word with errors clipped.

    Rules for calculate the GLD for each word:
    See the "Word-level LD calculation algorithm" section of the paper.

    Args:
    -   s: Source (reference) sequence as list of strings.
    -   t: Target (hypothesis) sequence as list of strings.
    -   err_limit: Upper limit of the error for each word.

    Returns:
    -   wlst: Word list---list of [word, GLD] for each word in s; GLD is float.
    """

    s, t, fwlst, pwlst, ld_4_ank = _check_st_tails(s, t)
    if len(fwlst) > 0:
        return fwlst

    m, n = len(s), len(t)   # sizes of s and t
    d0 = list(range(n+1))   # prev LD list
    d1 = [0] * (n+1)        # curr LD list

    wlst = [[0] * 2 for _ in range(m)]  # wlst = word list
    min_d0 = 0  # v_plus, base_dist of the seg version

    ss = 0      # base index for s
    mc = m      # copy of m used in loop control

    while True:
        for i in range(m):
            d1 = _update_d1(s, t, d0, d1, i, n)

            # Assign word and update its LD to word list, wlst.
            wlst[ss+i][0] = s[i]    # word of s
            min_d1 = min(d1)        # _v_plus_upper(d1)
            dist = min_d1 - min_d0  # LD of word
            # use update since the value may have been assigned in (1) in
            wlst[ss+i][1] += dist / 2.0  # 0 or 0.5     previous for i loop
            d0, d1, min_d0 = d1, d0, min_d1

            if dist == 0: continue

            # If dist is 1, check if it is caused by prefix drift or others
            n_pd, n_sub, r, h = _prefix_drift_sub_rh(s, t, i, d1)  # d1 => d0
            if n_pd:    # dist caused by prefix drift (ins.)
                if n_sub == 0:  # the case with ins. only
                    hf_pd = 0.5 * n_pd  # blamed for half errors
                    if ss+i == 0:       # head ins. (at start of the seq)
                        wlst[0][1] = 2.0 * hf_pd    # (1) assign full blame
                    else:
                        wlst[ss+i-1][1] += hf_pd    # add to left anchor
                        wlst[ss+i][1] = hf_pd       # (1) assign to right anchor
                else:           # the case with mixed ins. and subs.
                    len_seq = n_pd + n_sub
                    if ss+i == 0:       # head ins.
                        wlst[n_sub][0] = s[n_sub]   # right anchor
                        wlst[n_sub][1] = 0.5        # (1) right anchor
                        avg_share = (len_seq - 0.5) / n_sub  # average share
                    else:
                        wlst[ss+i-1][1] += 0.5      # add to left anchor
                        wlst[ss+i+n_sub][0] = s[i+n_sub]
                        wlst[ss+i+n_sub][1] = 0.5   # (1) assign to right anchor
                        avg_share = (len_seq - 1.0) / n_sub  # average share
                    # Update LD for elements corresponding to subs.
                    for ii in range(n_sub):
                        wlst[ss+i+ii][0] = s[i+ii]
                        wlst[ss+i+ii][1] = avg_share
                # update s and t and related vars for a new "for i loop"
                s, t, m, n, d0, d1, ss, i = \
                    _update_sub_st_vars(r, h, n_pd, n_sub, ss, i)
                min_d0 = 0
                break
            else:   # dist caused by sub. or del.
                wlst[ss+i][1] += 0.5    # word-level LD = 1.0 now

        if ss + i >= mc - 1:        # all elements of s scanned
            wlst[mc-1][1] += ld_4_ank
            wlst = wlst + pwlst     # tail resulets appended here

            wlst = _clip_wlst_err(wlst, err_limit)
            return wlst


def levenshtein_word2(
    s: list[str],
    t: list[str],
    err_limit: int = 5,
) -> list[list]:
    """Levenshtein dist of each word with errors examined---the normal version.

    This function calculates the word-level levenshtein distance in a 'refined'
    way as compared to levenshtein_word_fast. The meaning of `refinement`
    is multi-fold:
    1.  Each error (Levenshtein dist being 1 for a word) is tested to see if
        it is an insertion (also called prefix drift or hallucination).
    2.  If tested as a prefix hallucination, the 'blame' is split to
        the two words on the two sides of the hallucination.
    3.  If the word is at the beginning of the source, all prefix
        hallucinations will be blamed to this word.
    4.  If the word is at the end of the source, all the surfix hallucinations
        will be blamed to this word.

    Note that:
    1.  Due to the splitting of error, we need to DOUBLE the value of
        the Levenshtein distance for easy processing and testing.
    2.  We need to use an error limit to so that a long hallucination
        will not skew the word-level WER too much.

    Args:
    -   s: Source (reference) sequence as list of strings.
    -   t: Target (hypothesis) sequence as list of strings.
    -   err_limit: Upper limit of the error for each word (in the double case).

    Returns:
    -   wlst: Word list---a list of [word, levenshtein_dist] for each word,
        where levenshtein_dist is an integer, assuming values 0, 1, 2, ...
    """

    # Find the number of suffix drifts and remove the tail from t
    num_sd = _num_suffix_drift(s, t)
    if num_sd:
        t = t[:-num_sd]

    m, n = len(s), len(t)   # sizes of s and t
    d0 = list(range(n+1))   # prev LD list
    d1 = [0] * (n+1)        # curr LD list

    wlst = [[0] * 2 for _ in range(m)]  # wlst = word list
    min_d0 = 0      # v_plus, base_dist of the seg version

    ss = 0      # base index for s
    mc = m      # copy of m used in loop control

    while True:
        for i in range(m):
            d1 = _update_d1(s, t, d0, d1, i, n)

            # Assign word and update its LD to word list, wlst.
            wlst[ss+i][0] = s[i]      # word of s
            min_d1 = min(d1)          # _v_plus_upper(d1)
            dist = min_d1 - min_d0    # LD of word
            # use update since the value may have been assigned in (1) in
            wlst[ss+i][1] += dist     # 0 or 1          previous for i loop
            d0, d1, min_d0 = d1, d0, min_d1

            if dist == 0: continue

            # If dist is 1, check if it is caused by prefix drift.
            n_pd, r, h = _prefix_drift_rh(s, t, i, d1)  # d1 is actually d0
            if n_pd:
                wlst[ss+i][1] = n_pd         # (1) assign num of prefix drifts
                if ss+i == 0:
                    wlst[ss+i][1] += n_pd    # add again for s[0]
                else:
                    wlst[ss+i-1][1] += n_pd  # share blame with neighbor
                # update s and t and related vars for a new "for i loop"
                s, t, m, n, d0, d1, ss, i =  _update_st_vars(r, h, n_pd, ss, i)
                min_d0 = 0
                break
            else:  # substitution or deletion
                wlst[ss+i][1] += 1  # seg dist = 2 now

        if ss + i >= mc - 1:  # all elements of s scanned
            wlst[mc-1][1] += 2 * num_sd
            wlst = _clip_wlst_err(wlst, err_limit)
            return wlst


#--------------------------------------------------------------------
# Common Utility/Helper functions
#--------------------------------------------------------------------

# Check the s and t sequences t tails and return a tuple of results.
def _check_st_tails(
    s: list[str], t: list[str]
) -> tuple[list[str], list[str], list[list], list[list], float]:
    fwlst, pwlst = [], []   # full and partial word lists
    ld_4_ank = 0.0          # LD for last anchor

    # Case 1. The two sequences are not related. Form fwlst with 1.0.
    # In caller, if fwlst is not empty, content is used as-is, then return.
    m, n = len(s), len(t)
    dist0 = levenshtein(s, t)
    if dist0 >= max(m, n):
        fwlst = [[w, 1.0] for w in s]
        return s, t, fwlst, pwlst, ld_4_ank

    # Case 2. Last elements are aligned. No need to do anything.
    if s[-1] == t[-1]:
        return s, t, fwlst, pwlst, ld_4_ank

    # Now, we will have the tails checked for further cases.
    r = s[::-1]
    h = t[::-1]
    i = 0       # number of subs. in sequence of subs. & ins.

    # Check positive suffix drift.
    pos_sd = _num_prefix_drift(r, h)    # positive suffix drift
    if pos_sd:      # Case 3. h has ins. at the start of the seq.
        # Check if there are any subs. in the ins. sequence.
        while i < m and pos_sd + i < n and r[i] != h[pos_sd + i]:
            i += 1
        if i == m or pos_sd + i == n:   # cannot find matched element
            # Case 3a. Something is wrong: we have pos_sd, but no matching.
            # Here is just an issue catching processing. Return like Case 1.
            fwlst = [[w, 1.0] for w in s]
            return s, t, fwlst, pwlst, ld_4_ank
        if i == 0:
            # Case 3b. No subs.
            ld_4_ank = 1.0 * pos_sd     # all blame will be on last anchor
            t = t[: -pos_sd]            # remove tail of t (the suffix drift)
        else:               # with subs.
            # Case 3c. Has subs. in the ins. sequence.
            ld_4_ank = 0.5              # last anchor only blamed slightly
            avg_ld = (pos_sd + i - 0.5) / i  # each sub's average share of LD
            pwlst = [[w, avg_ld] for w in r[: i]]
            pwlst = pwlst[::-1]         # partial wlst in correct order
            s = s[: -i]         # remove tail of s (the subs.)
            t = t[: -pos_sd-i]  # remove tail of t (the suffix drift & subs.)
        return s, t, fwlst, pwlst, ld_4_ank

    # Check negative suffix drift.
    neg_sd = _num_prefix_drift(h, r)    # negative suffix drift
    if neg_sd:      # Case 4. r has ins. at the start of the seq.
        # Check if there are any subs. in the ins. sequence.
        while i < n and neg_sd + i < m and h[i] != r[neg_sd + i]:
            i += 1
        if i == n or neg_sd + i == m:   # cannot find matched element
            # Case 4a. Something is wrong: we have neg_sd, but no matching.
            # Same handling as Case 3a.
            fwlst = [[w, 1.0] for w in s]
            return s, t, fwlst, pwlst, ld_4_ank
        if i == 0:
            # Case 4b. No subs.
            s = s[: -neg_sd]            # remove tail of s (the suffix drift)
        else:       # with subs.
            # Case 4c. Has subs. in the ins. sequence.
            s = s[: -neg_sd-i]  # remove tail of s (the suffix drift & subs.)
            t = t[: -i]         # remove tail of t (the subs.)
        # Each element at the tail of s blamed for sub. or del.
        pwlst = [[w, 1.0] for w in r[: neg_sd + i]]
        pwlst = pwlst[::-1]
        return s, t, fwlst, pwlst, ld_4_ank

    # Case 5. Both pos_sd and neg_sd are 0 => only subs.
    while i < n and i < m and h[i] != r[i]:
        i += 1
    if i == n or i == m:   # cannot find matched element
        # Case 5a. Something is wrong: we have no matching.
        # Same handling as Cases 3a and 4a.
        fwlst = [[w, 1.0] for w in s]
        return s, t, fwlst, pwlst, ld_4_ank
    else:           # with subs.
        # Case 5b. Has a subs. Same handling as Case 4b.
        pwlst = [[w, 1.0] for w in r[: i]]
        pwlst = pwlst[::-1]
        s = s[: -i]
        t = t[: -i]
    return s, t, fwlst, pwlst, ld_4_ank


# Find the max index of the min value of a list.
def _clip_wlst_err(wlst, err_limit):
    for word_err in wlst:
        word_err[1] = min(word_err[1], err_limit)
    return wlst


# Find the num of prefix drifts (insertion or hallucination words) of s & t.
def _num_prefix_drift(s: list[str], t: list[str]) -> int:
    shift = 0
    dist0 = levenshtein(s, t)
    dist1 = levenshtein(s, t[1:])
    while dist0 > dist1:
        shift += 1
        dist0 = dist1
        dist1 = levenshtein(s, t[shift+1:])
    return shift


# Find the num of suffix drifts (insertion or hallucination words) of s & t.
def _num_suffix_drift(s: list[str], t: list[str]) -> int:
    reversed_s = s[::-1]
    reversed_t = t[::-1]
    return _num_prefix_drift(reversed_s, reversed_t)


# Find the num of prefix drifts and new s & t sequences.
def _prefix_drift_rh(s, t, s_ind, d0):
    t_ind = _ind_v_plus_lower(d0)
    r = s[s_ind:]           # r = ref, partial source
    h = t[t_ind:]           # h = hyp, partial target
    n_pd = _num_prefix_drift(r, h)
    return n_pd, r, h


# Find the num of prefix drifts, num of subs., and new s & t sequences.
def _prefix_drift_sub_rh(s, t, s_ind, d0):
    t_ind = _ind_v_plus_lower(d0)
    r = s[s_ind:]           # r = ref, partial source
    h = t[t_ind:]           # h = hyp, partial target
    n_pd = _num_prefix_drift(r, h)  # number of prefix drifts
    i = 0                   # number of subs. in sequence of subs. & ins.
    if n_pd:
        m, n = len(r), len(h)
        while i < m and n_pd + i < n and r[i] != h[n_pd + i]:
            i += 1
    return n_pd, i, r, h


# Update list d1 for Levenshtein distance.
# Direct implementation can be found in the levenshtein() function.
def _update_d1(s, t, d0, d1, i, n):
    d1[0] = i + 1
    for j in range(n):
        c = 0 if s[i] == t[j] else 1
        d1[j+1] = min(
            d0[j] + c,      # sub s->t
            d0[j+1] + 1,    # del of s
            d1[j] + 1,      # ins to s
        )
    return d1


# Update s and t sequences and related variables used when reset everthing.
# Needed when we have leading hallucinations of t against s.
def _update_st_vars(r, h, n_pd, ss, i):
    s = r                   # source
    t = h[n_pd:]            # target
    m, n = len(s), len(t)   # sizes
    d0 = list(range(n+1))   # prev dist
    d1 = [0] * (n+1)        # curr dist
    ss += i                 # base index for s
    i = 0                   # index for s
    return s, t, m, n, d0, d1, ss, i


# Update s and t sequences and related variables used when reset everthing.
# Needed when we have leading hallucinations of t against s.
def _update_sub_st_vars(r, h, n_pd, n_sub, ss, i):
    s = r[n_sub:]           # source
    t = h[n_pd + n_sub:]    # target
    m, n = len(s), len(t)   # sizes
    d0 = list(range(n+1))   # prev dist
    d1 = [0] * (n+1)        # curr dist
    ss = ss + n_sub + i     # base index for s
    i = 0                   # index for s
    return s, t, m, n, d0, d1, ss, i


#--------------------------------------------------------------------
# Utility/Helper functions for special value and index
#--------------------------------------------------------------------

# Find the max index of the min value of a list.
def _max_ind_of_min(d: list[int]) -> int:
    min_val = min(d)
    ind = [i for i, x in enumerate(d) if x == min_val]
    return max(ind)


# # Find v_minus at the lower boundary.
# def _v_minus_lower(d1):
#     return min(d1)


# Find index of v_minus at the lower boundary.
def _ind_v_minus_lower(d1):
    return _max_ind_of_min(d1)


# # Find v_plus at the lower boundary.
# def _v_plus_lower(d0):
#     return min(d0)


# Find index of v_plus at the lower boundary.
def _ind_v_plus_lower(d0):
    return _max_ind_of_min(d0)


# Find v_plus at the upper boundary.
def _v_plus_upper(d1):
    return min(d1)


# Find index of v_plus at the upper boundary.
def _ind_v_plus_upper(d1):
    return _max_ind_of_min(d1)


# Calculate v_plus used for obtaining seg LD in non-tight way.
def _v_plus(d0, d1):  # used for obtaining seg LD not tightly
    return min(d0)


# Define function base_seg_dist for calculate the seg distance.
def _v_star(d0, d1):  # used for obtaining seg LD tightly
    return d0[_ind_v_star(d1)]


# Find index of v_plus at the lower boundary of a segment.
def _ind_v_star(d1):
    return _max_ind_of_min(d1) - 1
