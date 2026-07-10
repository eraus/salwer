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
        print("     j > ")
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
    len_segs = len(segs)
    # segs = segments of s; segt = segments of t
    segt = [[0] * 2 for _ in range(len_segs)]
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
        print(f"{d1 = }")
        if segs[k][0] == i:
            segt[k][0] = max_ind_of_min(d1) - 1
        if segs[k][1] == i + 1:
            segt[k][1] = max_ind_of_min(d1)
            k += 1
            if k >= len_segs: break
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

    m, n = len(s), len(t)
    d0 = list(range(n+1))   # prev dist
    d1 = [0] * (n+1)        # curr dist
    len_segs = len(segs)
    segt = [[0] * 2 for _ in range(len_segs)]
    k = 0                   # index of segs
    L = 0                   # shift of segt
    for i in range(m):
        d1[0] = i + 1
        for j in range(n):
            c = 0 if s[i] == t[j] else 1
            d1[j+1] = min(
                d0[j] + c,      # sub s->t
                d0[j+1] + 1,    # del of s
                d1[j] + 1,      # ins to s
            )
        print(f"{d1 = }")
        if segs[k][0] == i:
            # ind_star = max_ind_of_min(d1) - 1
            # ind_minus = max_ind_of_min(d0)
            # L += ind_star - ind_minus
            # segt[k][0] = L + ind_star
            # print(f"{i = }; {ind_star = }; {ind_minus = }; {L = }")
            segt[k][0] = max_ind_of_min(d1) - 1
        if segs[k][1] == i + 1:
            # segt[k][1] = L + max_ind_of_min(d1)
            segt[k][1] = max_ind_of_min(d1)
            k += 1
            if k >= len_segs: break
        d0, d1 = d1, d0
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

    Returns: List of [segment_length, edit_distance] for each segment, where
      - segment_length (end - start),
      - levenshtein_dist between s[start:end] and the correcponding t sequence.
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
    base_dist = 0           # base dist of a Seg; d1[0]
    len_segs = len(segs)
    rslts = [[0] * 2 for _ in range(len_segs)]
    k = 0                   # index of segment
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
            rslts[k][0] = segs[k][1] - segs[k][0]   # Seg size
            rslts[k][1] = min(d1) - base_dist       # Seg dist
            k += 1
            if k >= len_segs: break
        d0, d1 = d1, d0
    return rslts


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

    Returns: List of [segment_length, edit_distance] for each segment, where
      - segment_length (end - start),
      - levenshtein_dist between s[start:end] and the correcponding t sequence.
    """

    m, n = len(s), len(t)
    m0 = m
    d0 = list(range(n+1))   # prev dist
    d1 = [0] * (n+1)        # curr dist
    l_segs = len(segs)
    rslts = [[0] * 2 for _ in range(l_segs)]
    b = 0                   # Base index for s
    base_dist = 0           # Base dist of a seg; d1[0]
    pre_drift = 0           # Number of prefix drift
    seg = 0

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
            if seg >= l_segs: return rslts
            if segs[seg][0] == b + i:
                # Check the num of prefix drift
                index4t = max_ind_of_min(d0)
                r = s[i:]           # ref = source
                h = t[index4t:]     # hyp = target
                num_shift = num_prefix_drift(r, h)
                if num_shift:
                    s = r
                    t = h[num_shift:]
                    m, n = len(s), len(t)
                    d0 = list(range(n+1))   # prev dist
                    d1 = [0] * (n+1)        # curr dist
                    b += i
                    i = 0
                    pre_drift = num_shift
                    break
                base_dist = min(d0)
            if segs[seg][1] == b + i + 1:
                rslts[seg][0] = segs[seg][1] - segs[seg][0]  # Seg size
                rslts[seg][1] = min(d1) - base_dist          # Seg dist
                if head: rslts[seg][1] += pre_drift          # Seg dist
                pre_drift = 0
                seg += 1
            d0, d1 = d1, d0
        if b + i >= m0 - 1: break

    # Safety net to ensure calculated seg size is the same as provided
    for seg in range(l_segs):
        if rslts[seg][0] == 0:
            rslts[seg][0] = segs[seg][1] - segs[seg][0]
            rslts[seg][1] = rslts[seg][0]

    return rslts

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


# s = "A B A D E B G H I".split()
# t = "A B C D E F G H I".split()
#
# s\t j   A   B   C   D   E   F   G   H   I
# i   0   1   2   3   4   5   6   7   8   9
# A   1   0   1   2   3   4   5   6   7   8
# B   2   1   0:  1   2   3   4   5   6   7
# A   3   2   1   1:  2   3   4   5   6   7
# D   4   3   2   2   1   2   3   4   5   6
# E   5   4   3   3   2   1:  2   3   4   5
# B   6   5   4   4   3   2   2:  3   4   5
# G   7   6   5   5   4   3   3   2-  3   4
# H   8   7   6   6   5   4   4   3   2   3
# I   9   8   7   7   6   5   5   4   3   2

# Single-deletion from source case:

# s = "A B C D E F G H I".split()
# t = "A B   D E   G H I".split()
#
# s\t j   A   B   D   E   G   H   I
# i   0   1   2   3   4   5   6   7
# A   1   0   1   2   3   4   5   6
# B   2   1   0:  1   2   3   4   5
# C   3   2   1   1:  2   3   4   5
# D   4   3   2   1   2   3   4   5
# E   5   4   3   2   1:  2   3   4
# F   6   5   4   3   2   2:  3   4
# G   7   6   5   4   3   2   3   4
# H   8   7   6   5   4   3   2   3
# I   9   8   7   6   5   4   3   2


# Single insertation to the source case (only one prefix drift):

# s = "A B   D E   G H I".split()
# t = "A B C D E F G H I".split()
#                                           i = 0   1   2   3   4   5   6   7
# s\t j   A   B   C   D   E   F   G   H   I
# i   0   1   2   3   4   5   6   7   8   9     d0
# A   1   0   1   2   3   4   5   6   7   8     d1->d0
# B   2   1   0:  1   2   3   4   5   6   7         d1->d0
# D   3   2   1   1   1:  2   3   4   5   6             d1->d0

# s\t j   A   B   D   E   F   G   H   I
# D   3   2   1   0   1:  2   3   4   5   6                 d0
# E   4   3   2   2   2   1:  2   3   4   5
# G   5   4   3   3   3   2   2   2:  3   4
# H   6   5   4   4   4   3   3   3   2   3
# I   7   6   5   5   5   4   4   4   3   2


# s = "  B C D   F G H".split()
# t = "A B C D E F G H I".split()
#
# s\t j   A   B   C   D   E   F   G   H   I
# i   0:  1   2   3   4   5   6   7   8   9
# B   1   1   1:  2   3   4   5   6   7   8
# C   2   2   2   1   2   3   4   5   6   7
# D   3   3   3   2   1:  2   3   4   5   6
# F   4   4   4   3   2   2   2:  3   4   5
# G   5   5   5   4   3   3   3   2   3   4
# H   6   6   6   5   4   4   4   3   2   3


# Multiple-insertation to the source case (2+ prefix drifts):

# s = "    C D E     H I".split()
# t = "A B C D E F G H I".split()
#
# s\t j   A   B   C   D   E   F   G   H   I
# i   0:  1   2   3   4   5   6   7   8   9
# C   1   1:  2   2   3   4   5   6   7   8
# D   2   2   2   3   2   3   4   5   6   7
# E   3   3   3   3   3   2:  3   4   5   6
# H   4   4   4   4   4   3   3:  4   4   5
# I   5   5   5   5   5   4   4   4   5   4


# def levenshtein_n_seg_size_tail(
#     s: List[str],
#     t: List[str],
#     segs: List[List],
# ) -> List[List]:
#     """Levenshtein distance and size for semantic segments.

