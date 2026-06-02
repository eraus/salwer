from salwer.levenshtein import _levenshtein_full_mem


def print_levenshtein_table_():
    """Checks class/segment of reference transcripts.

    Arguments:
    -  folder: str. Path to folder containing hypo transcript JSON files
    -  diff: bool=False. Show differences
    """
    s = "A B C D E F G H I".split()
    t = "    C D E     H I".split()

    _levenshtein_full_mem(s, t, print_d=True)

"""
    s = "    C D E     H I".split()
    t = "A B C D E F G H I".split()
    s = "  B C D E   G H I".split()
    t = "A B C D E F G H I".split()
    s = "A B A D E B G H I".split()
    t = "A B C D E F G H I".split()
    s = "A B C D E F G H I".split()
    t = "A B   D E   G H I".split()
    s = "A B   D E   G H I".split()
    t = "A B C D E F G H I".split()
    s = "  B C D E   G H I".split()
    t = "A B C D E F G H I".split()
The following strings are created from: https://www.random.org/strings/

QHFXWFBSWV
ZVCNXJCGZP
EARWGXQVXA
ZKZMNKMVWU
ELJKYWQBSK
CHTPJXRXLA
FNXRPKEYUF
CKIWLKGQDS
IDTINCJFUC
VQLPWTJDNE
PFOORIRAQP
TLYSZOBJVP
NCNRGDJWVS
PIWGPKGRWM
DRCRDHXNKQ
NHOKOOGARV
IMNUOPZMYA
JWLMEWXNOH
ZPSIZNQQVG
UDRUVANAWM
CYMAOKCYRW
QWIZXFDEQK
EPXYFVGRFN
WELLWIOBAP
GGSBSBOBBQ
DQLTRTTCZV
CHZQEYWBEC
XYIWUQEMNN
OMUZHJJFSZ
APYVHZTEQV
FUTABKHJLI
TOUIWSKBGF
QIDSKANKUK
UOTOAFFZIO
GASNUKITON
EVBZXVCBCI
KVXLTUPMBB
AVHYZFMAYS
OVNXWZAZGS
UFOJGKSWFN
"""