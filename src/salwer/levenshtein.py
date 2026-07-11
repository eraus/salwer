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
        print_ld: bool = False,  # print the LD table if True
    ) -> int:
    """Full-memory implementation of the Levenshtein distance alg."""

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
    """

    # Initialize the 2 1D LD lists.
    m, n = len(s), len(t)     # sizes of s and t
    d0 = list(range(n+1))     # prev LD dist
    d1 = [0] * (n+1)          # curr LD dist

    for i in range(m):
        d1[0] = i + 1
        for j in range(n):
            c = 0 if s[i] == t[j] else 1
            d1[j+1] = min(
                d0[j] + c,    # sub s->t
                d0[j+1] + 1,  # del of s
                d1[j] + 1,    # ins to s
            )

        d0, d1 = d1, d0       # swap lists

    return d0[n]


def levenshtein_1d(s: List[str], t: List[str]) -> int:
    """Single-list implementation of the Levenshtein distance alg.

    A single 1D list, d, is used instead of 2 1D lists.
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
# Levenshtein alignment
#--------------------------------------------------------------------

def levenshtein_align_fast(
    s: List[str],
    t: List[str],
    segs: List[List],
) -> List[List]:
    """Segment alignment based Levenshtein distance---the fast version.

    See the doc string of the levenshtein_align() function for details.
    """

    m, n = len(s), len(t)   # sizes of s and t
    d0 = list(range(n+1))   # prev dist
    d1 = [0] * (n+1)        # curr dist

    n_segs = len(segs)      # num of segments
    # segments of t corresponding to segments of s: segs
    segt = [[0] * 2 for _ in range(n_segs)]
    k = 0                   # index of segs/segt

    for i in range(m):
        # Update d1. To make the main loop more readable, this code block
        # can be implemented as update_d1(s, t, d0, d1, i, n).
        d1[0] = i + 1
        for j in range(n):
            c = 0 if s[i] == t[j] else 1
            d1[j+1] = min(
                d0[j] + c,      # sub s->t
                d0[j+1] + 1,    # del of s
                d1[j] + 1,      # ins to s
            )

        # Find segment lower boundary for t based on ind_v_minus - 1
        if segs[k][0] == i:
            segt[k][0] = max_ind_of_min(d1) - 1

        # Find segment upper boundary for t based on ind_v_plus.
        # Update the segment index; exit as needed.
        if segs[k][1] == i + 1:
            segt[k][1] = max_ind_of_min(d1)
            k += 1
            if k >= n_segs: break

        d0, d1 = d1, d0

    return segt


def levenshtein_align(
    s: List[str],
    t: List[str],
    segs: List[List],
) -> List[List]:
    """Segment alignment based Levenshtein distance---the normal version.

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
            is referred to as v_star, and the index is ind_v_star.

    Args:
    -   s: Source (reference) sequence as list of strings.
    -   t: Target (hypothesis) sequence as list of strings.
    -   segs: List of semantic segments of s, each segment is [start, end].

    Return:
    -   segt: List of aligned segments of t, each corresponds to a segment
            in segs; so it has the same dimension as segs.
    """

    # s, t, m, n, d0, d1, ss, i = update_st_vars(s, t, 0, 0, 0)
    m, n = len(s), len(t)   # sizes of s and t
    d0 = list(range(n+1))   # prev LD dist
    d1 = [0] * (n+1)        # curr LD dist

    n_segs = len(segs)      # num of segments
    # segments of t corresponding to segments of s: segs
    segt = [[0] * 2 for _ in range(n_segs)]
    k = 0                   # index of segs/segt

    ss = 0   # sequence s' total shift due to update of s
    ts = 0   # sequence t's total shift; counterpart of ss
    mm = m   # m's original value for loop control

    check_shift = True      # flag for checking shift

    while True:
        for i in range(m):

            # Check the prefix drift at seg's lower boundary.
            # If exist, update s and t and related variables.
            if segs[k][0] == ss + i and check_shift:
                # n_pd: num of prefix drift (leading ins of t compared to s).
                # t_ind: t's index used for prefix drift checking.
                # r, h: sub sequences in s and t for prefix drift checking.
                n_pd, t_ind, r, h = check_prefix_drift(s, t, d0, i)

                # Restart the "for i loop" as needed if there is prefix drift
                if n_pd:
                    check_shift = False     # will not check prefix drift again
                    s, t, m, n, d0, d1, ss, i = \
                        update_st_vars(r, h, n_pd, ss, i)
                    ts = ts + t_ind + n_pd  # needed for alignment
                    # Only break the current "for i loop" if s has 2+ elements
                    if m > 1: break

            d1 = update_d1(s, t, d0, d1, i, n)

            # Find segment lower boundary for t based on ind_v_minus - 1.
            if segs[k][0] == ss + i:
                segt[k][0] = max_ind_of_min(d1) - 1

            # Find segment upper boundary for t based on ind_v_plus.
            if segs[k][1] == ss + i + 1:
                segt[k][1] = max_ind_of_min(d1)
                segt[k][0] += ts     # update lower boundary
                segt[k][1] += ts     # update upper boundary
                check_shift = False  # get ready for prefix drift checking
                k += 1               # update the segment index
                if k >= n_segs: return segt  # exit as needed

            d0, d1 = d1, d0

        if ss + i >= mm - 1: break   # all elements in s scanned

    return segt