#     This function takes a list of segments, where each segment is defined by
#     [start, end] indices, and computes the Levenshtein distance between the
#     corresponding slices of ref and hyp for each segment.

#     Args:
#         s: Reference sequence as list of strings.
#         t: Hypothesis sequence as list of strings.
#         segs: List of segments, each segment is [start, end].

#     Returns:
#         List of [segment_length, edit_distance] for each segment, where
#         segment_length = end - start,
#         edit_distance = edit dist btwn ref[start:end] and hyp[start:end].
#     """

#     m, n = len(s), len(t)
#     d0 = list(range(n+1))   # prev dist
#     d1 = [0] * (n+1)        # curr dist

#     dist = 0    # The start distance, corresponding to d1[0]
#     rslts = [[0] * 2 for _ in range(len(segs))]
#     seg = 0

#     for i in range(m):
#         d1[0] = i + 1
#         for j in range(n):
#             c = 0 if s[i] == t[j] else 1
#             d1[j+1] = min(
#                 d0[j+1] + 1,  # deletion
#                 d1[j] + 1,  # insertion
#                 d0[j] + c,  # substitution
#             )
#         if seg < len(segs):
#             # if segs[seg][0] == i and i > 1:
#             if segs[seg][0] == i and i > 0:
#                 dist_curr = min(d1)
#                 ind = [i for i, x in enumerate(d1) if x == dist_curr]
#                 dist_ind = max(ind)
#                 dist = d0[dist_ind - 1]
#             if segs[seg][1] == i + 1:
#                 rslts[seg][0] = segs[seg][1] - segs[seg][0]  # Size of seg
#                 rslts[seg][1] = min(d1) - dist  # edit distance
#                 seg += 1
#         d0, d1 = d1, d0

#     return rslts


# def levenshtein_n_seg_size_head(
#     s: List[str],
#     t: List[str],
#     segs: List[List],
# ) -> List[List]:
#     """Levenshtein distance and size for semantic segments.

#     This function takes a list of segments, where each segment is defined by
#     [start, end] indices, and computes the Levenshtein distance between the
#     corresponding slices of ref and hyp for each segment.

#     Args:
#         s: Reference sequence as list of strings.
#         t: Hypothesis sequence as list of strings.
#         segs: List of segments, each segment is [start, end].

#     Returns:
#         List of [segment_length, edit_distance] for each segment, where
#         segment_length = end - start,
#         edit_distance = edit dist btwn ref[start:end] and hyp[start:end].
#     """

#     m, n = len(s), len(t)
#     d0 = list(range(n+1))   # prev dist
#     d1 = [0] * (n+1)        # curr dist

#     dist = 0    # The start distance, corresponding to d1[0]
#     rslts = [[0] * 2 for _ in range(len(segs))]
#     seg = 0

#     for i in range(m):
#         d1[0] = i + 1
#         for j in range(n):
#             c = 0 if s[i] == t[j] else 1
#             d1[j+1] = min(
#                 d0[j+1] + 1,  # deletion
#                 d1[j] + 1,  # insertion
#                 d0[j] + c,  # substitution
#             )
#         if seg < len(segs):
#             # if segs[seg][0] == i and i > 1:
#             if segs[seg][0] == i and i > 0:
#                 dist = min(d0)
#             if segs[seg][1] == i + 1:
#                 rslts[seg][0] = segs[seg][1] - segs[seg][0]  # Size of seg
#                 rslts[seg][1] = min(d1) - dist  # edit distance
#                 seg += 1
#         d0, d1 = d1, d0

#     return rslts


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
