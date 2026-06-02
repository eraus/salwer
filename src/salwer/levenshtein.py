from typing import List
from rapidfuzz import fuzz


def levenshtein(s: List[str], t: List[str]) -> int:
    return _levenshtein(s, t)


# def _edit_distance_full_mem(ref: List[str], hyp: List[str]) -> int:
#     """Full-memory implementation of the Levenshtein distance"""

#     m, n = len(ref), len(hyp)
#     dp = [[0] * (n + 1) for _ in range(m + 1)]

#     for i in range(m + 1):
#         dp[i][0] = i
#     for j in range(n + 1):
#         dp[0][j] = j

#     for i in range(1, m + 1):
#         for j in range(1, n + 1):
#             cost = 0 if ref[i - 1] == hyp[j - 1] else 1
#             dp[i][j] = min(
#                 dp[i - 1][j] + 1,  # deletion
#                 dp[i][j - 1] + 1,  # insertion
#                 dp[i - 1][j - 1] + cost,  # substitution
#             )

#     return dp[m][n]


def _levenshtein_full_mem(
        s: List[str],
        t: List[str],
        print_d: bool = False,  # True to print
    ) -> int:
    """Full-memory implementation of the Levenshtein distance."""

    # m, n = len(s), len(t)
    # d = [[0] * (n+1) for _ in range(m+1)]
    # for i in range(m+1):
    #     d[i][0] = i
    # for j in range(n+1):
    #     d[0][j] = j
    # for i in range(1, m+1):
    #     for j in range(1, n+1):
    #         cost = 0 if s[i-1] == t[j-1] else 1
    #         d[i][j] = min(
    #             d[i-1][j] + 1,      # deletion of source
    #             d[i][j-1] + 1,      # insertion to source
    #             d[i-1][j-1] + cost, # substitution
    #         )
    # return d[m][n]

    m, n = len(s), len(t)
    d = [[0] * (n+1) for _ in range(m+1)]
    for i in range(m+1):
        d[i][0] = i
    for j in range(n+1):
        d[0][j] = j
    for i in range(m):      # row index
        for j in range(n):  # col index
            c = 0 if s[i] == t[j] else 1
            d[i+1][j+1] = min(
                d[i][j+1] + 1,  # del of s
                d[i+1][j] + 1,  # ins to s
                d[i][j] + c,    # subs
            )
    if print_d:
        print("s\\t j   " + '   '.join(t))
        print("i   " + '   '.join(str(num) for num in d[0]))
        for ch, row in zip(s, d[1:]):
            print(ch + "   " + '   '.join(str(num) for num in row))
    return d[m][n]


# def _edit_distance(ref: List[str], hyp: List[str]) -> int:
#     """Two-list implementation of the Levenshtein distance"""

#     m, n = len(ref), len(hyp)
#     prev = list(range(n + 1))
#     curr = [0] * (n + 1)

#     for i in range(1, m + 1):
#         curr[0] = i
#         for j in range(1, n + 1):
#             cost = 0 if ref[i - 1] == hyp[j - 1] else 1
#             curr[j] = min(
#                 prev[j] + 1,  # deletion
#                 curr[j - 1] + 1,  # insertion
#                 prev[j - 1] + cost,  # substitution
#             )
#         prev = curr.copy()

#     return prev[n]


def _levenshtein(s: List[str], t: List[str]) -> int:
    """Two-list implementation of the Levenshtein distance"""

    m, n = len(s), len(t)
    d0 = list(range(n+1))  # prev dist
    d1 = [0] * (n+1)       # curr dist
    for i in range(m):
        d1[0] = i + 1
        for j in range(n):
            c = 0 if s[i] == t[j] else 1
            d1[j+1] = min(
                d0[j+1] + 1,  # del of s
                d1[j] + 1,    # ins to s
                d0[j] + c,    # subs
            )
        d0, d1 = d1, d0
    return d0[n]


# def _edit_distance_mem_efficient(ref: List[str], hyp: List[str]) -> int:
#     """Single-list implementation of the Levenshtein distance"""

#     m, n = len(ref), len(hyp)
#     dp = list(range(n + 1))

#     for i in range(1, m + 1):
#         prev = dp[0]
#         dp[0] = i
#         for j in range(1, n + 1):
#             curr = dp[j]
#             cost = 0 if ref[i - 1] == hyp[j - 1] else 1
#             dp[j] = min(
#                 dp[j] + 1,  # deletion
#                 dp[j - 1] + 1,  # insertion
#                 prev + cost,  # substitution
#             )
#             prev = curr

#     return dp[n]


def _levenshtein_one_list(s: List[str], t: List[str]) -> int:
    """Single-list implementation of the Levenshtein distance"""

    m, n = len(s), len(t)
    d = list(range(n+1))
    for i in range(m):
        d0 = d[0]
        d[0] = i + 1
        for j in range(n):
            d1 = d[j+1]
            c = 0 if s[i] == t[j] else 1
            d[j+1] = min(
                d[j+1] + 1,  # del of s
                d[j] + 1,    # ins to s
                d0 + c,      # sub
            )
            d0 = d1
    return d[n]


