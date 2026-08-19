"""Functions used for different level LD calculation based on aligned seqs."""


def attribute_wl_gld(
    s:list[str],    # source sequence
    e:list[str],    # error indicator sequence
) -> list[list]:
    """Attribute word-level generalized LD based on given s adn e sequences.

    Arguments:
    - s:list[str]. Source sequence used for providing words of interests
    - e:list[str]. Error indicator sequence corresponding to words in s:
        - " " for no error (same elements between s and t sequences)
        - "D" for deletion (del.) (the element in s is missing in t)
        - "S" for substitution (sub.) (different element values in s and t)
        - "I" for insertion (ins.) (hallucination in t as compared to s)

    Return:
    -   wlst: Word list---list of [word, GLD] for each word in s; GLD is float.
    """

    m = len(e)
    wlst = [[0.0] * 2 for _ in range(m)]  # wlst = word list

    # Attribute del errors:
    for ind, word in enumerate(e):
        wlst[ind][0] = s[ind]       # assign each element of s
        if word == "D":
            wlst[ind][1] = 1.0

    # Attribute sub only errors:
    sub_inds = find_sub_index(e)
    for inds in sub_inds:
        for ind in range(inds[0], inds[1]):
            wlst[ind][1] = 1.0

    # Attribute sub-ins errors:
    ins_sub_ind_num_sub_list = find_ins_sub_index_num_of_sub(e)
    for ins_sub_ind_num_sub in ins_sub_ind_num_sub_list:
        # length of the entire sub_ins sequence; used for indexes
        len_seq = 1.0 * (ins_sub_ind_num_sub[1] - ins_sub_ind_num_sub[0])
        sub_share = len_seq - 1  # share of blame by the subs.
        if ins_sub_ind_num_sub[2] == 0:  # no subs. in ins. sequence
            if ins_sub_ind_num_sub[0] == 0:        # head insertion
                wlst[ins_sub_ind_num_sub[1]][1] += len_seq
            elif ins_sub_ind_num_sub[1] == m:      # tail insertion
                wlst[ins_sub_ind_num_sub[0] - 1][1] += len_seq
            else:                       # normal insertion
                wlst[ins_sub_ind_num_sub[0] - 1][1] += len_seq/2
                wlst[ins_sub_ind_num_sub[1]][1] += len_seq/2
        else:   # there are subs. in sub-ins sequence
            if ins_sub_ind_num_sub[0] == 0:        # head insertion
                wlst[ins_sub_ind_num_sub[1]][1] += 0.5  # for anchor
                each_share = (sub_share + 0.5) / ins_sub_ind_num_sub[2]
            elif ins_sub_ind_num_sub[1] == m:      # tail insertion
                wlst[ins_sub_ind_num_sub[0] - 1][1] += 0.5
                each_share = (sub_share + 0.5) / ins_sub_ind_num_sub[2]
            else:                       # normal insertion
                wlst[ins_sub_ind_num_sub[0] - 1][1] += 0.5
                wlst[ins_sub_ind_num_sub[1]][1] += 0.5
                each_share = sub_share / ins_sub_ind_num_sub[2]
            # Update LD for elements corresponding to subs.
            for ind in range(ins_sub_ind_num_sub[0], ins_sub_ind_num_sub[1]):
                if e[ind] == "S":
                    wlst[ind][1] += each_share
    # Remove empty elements:
    reduced_wlst = []
    for pair in wlst:
        c, _ = pair[0], pair[1]
        if c != " ":
            reduced_wlst.append(pair)

    return reduced_wlst


