import copy
from pathlib import Path
import re
import typer
from typing import Optional

from salwer.labels import Transcripts
from salwer.utils import (
    _clean_transcript,
    _cue_seg_ranges,
    read_file_to_text,
)
from salwer.levenshtein import seg_size_n_edit_distance

# The purpose of checking:
# - The segments are produced by LLM, which may create errors.
# - Manual editing is needed to check the LLM results.
# - Manual editing can contain errors as well.
# - We use this function to help to check the consistence between
#   the segments and the original text.
# Note:
# - We need to reduce the error in segments to the minimum since each
#   error here will be affecting the final WER
# - This checking can be done before or and after the manual editing
#   of the segments.
# - We may want to put the LLM code for creating the segments here as well.
#   For this case, we need to add one more command to create the classes and
#   segments.
def check_class_seg_(folder: str, diff: int = 0):
    """Checks class/segment of reference transcripts.

    Arguments:
    -  folder: str. Path to folder containing hypo transcript JSON files
    -  diff: bool=False. Show differences
    """
    files_checked = 0
    ref_dir = Path(folder)
    for file in ref_dir.glob("*.cns"):
        files_checked += 1
        print(f"Checking {file}:----------------------------------------------")
        if file.is_file():
            ref_file = str(file)
            # Read from original JSON file (without prefix)
            ref_file = str(ref_dir / f"{file.stem}.cns")
            _check_class_seg_file(ref_file, diff)
    print(f"Checked {files_checked} files.")


def _check_class_seg_file(ref_file: str, diff: int = 0):
    ref_text = read_file_to_text(ref_file)
    ref_ann = Transcripts.from_ref_cns_text(ref_text)
    _check_class_seg_ann(ref_ann, diff)


# The following function is used to check if the segments and the transcripts
# are consistent. If not, the results will be print out and we can check
# the original text classfication.
def _check_class_seg_ann(
        ref_ann: Transcripts, diff: int = 0, prnt: bool = False):
    segs = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
    total_edit_dist = 0
    total_num_words = 0
    for i in range(len(ref_ann.cues)):
        ref_cue = ref_ann.cues[i]
        txt = _clean_transcript(ref_cue.txt)
        ref_lst = txt.split()
        hyp_lst = copy.deepcopy(ref_lst)
        total_num_words, total_edit_dist = 0, 0
        for seg in segs:
            if ("(" + seg) not in ref_cue.cns:
                continue
            seg_ranges = _cue_seg_ranges(txt, ref_cue.cns, seg)
            if seg_ranges:
                results = seg_size_n_edit_distance(seg_ranges, ref_lst, hyp_lst)
                for seg_size, edit_dist in results:
                    total_edit_dist += edit_dist
                    total_num_words += seg_size

        if (
            prnt
            or (len(ref_lst) - total_num_words) > diff
            or total_edit_dist > 0
        ):
            print(
                f"\nTim: {ref_cue.bgn_time}; Total TXT Words: {len(ref_lst)}; "
                f"Total WER Words: {total_num_words}; "
                f"Total Dist: {total_edit_dist} ---------------------"
            )
            print(f"Txt: {ref_cue.txt}")
            print(f"CnS: {ref_cue.cns}")
