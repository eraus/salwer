from typing import List


# def _levenshtein_full_mem(
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
        print("s\\t j   " + '   '.join(t))
        print("i   " + '   '.join(str(num) for num in d[0]))
        for ch, row in zip(s, d[1:]):
            print(ch + "   " + '   '.join(str(num) for num in row))
    return d[m][n]


# def _levenshtein(s: List[str], t: List[str]) -> int:
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


# def _levenshtein_one_list(s: List[str], t: List[str]) -> int:
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

def seg_size_n_edit_distance(
    segs: List[List],
    ref: List[str],
    hyp: List[str],
) -> List[List]:
    pass


def levenshtein_seg(
    s: List[str],
    t: List[str],
    segs: List[List],
    head: bool = False,
) -> List[List]:
    """Levenshtein distance and size of semantic segments.

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

    def base_seg_dist(d0, d1):      # base seg dist w/o prefix drift
        dist_curr = min(d1)
        ind = [i for i, x in enumerate(d1) if x == dist_curr]
        dist_ind = max(ind)
        dist = d0[dist_ind - 1]
        return dist

    def base_seg_dist_head(d0, d1): # base seg dist with prefix drift
        return min(d0)

    base_seg_dist = base_seg_dist_head if head else base_seg_dist

    m, n = len(s), len(t)
    d0 = list(range(n+1))   # prev dist
    d1 = [0] * (n+1)        # curr dist

    base_dist = 0           # The base dist of a seg; d1[0]
    rslts = [[0] * 2 for _ in range(len(segs))]
    seg = 0

    for i in range(m):
        d1[0] = i + 1
        for j in range(n):
            c = 0 if s[i] == t[j] else 1
            d1[j+1] = min(
                d0[j] + c,    # sub s->t
                d0[j+1] + 1,  # del of s
                d1[j] + 1,    # ins to s
            )
        if seg < len(segs):
            if segs[seg][0] == i:
                base_dist = base_seg_dist(d0, d1)
            if segs[seg][1] == i + 1:
                rslts[seg][0] = segs[seg][1] - segs[seg][0]  # Seg size
                rslts[seg][1] = min(d1) - base_dist          # Seg dist
                seg += 1
        d0, d1 = d1, d0

    return rslts


def levenshtein_word_raw(
    s: List[str],
    t: List[str],
) -> List[List]:
    """Levenshtein distance of each word without examining errors.

    This function calculates the word-level levenshtein distance. The meaning
    of raw is two fold:

    1. The errors (distance being one for a word) are not examined for reasons.
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
    min_d0 = min(d0)
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


# Multiple-insertation to the source case (2+ prefix drifts):

# s = "    C D E     H I".split()
# t = "A B C D E F G H I".split()
#
# s\t j   A   B   C   D   E   F   G   H   I
# i   0+| 1   2*| 3   4   5 | 6   7 | 8   9
#    ---------------------------------------
# C   1 | 1-  2 | 2-  3   4 | 5   6 | 7   8
# D   2 | 2   2 | 3   2   3 | 4   5 | 6   7
# E   3 | 3   3 | 3   3   2+| 3   4*| 5   6
#    ---------------------------------------
# H   4 | 4   4 | 4   4   3 | 3-  4 | 4-  5
# I   5 | 5   5 | 5   5   4 | 4   4 | 5   4+


def levenshtein_word(
    s: List[str],
    t: List[str],
) -> List[List]:
    """Levenshtein distance of each word with errors examined.

    This function calculates the word-level levenshtein distance in a refined
    way as compared to levenshtein_word_raw. The meaning of refinement
    is two fold:

    1. Each error (Levenshtein dist being 1 for a word) is tested to see if
       it is a prefix hallucination.
    2. If tested as a prefix hallucination, it is split to by the two words
       on the two sides of the hallucination.
    3. If the word is at the beginning of the source, all prefix hallucinations
       will be on this word.
    4. If the word is at the end of the source, all the surfix hallucinations
       will be on this word.

    Args:
        s: Reference sequence as list of strings.
        t: Hypothesis sequence as list of strings.

    Returns:
        List of [word, levenshtein_dist] for each word, where
        levenshtein_dist is can be a real number.
    """

    m, n = len(s), len(t)
    d0 = list(range(n+1))   # prev dist
    min_d0 = min(d0)
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