def seg_size_n_edit_distance(
    segs: List[List],
    ref: List[str],
    hyp: List[str],
) -> List[List]:
    pass
#     """Compute edit distance for segmented parts of ref and hyp sequences.

#     This function takes a list of segments, where each segment is defined by
#     [start, end] indices, and computes the edit distance between the
#     corresponding slices of ref and hyp for each segment.

#     Args:
#         segs: List of segments, each segment is [start, end].
#         ref: Reference sequence as list of strings.
#         hyp: Hypothesis sequence as list of strings.

#     Returns:
#         List of [segment_length, edit_distance] for each segment, where
#         segment_length = end - start,
#         edit_distance = edit dist btwn ref[start:end] and hyp[start:end].
#     """

#     m, n = len(ref), len(hyp)
#     prev = list(range(n + 1))
#     curr = [0] * (n + 1)

#     dist = 0  # The start distance, corresponds to curr[0]
#     rslts = [[0] * len(segs[0]) for _ in range(len(segs))]
#     seg = 0

#     # for i in range(1, m + 1):
#     #     curr[0] = i
#     #     for j in range(1, n + 1):
#     #         cost = 0 if ref[i - 1] == hyp[j - 1] else 1
#     #         curr[j] = min(
#     #             prev[j] + 1,  # deletion
#     #             curr[j - 1] + 1,  # insertion
#     #             prev[j - 1] + cost,  # substitution
#     #         )
#     #     if seg < len(segs):
#     #         if segs[seg][0] == i - 1 and i > 0:
#     #             dist = min(prev)
#     #         if segs[seg][1] == i:
#     #             rslts[seg][0] = segs[seg][1] - segs[seg][0]  # Size of seg
#     #             rslts[seg][1] = min(curr) - dist  # edit distance
#     #             seg += 1
#     #     prev = curr.copy()

#     for i in range(1, m + 1):
#         curr[0] = i
#         for j in range(1, n + 1):
#             cost = 0 if ref[i - 1] == hyp[j - 1] else 1
#             curr[j] = min(
#                 prev[j] + 1,  # deletion
#                 curr[j - 1] + 1,  # insertion
#                 prev[j - 1] + cost,  # substitution
#             )
#         if seg < len(segs):
#             if segs[seg][0] == i - 1 and i > 0:
#                 dist_curr = min(curr)
#                 ind = [i for i, x in enumerate(curr) if x == dist_curr]
#                 dist_ind = max(ind)
#                 dist = prev[dist_ind -1]
#             if segs[seg][1] == i:
#                 rslts[seg][0] = segs[seg][1] - segs[seg][0]  # Size of seg
#                 rslts[seg][1] = min(curr) - dist  # edit distance
#                 seg += 1
#         prev = curr.copy()

#     return rslts


def levenshtein_n_seg_size_tail(
    s: List[str],
    t: List[str],
    segs: List[List],
) -> List[List]:
    """Levenshtein distance and size for semantic segments.

    This function takes a list of segments, where each segment is defined by
    [start, end] indices, and computes the Levenshtein distance between the
    corresponding slices of ref and hyp for each segment.

    Args:
        s: Reference sequence as list of strings.
        t: Hypothesis sequence as list of strings.
        segs: List of segments, each segment is [start, end].

    Returns:
        List of [segment_length, edit_distance] for each segment, where
        segment_length = end - start,
        edit_distance = edit dist btwn ref[start:end] and hyp[start:end].
    """

    m, n = len(s), len(t)
    d0 = list(range(n+1))   # prev dist
    d1 = [0] * (n+1)        # curr dist

    dist = 0    # The start distance, corresponding to d1[0]
    rslts = [[0] * 2 for _ in range(len(segs))]
    seg = 0

    for i in range(m):
        d1[0] = i + 1
        for j in range(n):
            c = 0 if s[i] == t[j] else 1
            d1[j+1] = min(
                d0[j+1] + 1,  # deletion
                d1[j] + 1,  # insertion
                d0[j] + c,  # substitution
            )
        if seg < len(segs):
            # if segs[seg][0] == i and i > 1:
            if segs[seg][0] == i and i > 0:
                dist_curr = min(d1)
                ind = [i for i, x in enumerate(d1) if x == dist_curr]
                dist_ind = max(ind)
                dist = d0[dist_ind - 1]
            if segs[seg][1] == i + 1:
                rslts[seg][0] = segs[seg][1] - segs[seg][0]  # Size of seg
                rslts[seg][1] = min(d1) - dist  # edit distance
                seg += 1
        d0, d1 = d1, d0

    return rslts


