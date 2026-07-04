from pathlib import Path
import typer
from typing import Optional

from salwer.labels import Transcripts
from salwer.utils import (
    _clean_transcript,
    read_file_to_text,
)
from salwer.levenshtein import (
    levenshtein,
)


def calculate_avg_wer_(
    ref_dir: str,
    hyp_dir: str,
    level: int,
):
    """Calculate average WER reference and hypothesis transcripts.

    Args:
        ref_dir: Path to folder containing reference files
        hyp_dir: Path to folder containing hypothesis JSON files
        level: int=3. Audio quality level (1, 2, or 3). Cues with stm starting
              with a number greater than level will be dropped.
    """
    total_edit_dist = 0
    total_num_words = 0

    hyp_dir = Path(hyp_dir)
    ref_dir = Path(ref_dir)

    for file in hyp_dir.glob("*.txt"):
        if file.is_file():
            hyp_file = str(file)
            # Read from original JSON file (without prefix)
            ref_file = str(ref_dir / f"{file.stem}.cns")
            # ref_file = str(ref_dir / f"{file.stem}.llm")
            edit_dist, num_words = dist_of_file(
                ref_file, hyp_file,
                level,
            )
            total_edit_dist += edit_dist
            total_num_words += num_words

    print("\n\nResults:")
    if total_num_words > 0:
        wer = total_edit_dist / total_num_words
        typer.echo(f"Average WER is {wer}")
    typer.echo(
        f"Total edit distance {total_edit_dist}; total number of words "
        f"{total_num_words}."
    )


def dist_of_file(
    ref_file: str,
    hyp_file: str,
    level: int,
):
    ref_text = read_file_to_text(ref_file)
    ref_ann = Transcripts.from_ref_cns_text(ref_text, level)
    # ref_ann = Transcripts.from_txt_llm_text(ref_text, level)
    hyp_text = read_file_to_text(hyp_file)
    hyp_ann = Transcripts.from_asr_pred_text(hyp_text)

    print(f"{ref_file = }; {hyp_file = }------------------------------------")
    if len(ref_ann.cues) != len(hyp_ann.cues):
        raise ValueError(
            f"Num of cues mismatch: {len(ref_ann.cues)} vs {len(hyp_ann.cues)}!"
        )

    return dist_of_ann(ref_ann, hyp_ann)


def dist_of_ann(
    ref_ann: Transcripts,
    hyp_ann: Transcripts,
):

# Then use it:
    total_edit_dist = 0
    total_num_words = 0
    for i in range(len(ref_ann.cues)):
        ref_cue = ref_ann.cues[i]
        hyp_cue = hyp_ann.cues[i]
        ref_cue.txt = _clean_transcript(ref_cue.txt)
        hyp_cue.txt = _clean_transcript(hyp_cue.txt)

        dist = levenshtein(ref_cue.txt.split(), hyp_cue.txt.split())


        total_edit_dist += dist
        total_num_words += len(ref_cue.txt.split())

        if dist:
            print(f"\ntim: {ref_cue.bgn_time}")
            print(f"hyp: {hyp_cue.txt}")
            print(f"ref: {ref_cue.txt}")
            print(f"dst: {dist}")

    return total_edit_dist, total_num_words


# Note that the above _cue_seg_ranges function is revised based on AI code,
# created based on the following prompt:
# -----
# Now, we need to create the _cue_seg_ragens function in
# @src\salalp\recipes\s_class_n_seg_wer.py so that it will return the indexes
# of the selected words. Take a look at the test functions in lines 213 to 234
# in @tests\test_wer.py; the test cases and expected values are defined there.
# Essentially, we convert txt, the first argument of _cue_seg_ranges into
# a list of words, as we did in lines 206 to 210; denote it as txt_lst.
# The return of the function should be a list of lists. Each of the inner list
# contains the indexes of the words in the brackets with the seg string,
# "A" is "(A)" or "B" in "(B4)". We need to find the start and end index of
# the words in the brackets in txt_lst. Just create the code in _cue_seg_ranges
# in @src\salalp\recipes\s_class_n_seg_wer.py. I will look at the code and we
# can go from there.
# -----

# Note also that after the revision of the above code, we added more test cases,
# all of which have passed.
