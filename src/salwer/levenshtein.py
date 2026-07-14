from typing import List

# To be removed later
def seg_size_n_edit_distance(
    segs: List[List],
    ref: List[str],
    hyp: List[str],
) -> List[List]:
    raise ValueError("seg_size_n_edit_distance is not defined.")

#--------------------------------------------------------------------
# Different implementation of the Levenshtein algorithm
#--------------------------------------------------------------------

def levenshtein_2d(
        s: List[str],
        t: List[str],
        print_ld: bool = False,
    ) -> int:
    """Full-memory implementation of the Levenshtein distance alg.

    Args:
    -   s: List[str]. Source (reference) sequence as list of strings.
    -   t: List[str]. Target (hypothesis) sequence as list of strings.
    -   print_ld: bool = False. Print the Levenshtein dist (LD) table if True.

    Return:
    -   The Levenshtein distance between s and t.
    """

    # Initialize the 2D Levenshtein distance (LD) table
    m, n = len(s), len(t)   # sizes of s and t
    d = [[0] * (n+1) for _ in range(m+1)]  # 2D LD table
    for i in range(1, m+1):
        d[i][0] = i
    for j in range(1, n+1):
        d[0][j] = j

    # Populate the 2D LD table
    for i in range(m):          # row index
        for j in range(n):      # col index
            c = 0 if s[i] == t[j] else 1
            d[i+1][j+1] = min(
                d[i][j] + c,    # sub s->t
                d[i][j+1] + 1,  # del of s
                d[i+1][j] + 1,  # ins to s
            )

    # Populate the 2D LD table as needed
    if print_ld:
        print("s\\t      " + '   '.join(t))
        print("     j >")
        i_line = "  i  0 | 1   " + '   '.join(str(num) for num in d[0][2:])
        print(i_line)
        divider = ''.join(["-"] * (len(i_line)-3))
        print("  v " + divider)
        for ch, row in zip(s, d[1:]):
            print(f"{ch}    {row[0]} | "
                  f"{'   '.join(str(num) for num in row[1:])}")

    # Only return the final LD result
    return d[m][n]


def levenshtein(s: List[str], t: List[str]) -> int:
    """Two-list implementation of the Levenshtein distance alg.

    Two 1D lists, d0 and d1, are used instead of a 2D list.

    Args:
    -   s: List[str]. Source (reference) sequence as list of strings.
    -   t: List[str]. Target (hypothesis) sequence as list of strings.

    Return:
    -   The Levenshtein distance between s and t.
    """

    # Initialize the 2 1D LD lists.
    m, n = len(s), len(t)     # sizes of s and t
    d0 = list(range(n+1))     # prev LD dist
    d1 = [0] * (n+1)          # curr LD dist

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


def levenshtein_1d(s: List[str], t: List[str]) -> int:
    """Single-list implementation of the Levenshtein distance alg.

    A single 1D list, d, is used instead of 2 1D lists.

    Args:
    -   s: List[str]. Source (reference) sequence as list of strings.
    -   t: List[str]. Target (hypothesis) sequence as list of strings.

    Return:
    -   The Levenshtein distance between s and t.
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
    s: List[str],
    t: List[str],
    segs: List[List],
) -> List[List]:
    """Segment alignment based on the alignment rules---the fast version.

    See the doc string of the levenshtein_align() function for details.
    """

    m, n = len(s), len(t)   # sizes of s and t
    d0 = list(range(n+1))   # prev LD dist
    d1 = [0] * (n+1)        # curr LD dist

    n_segs = len(segs)      # num of segments
    # segt = segments of t corresponding to segments of s: segs
    segt = [[0] * 2 for _ in range(n_segs)]
    k = 0                   # index of segs/segt

    for i in range(m):
        d1 = _update_d1(s, t, d0, d1, i, n)

        # Correct upper boundary overshoot which happens when the upper
        # boundary, _ind_v_plus_upper, is greater than _ind_v_minus - 1,
        # as shown in x1d1b in test_levenshtein_seg.py
        if k > 0 and segs[k-1][1] == i:  # just above the upper boundary
            ind_v_minus_i = _ind_v_minus_lower(d1) - 1
            if segt[k-1][1] > ind_v_minus_i:
                segt[k-1][1] = ind_v_minus_i
            if k >= n_segs: break

        # Find segment lower boundary for t based on _ind_v_minus_lower(d1)
        if segs[k][0] == i:
            segt[k][0] = _ind_v_minus_lower(d1) - 1

        # Find segment upper boundary for t based on ind_v_plus.
        if segs[k][1] == i + 1:
            segt[k][1] = _ind_v_plus_upper(d1)
            k += 1          # update the segment index

        d0, d1 = d1, d0

    return segt


def levenshtein_align(
    s: List[str],
    t: List[str],
    segs: List[List],
) -> List[List]:
    """Segment alignment with prefix drift addressed---the normal version.

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
    -   segs: List of semantic segments of s, each segment is [start, end].

    Return:
    -   segt: List of aligned segments of t, each corresponds to a segment
            in segs; so it has the same dimension as segs.