def levenshtein_n_seg_size_head(
    s: List[str],
    t: List[str],
    segs: List[List],
) -> List[List]:
    """Levenshtein distance and size for semantic segments.

    This function takes a list of segments, where each segment is defined by
    [start, end] indices, and computes the Levenshtein distance between the
    corresponding slices of ref and hyp for each segment.

    Args:
        s: Reference sequence as list of strings.
        t: Hypothesis sequence as list of strings.
        segs: List of segments, each segment is [start, end].

    Returns:
        List of [segment_length, edit_distance] for each segment, where
        segment_length = end - start,
        edit_distance = edit dist btwn ref[start:end] and hyp[start:end].
    """

    m, n = len(s), len(t)
    d0 = list(range(n+1))   # prev dist
    d1 = [0] * (n+1)        # curr dist

    dist = 0    # The start distance, corresponding to d1[0]
    rslts = [[0] * 2 for _ in range(len(segs))]
    seg = 0

    for i in range(m):
        d1[0] = i + 1
        for j in range(n):
            c = 0 if s[i] == t[j] else 1
            d1[j+1] = min(
                d0[j+1] + 1,  # deletion
                d1[j] + 1,  # insertion
                d0[j] + c,  # substitution
            )
        if seg < len(segs):
            # if segs[seg][0] == i and i > 1:
            if segs[seg][0] == i and i > 0:
                dist = min(d0)
            if segs[seg][1] == i + 1:
                rslts[seg][0] = segs[seg][1] - segs[seg][0]  # Size of seg
                rslts[seg][1] = min(d1) - dist  # edit distance
                seg += 1
        d0, d1 = d1, d0

    return rslts


def levenshtein_n_seg_size(
    s: List[str],
    t: List[str],
    segs: List[List],
    head: bool = False,
) -> List[List]:
    """Levenshtein distance and size for semantic segments.

    This function takes a list of segments, where each segment is defined by
    [start, end] indices, and computes the Levenshtein distance between the
    corresponding slices of ref and hyp for each segment.

    Args:
        s: Reference sequence as list of strings.
        t: Hypothesis sequence as list of strings.
        segs: List of segments, each segment is [start, end].
        head: Boolean indicator for including insertions before the segment:
            True: include
            False: do not include

    Returns:
        List of [segment_length, edit_distance] for each segment, where
        segment_length = end - start,
        edit_distance = edit dist btwn ref[start:end] and hyp[start:end].
    """

    def seg_dist_no_head(d0, d1):  # seg dist without head hallucination
        dist_curr = min(d1)
        ind = [i for i, x in enumerate(d1) if x == dist_curr]
        dist_ind = max(ind)
        dist = d0[dist_ind - 1]
        return dist

    def seg_dist_with_head(d0, d1):  # seg dist with head hallucination
        return min(d0)

    seg_dist = seg_dist_with_head if head else seg_dist_no_head

    m, n = len(s), len(t)
    d0 = list(range(n+1))   # prev dist
    d1 = [0] * (n+1)        # curr dist

    dist = 0    # The start distance, corresponding to d1[0]
    rslts = [[0] * 2 for _ in range(len(segs))]
    seg = 0

    for i in range(m):
        d1[0] = i + 1
        for j in range(n):
            c = 0 if s[i] == t[j] else 1
            d1[j+1] = min(
                d0[j+1] + 1,  # deletion
                d1[j] + 1,  # insertion
                d0[j] + c,  # substitution
            )
        if seg < len(segs):
            # if segs[seg][0] == i and i > 1:
            # if segs[seg][0] == i and i > 0:
            if segs[seg][0] == i:
                dist = seg_dist(d0, d1)
            if segs[seg][1] == i + 1:
                rslts[seg][0] = segs[seg][1] - segs[seg][0]  # Size of seg
                rslts[seg][1] = min(d1) - dist  # edit distance
                seg += 1
        d0, d1 = d1, d0

    return rslts


# def rmin(d_row):
#     # min_d = d_row[-1]
#     for i in range(len(d_row) - 1, 0, -1):  # go backwards
#         min_d = d_row[i]
#         if d_row[i] != d_row[i-1] + 1:
#             break  # First match from the right is the last match overall
#     return min_d


# # Need to convert the following code to a function named remove_asr_prefix, which is used to remove the prefix hallucination from the ASR transcript. The will be two items for the return: string of removed words, string of kept words.

# Will consider if we need to add faked start word if the first word in s and t are not the same. With this, we can better align the sequences. Note that if we add a long enough fixed sequence, we don't need to worry about the alignment anymore. We can consider this approach. This is only added if the first words the strings are not the same.


# # Your two sequences
# ref = "climb and maintain one zero thousand"
# hyp = "uh yeah tower said climb maintain one zero thousand"

# # Get similarity score and alignment positions
# result = fuzz.partial_ratio_alignment(ref, hyp)

# # Extract the aligned regions
# aligned_in_seq1 = ref[result.src_start:result.src_end]
# aligned_in_seq2 = hyp[result.dest_start:result.dest_end]

# print(f"\n🔍 Aligned regions:")
# print(f"   Seq1: '{aligned_in_seq1}'")
# print(f"   Seq2: '{aligned_in_seq2}'")