def find_sub_index(
    e:list[str],    # error indicator sequence
) -> list[list[int]]:
    """Find the indexes of substitutions from the e sequence.

    Two examples for illustration:

    Example 1: subs. w/o ins.:
       e = ["S", "S", " ", " ", " ", "S", "S", " ", " "]
     index:  0    1    2    3    4    5    6    7    8
       exp_ind_lst = [[0, 2], [5, 7]]

    Example 2: sub. connected to ins.:
       e = [" ", "S", " ", "D", " ", "S", "I", " ", "I"]
     index:  0    1    2    3    4    5    6    7    8
       exp_ind_lst = [[1, 2]]

    Arguments:
    - e:list[str]. Error indicator sequence corresponding to words in s:
        - " " for no error (same elements between s and t sequences)
        - "D" for deletion (del.) (the element in s is missing in t)
        - "S" for substitution (sub.) (different element values in s and t)
        - "I" for insertion (ins.) (hallucination in t as compared to s)

    Return:
    -   sub_ind_lst: list of index of subs., as shown in above examples.
    """

    m = len(e)
    sub_ind_list = []
    ind = 0
    while ind < m:
        # Skip all spaces and "D"'s.
        while ind < m and (e[ind] == " " or e[ind] == "D"):
            ind += 1
        if ind >= m:
            break

        # Find start and end of sequence of "I" or "S".
        group_start = ind
        has_ins = False
        while ind < m and e[ind] != " " and e[ind] != "D":
            if e[ind] == "I":
                has_ins = True      # sequence with "I"
            ind += 1
        group_end = ind

        if not has_ins:
            sub_ind_list.append([group_start, group_end])
    return sub_ind_list


def find_ins_sub_index_num_of_sub(
    e:list[str],    # error indicator sequence
) -> list[list[int]]:
    """Find the indexes of sub.-including ins. seq. plus number of subs.

    This is a sequence of ins., but there can be subs.; the number of subs.
    should be included. Two examples for illustration:

    Example 1: head inserts and consecutive inserts:
       e = ["I", "I", "S", " ", " ", "I", "S", "I", "S"]
     index:  0    1    2    3    4    5    6    7    8
       exp_ind_lst = [[0, 3, 1], [5, 9, 2]]

    Example 2: middle insert and tail insert:
       e = [" ", "S", " ", "D", " ", "S", "I", " ", "I"]
     index:  0    1    2    3    4    5    6    7    8
       exp_ind_lst = [[5, 7, 1], [8, 9, 0]]

    Arguments:
    - e:list[str]. Error indicator sequence corresponding to words in s:
        - " " for no error (same elements between s and t sequences)
        - "D" for deletion (del.) (the element in s is missing in t)
        - "S" for substitution (sub.) (different element values in s and t)
        - "I" for insertion (ins.) (hallucination in t as compared to s)

    Return:
    -   ins_sub_ind_lst: list of index of subs., as shown in above examples.
    """

    m = len(e)
    ins_sub_ind_lst = []
    to_find_bgn_sub_ins:bool = True     # flag to find begin index
    num_subs = 0
    num_ins = 0
    for ind, word in enumerate(e):
        if to_find_bgn_sub_ins:
            if word == "S":
                num_subs += 1
                sub_ins_bgn_ind = ind
                to_find_bgn_sub_ins = False   # need to find end index
            elif word == "I":
                num_ins += 1
                sub_ins_bgn_ind = ind
                to_find_bgn_sub_ins = False   # need to find end index
                if ind == m-1:      # find end index at end of list
                    sub_ins_end_ind = ind+1
                    if num_ins:
                        ins_sub_ind_lst.append(
                            [sub_ins_bgn_ind, sub_ins_end_ind, num_subs]
                        )
        else:
            if word == " " or word == "D": # find end index before end of list
                sub_ins_end_ind = ind
                to_find_bgn_sub_ins = True
                if num_ins:
                    ins_sub_ind_lst.append(
                        [sub_ins_bgn_ind, sub_ins_end_ind, num_subs]
                    )
                num_subs = 0
            else:
                if word == "S":     # find another 'S'
                    num_subs += 1
                elif word == "I":   # find another 'I'.
                    num_ins += 1
                if ind == m-1:      # find end index at end of list
                    sub_ins_end_ind = ind+1
                    if num_ins:
                        ins_sub_ind_lst.append(
                            [sub_ins_bgn_ind, sub_ins_end_ind, num_subs]
                        )
    return ins_sub_ind_lst
