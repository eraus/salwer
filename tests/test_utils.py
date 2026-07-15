import pytest
import re

from salwer.utils import (
    _clean_transcript,
    _cue_class,
    _cue_seg_ranges,
)


def test_cue_class_1():
    """Test _cue_class with class 1 string."""
    cmt = "(1) [(A) U S Air Two Eleven] [(B4) turn left heading]"
    assert _cue_class(cmt) == "1"


def test_clean_transcript():
    """Test _clean_transcript."""
    txt = "Army Nine Three Six, traffic is V F R at er ten o'clock and two miles, he's er holding at the er outer marker."
    cleaned = "army nine three six traffic is v f r at ten oclock and two miles hes holding at the outer marker"
    assert _clean_transcript(txt) == cleaned


def test_str_to_list():
    """Verify that punctuations follow words while splitting string to list."""
    txt = "U S Air Two Eleven, turn left, heading"
    lst = ["U", "S", "Air", "Two", "Eleven,", "turn", "left,", "heading"]
    assert txt.split() == lst
    exp_low_cln = ["u", "s", "air", "two", "eleven", "turn", "left", "heading"]
    lst_low_cln = [re.sub(r"[^\w]", "", word.lower()) for word in lst]
    assert lst_low_cln == exp_low_cln


def test_cue_seg_ranges_1A():
    """Test _cue_seg_ranges with class 1 transcript and A segment."""
    txt = "U S Air Two Eleven, turn left, heading"
    seg = "(1) [(A) U S Air Two Eleven] [(B4) turn left heading]"
    seg_sel = "A"
    assert _cue_seg_ranges(txt, seg, seg_sel) == [[0, 5]]


def test_cue_seg_ranges_1B23():
    """Test _cue_seg_ranges with class 1 transcript and B segments (B2 & B3)."""
    txt = "King Air Five Charlie Foxtrot, climb and maintain niner thousand, expedite your climb, contact Departure one two one point zero five."
    seg = "(1) [(A) King Air Five Charlie Foxtrot] [(B2) climb and maintain] [(C2) niner thousand] [(E) expedite your climb] [(B3) contact] [(G) Departure] [(C3) one two one point zero five]"
    seg_sel = "B"
    assert _cue_seg_ranges(txt, seg, seg_sel) == [[5, 8], [13, 14]]


def test_cue_seg_ranges_1B4():
    """Test _cue_seg_ranges with class 1 transcript and B4 segment."""
    txt = "U S Air Two Eleven, turn left, heading"
    seg = "(1) [(A) U S Air Two Eleven] [(B4) turn left heading]"
    seg_sel = "B"
    assert _cue_seg_ranges(txt, seg, seg_sel) == [[5, 8]]


def test_cue_seg_ranges_1B6():
    """Test _cue_seg_ranges with class 1 transcript and B6 segments."""
    txt = "u s air two eleven turn your transponder on squawk six five one five youre radar contact six northwest of national"
    seg = "(1) [(A) U S Air Two Eleven] [(E) turn your transponder on] [(B6) squawk] [(C6) six five one five] [(D) you're radar contact] [(E) six northwest of [(G) National]]"
    seg_sel = "B"
    assert _cue_seg_ranges(txt, seg, seg_sel) == [[9, 10]]


def test_cue_seg_ranges_1C23():
    """Test _cue_seg_ranges with class 1 transcript and B segments (B2 & B3)."""
    txt = "King Air Five Charlie Foxtrot, climb and maintain niner thousand, expedite your climb, contact Departure one two one point zero five."
    seg = "(1) [(A) King Air Five Charlie Foxtrot] [(B2) climb and maintain] [(C2) niner thousand] [(E) expedite your climb] [(B3) contact] [(G) Departure] [(C3) one two one point zero five]"
    seg_sel = "C"
    assert _cue_seg_ranges(txt, seg, seg_sel) == [[8, 10], [15, 21]]


def test_cue_seg_ranges_3Ea():
    """Test _cue_seg_ranges with class 3 transcript and E segment."""
    txt = "It is the GORDONSVILLE zero five six zero three six, direct GORDONSVILLE, and resume your own navigation."
    seg = "(3) [(E) It is the [(H) GORDONSVILLE] zero five six zero three six] [(E) direct [(H) GORDONSVILLE]] [(E) and resume your own navigation]"
    seg_sel = "E"
    assert _cue_seg_ranges(txt, seg, seg_sel) == [[0, 3], [4, 10], [10, 11], [12, 17]]


def test_cue_seg_ranges_3Eb():
    """Test _cue_seg_ranges with class 3 transcript and E segment."""
    txt = "American Three Fourteen, cross er Jetta at, at six thousand."
    seg = "(3) [(A) American Three Fourteen] [(E) cross [(H) Jetta] at six thousand]"
    seg_sel = "E"
    assert _cue_seg_ranges(txt, seg, seg_sel) == [[3, 4], [7, 10]]


def test_cue_seg_ranges_3Ec():
    """Test _cue_seg_ranges with class 3 transcript and E segment."""
    txt = "Army Nine Three Six, traffic is V F R at er ten o'clock and two miles, he's er holding at the er outer marker."
    txt = _clean_transcript(txt)
    seg = "(3) [(A) Army Nine Three Six] [(E) traffic is V F R at ten o'clock and two miles] [(E) he's holding at the outer marker]"
    seg_sel = "E"
    assert _cue_seg_ranges(txt, seg, seg_sel) == [[4, 15], [15, 21]]


def test_cue_seg_ranges_3H2():
    """Test _cue_seg_ranges with class 3 transcript and E segment."""
    txt = "HAFNER, it'll be the GORDON zero, * GORDONSVILLE zero five six zero three six, direct GORDONSVILLE, and resume your own navigation."
    txt = _clean_transcript(txt)
    seg = "(3) [(H) HAFNER] [(E) it'll be the GORDON zero [(H) GORDONSVILLE] zero five six zero three six] [(E) direct [(H) GORDONSVILLE]] [(E) and resume your own navigation]"
    seg_sel = "H"
    assert _cue_seg_ranges(txt, seg, seg_sel) == [[0, 1], [6, 7], [14, 15]]


def test_cue_seg_ranges_4E():
    """Test _cue_seg_ranges with class 4 transcript and E segment with er."""
    txt = "The second layer tops out about er seventy five, there's another layer we're entering now about er ten thousand."
    txt = _clean_transcript(txt)
    seg = "(4) [(E) The second layer tops out about seventy five] [(E) there's another layer we're entering now about ten thousand.]"
    seg_sel = "E"
    assert _cue_seg_ranges(txt, seg, seg_sel) == [[0, 8], [8, 17]]