#--------------------------------------------------------------------
# Different implementation of the Levenshtein algorithm
def levenshtein_seg_fast(
    s: List[str],
    t: List[str],
    segs: List[List],
    head: bool = False,
) -> List[List]:
    """Levenshtein distance and size of semantic segments--fast version.

    This function takes (1) the source list (s), (2) the target lyst (t),
    (3) the semantic segment list (segs), and (4) a boolean variable for
    including prefix drift or hallucination of each segment (head).

    Args:
      - s: Source (reference) sequence as list of strings.
      - t: Target (hypothesis) sequence as list of strings.
      - segs: List of semantic segments, each segment is [start, end].
      - head: Boolean indicator for including prefix drift before each segment:
        - False: do not include (default)
        - True: include

    Returns:
      - segd: segment distance---a list of [seg_size, edit_dist] for
            each segment, where
        - seg_size (= end - start),
        - edit_dist between s[start:end] and the correcponding t sequence.
    """

    # base seg dist w/o prefix drift, hence no head
    def base_seg_dist_nohead(d0, d1):
        dist_ind = max_ind_of_min(d1)
        dist = d0[dist_ind - 1]
        return dist

    # base seg dist with prefix drift, hence head
    def base_seg_dist_head(d0, d1):
        return min(d0)

    base_seg_dist = base_seg_dist_head if head else base_seg_dist_nohead

    m, n = len(s), len(t)
    d0 = list(range(n+1))   # prev dist
    d1 = [0] * (n+1)        # curr dist

    n_segs = len(segs)
    segd = [[0] * 2 for _ in range(n_segs)]
    k = 0           # index of segs
    base_dist = 0   # base dist: *value or value-

    for i in range(m):
        d1[0] = i + 1
        for j in range(n):
            c = 0 if s[i] == t[j] else 1
            d1[j+1] = min(
                d0[j] + c,      # sub s->t
                d0[j+1] + 1,    # del of s
                d1[j] + 1,      # ins to s
            )

        if segs[k][0] == i:
            base_dist = base_seg_dist(d0, d1)

        if segs[k][1] == i + 1:
            segd[k][0] = segs[k][1] - segs[k][0]   # Seg size
            segd[k][1] = min(d1) - base_dist       # Seg dist
            k += 1
            if k >= n_segs: break

        d0, d1 = d1, d0

    return segd


