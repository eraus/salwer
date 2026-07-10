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
def levenshtein_2d(
        s: List[str],
        t: List[str],
        print_d: bool = False,  # True to print
    ) -> int:
    """Full-memory implementation of the Levenshtein distance."""

    m, n = len(s), len(t)
    d = [[0] * (n+1) for _ in range(m+1)]
    for i in range(1, m+1):
        d[i][0] = i
    for j in range(1, n+1):
        d[0][j] = j

    for i in range(m):      # row index
        for j in range(n):  # col index
            c = 0 if s[i] == t[j] else 1
            d[i+1][j+1] = min(
                d[i][j] + c,    # sub s->t
                d[i][j+1] + 1,  # del of s
                d[i+1][j] + 1,  # ins to s
            )

    if print_d:
        print("s\\t      " + '   '.join(t))
        print("     j >")
        i_line = "  i  0 | 1   " + '   '.join(str(num) for num in d[0][2:])
        print(i_line)
        divider = ''.join(["-"] * (len(i_line)-3))
        print("  v " + divider)
        for ch, row in zip(s, d[1:]):
            print(f"{ch}    {row[0]} | "
                  f"{'   '.join(str(num) for num in row[1:])}")

    return d[m][n]


def levenshtein(s: List[str], t: List[str]) -> int:
    """Two-list implementation of the Levenshtein distance"""

    m, n = len(s), len(t)
    d0 = list(range(n+1))  # prev dist
    d1 = [0] * (n+1)       # curr dist

    for i in range(m):
        d1[0] = i + 1
        for j in range(n):
            c = 0 if s[i] == t[j] else 1
            d1[j+1] = min(
                d0[j] + c,    # sub s->t
                d0[j+1] + 1,  # del of s
                d1[j] + 1,    # ins to s
            )

        d0, d1 = d1, d0

    return d0[n]


