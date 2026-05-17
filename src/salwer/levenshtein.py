from typing import List


def edit_distance(ref: List[str], hyp: List[str]) -> int:
    return _edit_distance(ref, hyp)


def _edit_distance_full_mem(ref: List[str], hyp: List[str]) -> int:
    """Full-memory implementation of the Levenshtein distance"""

    m, n = len(ref), len(hyp)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            cost = 0 if ref[i - 1] == hyp[j - 1] else 1
            dp[i][j] = min(
                dp[i - 1][j] + 1,  # deletion
                dp[i][j - 1] + 1,  # insertion
                dp[i - 1][j - 1] + cost,  # substitution
            )

    return dp[m][n]


def _edit_distance(ref: List[str], hyp: List[str]) -> int:
    """Two-list implementation of the Levenshtein distance"""

    m, n = len(ref), len(hyp)
    prev = list(range(n + 1))
    curr = [0] * (n + 1)

    for i in range(1, m + 1):
        curr[0] = i
        for j in range(1, n + 1):
            cost = 0 if ref[i - 1] == hyp[j - 1] else 1
            curr[j] = min(
                prev[j] + 1,  # deletion
                curr[j - 1] + 1,  # insertion
                prev[j - 1] + cost,  # substitution
            )
        prev = curr.copy()

    return prev[n]


def _edit_distance_mem_efficient(ref: List[str], hyp: List[str]) -> int:
    """Single-list implementation of the Levenshtein distance"""

    m, n = len(ref), len(hyp)
    dp = list(range(n + 1))

    for i in range(1, m + 1):
        prev = dp[0]
        dp[0] = i
        for j in range(1, n + 1):
            curr = dp[j]
            cost = 0 if ref[i - 1] == hyp[j - 1] else 1
            dp[j] = min(
                dp[j] + 1,  # deletion
                dp[j - 1] + 1,  # insertion
                prev + cost,  # substitution
            )
            prev = curr

    return dp[n]


def seg_size_n_edit_distance(
    segs: List[List],
    ref: List[str],
    hyp: List[str],
) -> List[List]:
    """Compute edit distance for segmented parts of ref and hyp sequences.

    This function takes a list of segments, where each segment is defined by
    [start, end] indices, and computes the edit distance between the
    corresponding slices of ref and hyp for each segment.

    Args:
        segs: List of segments, each segment is [start, end].
        ref: Reference sequence as list of strings.
        hyp: Hypothesis sequence as list of strings.

    Returns:
        List of [segment_length, edit_distance] for each segment, where
        segment_length = end - start,
        edit_distance = edit dist btwn ref[start:end] and hyp[start:end].
    """

    m, n = len(ref), len(hyp)
    prev = list(range(n + 1))
    curr = [0] * (n + 1)

    dist = 0  # The start distance, corresponds to curr[0]
    rslts = [[0] * len(segs[0]) for _ in range(len(segs))]
    seg = 0

    # for i in range(1, m + 1):
    #     curr[0] = i
    #     for j in range(1, n + 1):
    #         cost = 0 if ref[i - 1] == hyp[j - 1] else 1
    #         curr[j] = min(
    #             prev[j] + 1,  # deletion
    #             curr[j - 1] + 1,  # insertion
    #             prev[j - 1] + cost,  # substitution
    #         )
    #     if seg < len(segs):
    #         if segs[seg][0] == i - 1 and i > 0:
    #             dist = min(prev)
    #         if segs[seg][1] == i:
    #             rslts[seg][0] = segs[seg][1] - segs[seg][0]  # Size of seg
    #             rslts[seg][1] = min(curr) - dist  # edit distance
    #             seg += 1
    #     prev = curr.copy()

    for i in range(1, m + 1):
        curr[0] = i
        for j in range(1, n + 1):
            cost = 0 if ref[i - 1] == hyp[j - 1] else 1
            curr[j] = min(
                prev[j] + 1,  # deletion
                curr[j - 1] + 1,  # insertion
                prev[j - 1] + cost,  # substitution
            )
        if seg < len(segs):
            if segs[seg][0] == i - 1 and i > 0:
                dist_curr = min(curr)
                ind = [i for i, x in enumerate(curr) if x == dist_curr]
                dist_ind = max(ind)
                dist = prev[dist_ind -1]
            if segs[seg][1] == i:
                rslts[seg][0] = segs[seg][1] - segs[seg][0]  # Size of seg
                rslts[seg][1] = min(curr) - dist  # edit distance
                seg += 1
        prev = curr.copy()

    return rslts