def levenshtein_seg(
    s: List[str],
    t: List[str],
    segs: List[List],
    head: bool = False,
) -> List[List]:
    """Levenshtein distance and size of semantic segments.

    This function takes (1) the source list (s), (2) the target list (t),
    (3) the semantic segment list (segs), and (4) a boolean variable for
    including prefix drift or hallucination of each segment (head).

    Args:
      - s: Source (reference) sequence as list of strings.
      - t: Target (hypothesis) sequence as list of strings.
      - segs: List of semantic segments, each segment is [start, end].
      - head: Boolean indicator for including prefix drift before each segment:
        - False: do not include (default)
        - True: include

    Returns:
      - segd: segment distance---a list of [seg_size, edit_dist] for
            each segment, where
        - seg_size (= end - start),
        - edit_dist between s[start:end] and the correcponding t sequence.
    """

    m, n = len(s), len(t)
    d0 = list(range(n+1))   # prev dist
    d1 = [0] * (n+1)        # curr dist

    n_segs = len(segs)
    segd = [[0] * 2 for _ in range(n_segs)]
    k = 0           # index of segs
    base_dist = 0   # base dist: value-

    ss = 0           # base index for s
    pd = 0          # num of prefix drift
    mm = m          # copy of m for loop control

    while True:
        for i in range(m):
            d1[0] = i + 1
            for j in range(n):
                c = 0 if s[i] == t[j] else 1
                d1[j+1] = min(
                    d0[j] + c,    # sub s->t
                    d0[j+1] + 1,  # del of s
                    d1[j] + 1,    # ins to s
                )

            if segs[k][0] == ss + i:
                base_dist = min(d0)

                # Check n_pd: the num of prefix drift
                t_ind = max_ind_of_min(d0)    # value-
                r = s[i:]           # ref = partial source
                h = t[t_ind:]     # hyp = partial target
                n_pd = num_prefix_drift(r, h)

                # Restart for i loop if there is prefix drift
                if n_pd:
                    s = r                   # new source
                    t = h[n_pd:]       # new target
                    m, n = len(s), len(t)   # new sizes
                    d0 = list(range(n+1))   # new prev dist
                    d1 = [0] * (n+1)        # new curr dist
                    ss += i
                    i = 0
                    pd = n_pd
                    break       # break the current for i loop

            if segs[k][1] == ss + i + 1:
                segd[k][0] = segs[k][1] - segs[k][0]    # seg size
                segd[k][1] = min(d1) - base_dist        # seg dist
                if head: segd[k][1] += pd               # seg dist
                pd = 0
                k += 1
                if k >= n_segs: return segd

            d0, d1 = d1, d0

        if ss + i >= mm - 1: break   # break the while loop

    # Safety net to ensure calculated seg size is assigned
    # Need to debug why we arrive here using
    #     assert levenshtein_seg(s1sdi1, t1sdi1, sg1sdi1c) == \
    #     [[2, 1], [3, 2], [1, 1]]

    for k in range(n_segs):
        if segd[k][0] == 0:
            segd[k][0] = segs[k][1] - segs[k][0]
            segd[k][1] = segd[k][0]

    return segd

#--------------------------------------------------------------------
# Different implementation of the Levenshtein algorithm
def levenshtein_word_fast(
    s: List[str],
    t: List[str],
) -> List[List]:
    """Levenshtein distance of each word without examining errors (fast).

    This function calculates the word-level levenshtein distance. The meaning
    of raw is two fold:

    1. The errors (distance being one for a word) are not examined for type,
            which is substitution/delete/insertion.
    2. The error due to a hallucination is only considered as prefix drift.

    Args:
        s: Reference sequence as list of strings.
        t: Hypothesis sequence as list of strings.

    Returns:
        List of [word, levenshtein_dist] for each word, where
        levenshtein_dist is 0 or 1.
    """

    m, n = len(s), len(t)
    d0 = list(range(n+1))   # prev dist
    min_d0 = 0
    d1 = [0] * (n+1)        # curr dist
    rslts = [[0] * 2 for _ in range(m)]

    for i in range(m):
        d1[0] = i + 1
        for j in range(n):
            c = 0 if s[i] == t[j] else 1
            d1[j+1] = min(
                d0[j] + c,    # sub s->t
                d0[j+1] + 1,  # del of s
                d1[j] + 1,    # ins to s
            )
        min_d1 = min(d1)
        rslts[i][0] = s[i]              # word
        rslts[i][1] = min_d1 - min_d0   # dist
        d0, d1, min_d0 = d1, d0, min_d1

    return rslts