def levenshtein_1d(s: List[str], t: List[str]) -> int:
    """Single-list implementation of the Levenshtein distance"""

    m, n = len(s), len(t)
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
def levenshtein_align_fast(
    s: List[str],
    t: List[str],
    segs: List[List],
) -> List[List]:
    """Levenshtein distance and size of semantic segments--fast version.

    Args:
      - s: Source (reference) sequence as list of strings.
      - t: Target (hypothesis) sequence as list of strings.
      - segs: List of semantic segments of s, each segment is [start, end].

    Return:
      - segt: List of aligned segments of t, each corresponds to a segment
            in segs; so it has the same dimension as segs.
    """

    m, n = len(s), len(t)
    d0 = list(range(n+1))   # prev dist
    d1 = [0] * (n+1)        # curr dist

    n_segs = len(segs)      # num of segments
    segt = [[0] * 2 for _ in range(n_segs)]  # return
    k = 0                   # index of segs

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
            ind_valua_minus = max_ind_of_min(d1)
            segt[k][0] = ind_valua_minus - 1

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
    """Levenshtein distance and size of semantic segments--fast version.

    Args:
      - s: Source (reference) sequence as list of strings.
      - t: Target (hypothesis) sequence as list of strings.
      - segs: List of semantic segments of s, each segment is [start, end].

    Return:
      - segt: List of aligned segments of t, each corresponds to a segment
            in segs; so it has the same dimension as segs.
    """

    s, t, m, n, d0, d1, b, i = seg_reset(s, t, 0, 0, 0)
    n_segs = len(segs)
    segt = [[0] * 2 for _ in range(n_segs)]
    k = 0           # index of segs
    tos = 0         # num of target offset
    m0 = m          # copy of m for loop control

    while True:
        for i in range(m):
            d1 = levenshtein_update_d1(s, t, d0, d1, i, n)

            if segs[k][0] == b + i:
                ind_valua_minus = max_ind_of_min(d1)
                segt[k][0] = ind_valua_minus - 1

                # Check num_shift: the num of prefix drift
                num_shift, index4t, r, h = \
                    check_prefix_drift(s, t, d0, i)
                # index4t = max_ind_of_min(d0)    # value-
                # r = s[i:]           # ref = partial source
                # h = t[index4t:]     # hyp = partial target
                # num_shift = num_prefix_drift(r, h)

                # Restart for i loop if there is prefix drift
                if num_shift:
                    s, t, m, n, d0, d1, b, i = \
                        seg_reset(r, h, num_shift, b, i)
                    tos = tos + index4t + num_shift
                    break       # break the current for i loop

            if segs[k][1] == b + i + 1:
                segt[k][1] = max_ind_of_min(d1)
                segt[k][0] += tos
                segt[k][1] += tos
                k += 1
                if k >= n_segs: return segt

            d0, d1 = d1, d0

        if b + i >= m0 - 1: break   # break the while loop

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

    b = 0           # base index for s
    pd = 0          # num of prefix drift
    m0 = m          # copy of m for loop control

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

            if segs[k][0] == b + i:
                base_dist = min(d0)

                # Check num_shift: the num of prefix drift
                index4t = max_ind_of_min(d0)    # value-
                r = s[i:]           # ref = partial source
                h = t[index4t:]     # hyp = partial target
                num_shift = num_prefix_drift(r, h)

                # Restart for i loop if there is prefix drift
                if num_shift:
                    s = r                   # new source
                    t = h[num_shift:]       # new target
                    m, n = len(s), len(t)   # new sizes
                    d0 = list(range(n+1))   # new prev dist
                    d1 = [0] * (n+1)        # new curr dist
                    b += i
                    i = 0
                    pd = num_shift
                    break       # break the current for i loop

            if segs[k][1] == b + i + 1:
                segd[k][0] = segs[k][1] - segs[k][0]    # seg size
                segd[k][1] = min(d1) - base_dist        # seg dist
                if head: segd[k][1] += pd               # seg dist
                pd = 0
                k += 1
                if k >= n_segs: return segd

            d0, d1 = d1, d0

        if b + i >= m0 - 1: break   # break the while loop

    # Safety net to ensure calculated seg size is assigned
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
    m0, s0 = m, s.copy()
    d0 = list(range(n+1))   # prev dist
    d1 = [0] * (n+1)        # curr dist
    min_d0 = 0              # min value of d0
    rslts = [[0] * 2 for _ in range(m)]
    b = 0   # the base for s
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
            rslts[b+i][0] = s0[b+i]     # word
            dist = min_d1 - min_d0      # dist
            rslts[b+i][1] += dist
            index4t = max_ind_of_min(d0)
            d0, d1, min_d0 = d1, d0, min_d1
            if dist == 0: continue
            # Otherwise, check the num of prefix drift
            r = s[i:]           # ref = source
            h = t[index4t:]     # hyp = target
            num_shift = num_prefix_drift(r, h)
            if num_shift:
                rslts[b+i][1] = num_shift
                if b+i == 0:
                    rslts[b+i][1] += num_shift
                else:
                    rslts[b+i-1][1] += num_shift
                s = r
                t = h[num_shift:]
                m, n = len(s), len(t)
                d0 = list(range(n+1))   # prev dist
                d1 = [0] * (n+1)        # curr dist
                min_d0 = 0              # min value of d0
                b += i
                i = 0
                break
            else:
                rslts[b+i][1] += 1
        if b + i >= m0 - 1:
            num_tail = len(d0) - max_ind_of_min(d0) - 1
            if num_tail:
                rslts[m0-1][1] += 2 * num_tail
            break

    return rslts


#--------------------------------------------------------------------
# Helper functions
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


def levenshtein_update_d1(s, t, d0, d1, i, n):
    d1[0] = i + 1
    for j in range(n):
        c = 0 if s[i] == t[j] else 1
        d1[j+1] = min(
            d0[j] + c,      # sub s->t
            d0[j+1] + 1,    # del of s
            d1[j] + 1,      # ins to s
        )
    return d1


def seg_reset(r, h, num_shift, b, i):
    s = r                   # new source
    t = h[num_shift:]       # new target
    m, n = len(s), len(t)   # new sizes
    d0 = list(range(n+1))   # new prev dist
    d1 = [0] * (n+1)        # new curr dist
    b += i
    i = 0
    return s, t, m, n, d0, d1, b, i


def check_prefix_drift(s, t, d0, i):
    index4t = max_ind_of_min(d0)    # value-
    r = s[i:]           # ref = partial source
    h = t[index4t:]     # hyp = partial target
    num_shift = num_prefix_drift(r, h)
    return num_shift, index4t, r, h