Will address the issue with extended end index. This can be done
-   by comparing the start index of the next immediate segment.
-   If there is no immediate next section, add one, which a size of 1.
    This needs an
-
    """

    m, n = len(s), len(t)   # sizes of s and t
    d0 = list(range(n+1))   # prev LD dist
    d1 = [0] * (n+1)        # curr LD dist

    n_segs = len(segs)      # num of segments
    # segments of t corresponding to segments of s: segs
    segt = [[0] * 2 for _ in range(n_segs)]
    k = 0                   # index of segs/segt

    ss = 0   # sequence s' total shift due to update of s
    ts = 0   # sequence t's total shift; counterpart of ss
    mc = m   # m's original value for loop control
    check_shift = True      # flag for checking shift

    while True:
        for i in range(m):
            # Check the prefix drift at seg's lower boundary.
            # If exist, update s and t and related variables.
            if k < n_segs and segs[k][0] == ss + i and check_shift:
                # t_ind: t's index used for prefix drift checking.
                t_ind = _ind_v_plus_lower(d0)
                # n_pd: num of prefix drift (leading ins of t compared to s).
                # r, h: sub sequences in s and t for prefix drift checking.
                n_pd, r, h = _prefix_drift_rh(s, t, i, t_ind)

                # Restart the "for i loop" as needed if there is prefix drift
                if n_pd:
                    s, t, m, n, d0, d1, ss, i = \
                        _update_st_vars(r, h, n_pd, ss, i)
                    ts = ts + t_ind + n_pd  # needed for alignment
                    check_shift = False     # no check again for this boundary
                    # Only break the current "for i loop" if s has 2+ elements
                    if m > 1: break

            d1 = _update_d1(s, t, d0, d1, i, n)

            # Correct upper boundary overshoot; see comments of fast version.
            if k > 0 and segs[k-1][1] == ss + i:  # just above the upper boundary
                ind_v_minus_i = _ind_v_minus_lower(d1) - 1 + ts
                if segt[k-1][1] > ind_v_minus_i:
                    segt[k-1][1] = ind_v_minus_i
                if k >= n_segs: return segt  # done with all segs; exit

            # Find segment lower boundary for t, which is _ind_v_star(d1).
            if segs[k][0] == ss + i:
                segt[k][0] = _ind_v_star(d1)

            # Find segment upper boundary for t based on ind_v_plus.
            if segs[k][1] == ss + i + 1:
                segt[k][0] += ts     # update lower boundary
                segt[k][1] = _ind_v_plus_upper(d1) + ts
                k += 1               # update the segment index
                check_shift = True   # get ready for prefix drift checking

            d0, d1 = d1, d0

        if ss + i >= mc - 1: break   # all elements in s scanned

    return segt


#--------------------------------------------------------------------
# Levenshtein segment-level distance functions
#--------------------------------------------------------------------

def levenshtein_seg_fast(
    s: List[str],
    t: List[str],
    segs: List[List],
    head: bool = False,
) -> List[List]:
    """Segment size and LD calculation---the fast version.

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
    -   segs: List of semantic segments, each segment is [start, end].
    -   head: Boolean indicator for including prefix drift (hallucination)
        before each segment:
        -   False: do not include (default)
        -   True: include

    Returns:
    -   segd: segment distance---a list of [seg_size, edit_dist] for
            each segment, where
        -   seg_size (= end - start),
        -   edit_dist between s[start:end] and the correcponding t sequence.
    """

    base_seg_dist = _v_plus if head else _v_star

    m, n = len(s), len(t)   # sizes of s and t
    d0 = list(range(n+1))   # prev LD dist
    d1 = [0] * (n+1)        # curr LD dist

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
    s: List[str],
    t: List[str],
    segs: List[List],
    head: bool = False,
) -> List[List]:
    """Calculate size and Levenshtein dist of segments---the normal version.

    See the doc string of the levenshtein_seg_fast function.
    """

    m, n = len(s), len(t)   # sizes of s and t
    d0 = list(range(n+1))   # prev LD dist
    d1 = [0] * (n+1)        # curr LD dist

    n_segs = len(segs)      # num of segments
    # segd = segment size and dist corresponding to segs
    segd = [[0] * 2 for _ in range(n_segs)]
    k = 0                   # index of segs/segt

    base_dist = 0           # base dist: v_plus

    ss = 0                  # base index for s
    mc = m                  # copy of m for loop control
    check_shift = True      # flag for checking shift

    while True:
        for i in range(m):
            # Check the prefix drift at seg's lower boundary.
            # If exist, update s and t and related variables.
            if segs[k][0] == ss + i and check_shift:
                # t_ind: t's index used for prefix drift checking.
                t_ind = _ind_v_plus_lower(d0)
                # n_pd: num of prefix drift (leading ins of t compared to s).
                # r, h: sub sequences in s and t for prefix drift checking.
                n_pd, r, h = _prefix_drift_rh(s, t, i, t_ind)

                # Restart the "for i loop" as needed if there is prefix drift
                if n_pd:
                    s, t, m, n, d0, d1, ss, i = \
                        _update_st_vars(r, h, n_pd, ss, i)
                    check_shift = False     # no check again for this boundary
                    # Only break the current "for i loop" if s has 2+ elements
                    if m > 1: break

            d1 = _update_d1(s, t, d0, d1, i, n)

            # Find the base dist at the segment lower boundary.
            if segs[k][0] == ss + i:
                base_dist = min(d0)

            # Find the seg size and dist at the segment upper boundary.
            if segs[k][1] == ss + i + 1:
                segd[k][0] = segs[k][1] - segs[k][0]    # seg size
                segd[k][1] = min(d1) - base_dist        # seg dist
                if head: segd[k][1] += n_pd             # seg dist
                check_shift = True   # get ready for prefix drift checking
                k += 1
                if k >= n_segs: return segd

            d0, d1 = d1, d0

        if ss + i >= mc - 1: break   # break the while loop

    return segd


#--------------------------------------------------------------------
# Levenshtein word-level distance functions
#--------------------------------------------------------------------

def levenshtein_word_fast(
    s: List[str],
    t: List[str],
) -> List[List]:
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
    d0 = list(range(n+1))   # prev LD dist
    d1 = [0] * (n+1)        # curr LD dist

    wlst = [[0] * 2 for _ in range(m)]  # wlst = word list
    min_d0 = 0

    for i in range(m):
        d1 = _update_d1(s, t, d0, d1, i, n)

        min_d1 = min(d1)
        wlst[i][0] = s[i]              # word
        wlst[i][1] = min_d1 - min_d0   # dist

        d0, d1, min_d0 = d1, d0, min_d1

    return wlst


def levenshtein_word(
    s: List[str],
    t: List[str],
    err_limit: int = 5,
) -> List[List]:
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

    m, n = len(s), len(t)   # sizes of s and t
    d0 = list(range(n+1))   # prev LD dist
    d1 = [0] * (n+1)        # curr LD dist

    wlst = [[0] * 2 for _ in range(m)]  # wlst = word list
    min_d0 = 0

    ss = 0                  # base index for s
    mc, sc = m, s.copy()

    while True:
        for i in range(m):
            d1 = _update_d1(s, t, d0, d1, i, n)

            # Assign word and initial dist to word list
            wlst[ss+i][0] = sc[ss+i]    # word
            min_d1 = min(d1)
            dist = min_d1 - min_d0
            wlst[ss+i][1] += dist       # 0 or 1

            t_ind = _ind_v_plus_lower(d0)
            d0, d1, min_d0 = d1, d0, min_d1

            if dist == 0: continue

            # Otherwise, check for potential prefix drift
            n_pd, r, h = _prefix_drift_rh(s, t, i, t_ind)
            # Restart the "for i loop" as needed if there is prefix drift
            if n_pd:
                wlst[ss+i][1] = n_pd         # add num of hallucinations
                if ss+i == 0:
                    wlst[ss+i][1] += n_pd    # add again for s[0]
                else:
                    wlst[ss+i-1][1] += n_pd  # share blame with neighbor

                s, t, m, n, d0, d1, ss, i = \
                    _update_st_vars(r, h, n_pd, ss, i)
                min_d0 = 0

                break
            else:  # substitution or deletion
                wlst[ss+i][1] += 1  # seg dist = 2 now

        if ss + i >= mc - 1:
            # Blame the last word in s for all tail issues.
            num_tail = len(d0) - _ind_v_plus_lower(d0) - 1
            if num_tail:
                wlst[mc-1][1] += 2 * num_tail

            wlst = _clip_wlst_err(wlst, err_limit)

            break  # all elements of s scanned

    return wlst


#--------------------------------------------------------------------
# Common Utility/Helper functions
#--------------------------------------------------------------------

# Find the max index of the min value of a list.
def _clip_wlst_err(wlst, err_limit):
    for word_err in wlst:
        word_err[1] = min(word_err[1], err_limit)
    return wlst


# Find the num of prefix drifts (insertion or hallucination words) of s & t.
def _num_prefix_drift(s: List[str], t: List[str]) -> int:
    shift = 0
    dist0 = levenshtein(s, t)
    dist1 = levenshtein(s, t[1:])
    while dist0 > dist1:
        shift += 1
        dist0 = dist1
        dist1 = levenshtein(s, t[shift+1:])
    return shift


# Find the num of prefix drifts and new s & t sequences.
def _prefix_drift_rh(s, t, i, t_ind):
    r = s[i:]               # r = ref, partial source
    h = t[t_ind:]           # h = hyp, partial target
    n_pd = _num_prefix_drift(r, h)
    return n_pd, r, h


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


#--------------------------------------------------------------------
# Utility/Helper functions for special value and index
#--------------------------------------------------------------------

# Find the max index of the min value of a list.
def _max_ind_of_min(d: List[int]) -> int:
    min_val = min(d)
    ind = [i for i, x in enumerate(d) if x == min_val]
    return max(ind)


# Find v_minus at the lower boundary.
def _v_minus_lower(d1):
    return min(d1)

# Find index of v_minus at the lower boundary.
def _ind_v_minus_lower(d1):
    return _max_ind_of_min(d1)


# Find v_plus at the lower boundary.
def _v_plus_lower(d0):
    return min(d0)

# Find index of v_plus at the lower boundary.
def _ind_v_plus_lower(d0):
    return _max_ind_of_min(d0)


# Find v_plus at the upper boundary.
def _v_plus_upper(d1):
    return min(d1)

# Find index of v_plus at the upper boundary.
def _ind_v_plus_upper(d1):
    return _max_ind_of_min(d1)


# Calculate v_plus used for obtaining seg dist with head.
def _v_plus(d0, d1):  # used for obtaining seg dist with head
    return min(d0)


# Define function base_seg_dist for calculate the seg distance.
def _v_star(d0, d1):  # used for obtaining seg dist w/o head
    return d0[_ind_v_star(d1)]


# Find index of v_plus at the lower boundary of a segment.
def _ind_v_star(d1):
    return _max_ind_of_min(d1) - 1