def levenshtein_word(
    s: List[str],
    t: List[str],
) -> List[List]:
    """Levenshtein distance of each word with errors examined.

    This function calculates the word-level levenshtein distance in a refined
    way as compared to levenshtein_word_fast. The meaning of refinement
    is multi-fold:

    1. Each error (Levenshtein dist being 1 for a word) is tested to see if
       it is an insertion (prefix drift or hallucination).
    2. If tested as a prefix hallucination, it is split to by the two words
       on the two sides of the hallucination.
    3. If the word is at the beginning of the source, all prefix hallucinations
       will be on this word.
    4. If the word is at the end of the source, all the surfix hallucinations
       will be on this word.

    Note that due to the splitting of error, we need to DOUBLE the value of
    the Levenshtein distance for easy processing and testing.

    Args:
        s: Reference sequence as list of strings.
        t: Hypothesis sequence as list of strings.

    Returns:
        List of [word, levenshtein_dist] for each word, where
        levenshtein_dist is can be a real number.
    """

    m, n = len(s), len(t)
    mm, s0 = m, s.copy()
    d0 = list(range(n+1))   # prev dist
    d1 = [0] * (n+1)        # curr dist
    min_d0 = 0              # min value of d0
    rslts = [[0] * 2 for _ in range(m)]
    ss = 0   # the base for s
    while True:
        for i in range(m):
            d1[0] = i + 1
            for j in range(n):
                c = 0 if s[i] == t[j] else 1
                d1[j+1] = min(
                    d0[j] + c,    # sub s->t
                    d0[j+1] + 1,  # del of s
                    d1[j] + 1,    # ins to s
                )
            min_d1 = min(d1)
            rslts[ss+i][0] = s0[ss+i]     # word
            dist = min_d1 - min_d0      # dist
            rslts[ss+i][1] += dist
            t_ind = max_ind_of_min(d0)
            d0, d1, min_d0 = d1, d0, min_d1
            if dist == 0: continue
            # Otherwise, check the num of prefix drift
            r = s[i:]           # ref = source
            h = t[t_ind:]     # hyp = target
            n_pd = num_prefix_drift(r, h)
            if n_pd:
                rslts[ss+i][1] = n_pd
                if ss+i == 0:
                    rslts[ss+i][1] += n_pd
                else:
                    rslts[ss+i-1][1] += n_pd
                s = r
                t = h[n_pd:]
                m, n = len(s), len(t)
                d0 = list(range(n+1))   # prev dist
                d1 = [0] * (n+1)        # curr dist
                min_d0 = 0              # min value of d0
                ss += i
                i = 0
                break
            else:
                rslts[ss+i][1] += 1
        if ss + i >= mm - 1:
            num_tail = len(d0) - max_ind_of_min(d0) - 1
            if num_tail:
                rslts[mm-1][1] += 2 * num_tail
            break

    return rslts


#--------------------------------------------------------------------
# Utility/Helper functions
#--------------------------------------------------------------------
def num_prefix_drift(s: List[str], t: List[str]) -> int:
    """Find the num of prefix drifts (insertion or hallucination) of s & t."""

    shift = 0
    dist0 = levenshtein(s, t)
    dist1 = levenshtein(s, t[1:])
    while dist0 > dist1:
        shift += 1
        dist0 = dist1
        dist1 = levenshtein(s, t[shift+1:])
    return shift


def max_ind_of_min(d: List[int]) -> int:
    """Find the max index of the min value of a list."""

    min_val = min(d)
    ind = [i for i, x in enumerate(d) if x == min_val]
    return max(ind)


# Utility function for updating d1.
# Direct implementation can be found in the levenshtein() function.
def update_d1(s, t, d0, d1, i, n):
    d1[0] = i + 1
    for j in range(n):
        c = 0 if s[i] == t[j] else 1
        d1[j+1] = min(
            d0[j] + c,      # sub s->t
            d0[j+1] + 1,    # del of s
            d1[j] + 1,      # ins to s
        )
    return d1


# Utility function for updating s and t sequences and related variables.
# This is needed when we want address the leading shift of t against s.
def update_st_vars(r, h, n_pd, ss, i):
    s = r                   # new source
    t = h[n_pd:]       # new target
    m, n = len(s), len(t)   # new sizes
    d0 = list(range(n+1))   # new prev dist
    d1 = [0] * (n+1)        # new curr dist
    ss += i
    i = 0
    return s, t, m, n, d0, d1, ss, i


def check_prefix_drift(s, t, d0, i):
    t_ind = max_ind_of_min(d0)    # value-
    r = s[i:]           # ref = partial source
    h = t[t_ind:]     # hyp = partial target
    n_pd = num_prefix_drift(r, h)
    return n_pd, t_ind, r, h