from salwer.levenshtein import levenshtein_2d


def print_levenshtein_table_(s: str, t: str):
    """Print out the levenshtein distance table of s and t.

    Arguments:
    -   s: str. The source string of alphabets.
    -   t: str. The target string of alphabets.
    """

    levenshtein_2d(s.split(), t.split(), print_d=True)
