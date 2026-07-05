from salwer.levenshtein import levenshtein_2d


def print_levenshtein_table_():
    """Checks class/segment of reference transcripts.

    Arguments:
    -  folder: str. Path to folder containing hypo transcript JSON files
    -  diff: bool=False. Show differences
    """
    # s = "    C D E   A H I".split()
    # t = "A B C D E F G H I".split()
    s = "A B".split()
    t = "C D E".split()
    # s_st = "roger wilco"
    # t_st = "you will tell"
    levenshtein_2d(s, t, print_d=True)

