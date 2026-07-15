import pytest

from salwer.labels import Transcripts
from salwer.recipes.inspect_llm_class_n_seg_results import (
    _inspect_class_seg_ann,
)


cns_text = """
stm: 1>D1-2>N5CF
tim: 3502290
txt: King Air Five Charlie Foxtrot, climb and maintain niner thousand, expedite your climb, contact Departure one two one point zero five.
cns: (1) [(A) King Air Five Charlie Foxtrot] [(B2) climb and maintain] [(C2) niner thousand] [(E) expedite your climb] [(B3) contact] [(G) Departure] [(C3) one two one point zero five]

stm: 2>N5CF>D1-2
tim: 3509240
txt: Twenty one zero five, expediting to niner thousand, Seven Five Charlie Fox, good day now.
cns: (2) [(C3) Twenty one zero five] [(B2) expediting to] [(C2) niner thousand] [(A) Seven Five Charlie Fox] [(I) good day now]

stm: 1>D1-2>USA211
tim: 3536270
txt: U S Air Two Eleven, turn left, heading two three zero, expect on course in twelve miles.
cns: (1) [(A) U S Air Two Eleven] [(B4) turn left heading] [(C4) two three zero] [(E) expect on course in twelve miles]

stm: 1>USA211>D1-2
tim: 3541460
txt: Two thirty the heading, U S Air Two Eleven.
cns: (2) [(C4) Two thirty] [(J) the heading] [(A) U S Air Two Eleven]

stm: 1>D1-2>N5CF
tim: 3308200
txt: HAFNER, it'll be the GORDON zero, * GORDONSVILLE zero five six zero three six, direct GORDONSVILLE, and resume your own navigation.
cns: (3) [(H) HAFNER] [(E) it'll be the GORDON [(H) GORDONSVILLE] zero five six zero three six] [(E) direct [(H) GORDONSVILLE]] [(E) and resume your own navigation]

stm: 2>N5CF>D1-2
tim: 3313860
txt: Charlie Fox, roger, thank you.
cns: (4) [(A) Charlie Fox] [(D) roger] [(I) thank you]

stm: 2>D1-2>N5CF
tim: 3350190
txt: King Air Five Charlie Foxtrot, expect climb in about seven miles.
cns: (3) [(A) King Air Five Charlie Foxtrot] [(E) expect climb in about seven miles]

stm: 1>N5CF>D1-2
tim: 3353220
txt: Charlie Fox, roger.
cns: (4) [(A) Charlie Fox] [(D) roger]
"""

def test_inspect_class_seg_ann():
    """Test _inspect_class_seg_ann using cns_text."""
    ann = Transcripts.from_ref_cns_text(cns_text)
    # _inspect_class_seg_ann(ann, prnt=True)
    _inspect_class_seg_ann(ann)
