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
    levenshtein_seg,
    levenshtein_seg_fast,
)


def calculate_avg_wer_(
    ref_dir: str,
    hyp_dir: str,
    level: int,
    words: str,
    approach: str,
):
    """Calculate average WER reference and hypothesis transcripts.

    Args:
        ref_dir: Path to folder containing reference files
        hyp_dir: Path to folder containing hypothesis JSON files
        level: int=3. Audio quality level (1, 2, or 3). Cues with stm starting
              with a number greater than level will be dropped.
    """
    if words.lower() not in ('all', 'first', 'second+'):
        raise ValueError(
            f"Value of 'section' can only be 'all', 'first', and 'second+'!"
        )
    total_edit_dist = 0
    total_num_words = 0

    hyp_dir = Path(hyp_dir)
    ref_dir = Path(ref_dir)

    for file in hyp_dir.glob("*.txt"):
        if file.is_file():
            hyp_file = str(file)
            ref_file = str(ref_dir / f"{file.stem}.cns")
            edit_dist, num_words = dist_of_file(
                ref_file, hyp_file,
                level, words, approach
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
    words: str,
    approach: str,
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

    return dist_of_ann(ref_ann, hyp_ann, words, approach)


def dist_of_ann(
    ref_ann: Transcripts,
    hyp_ann: Transcripts,
    words: str,
    approach: str,
):
    # Define a mapping outside the loop for efficiency
    approach_map = {
        "normal": levenshtein_seg,
        "fast": levenshtein_seg_fast,
    }
    seg_func = approach_map.get(approach.lower(), levenshtein_seg)

# Then use it:
    total_edit_dist = 0
    total_num_words = 0
    for i in range(len(ref_ann.cues)):
        ref_cue = ref_ann.cues[i]
        hyp_cue = hyp_ann.cues[i]
        ref_cue.txt = _clean_transcript(ref_cue.txt)
        hyp_cue.txt = _clean_transcript(hyp_cue.txt)
        seg_size = len(ref_cue.txt.split())
        if words.lower() == "all":
            dist = levenshtein(ref_cue.txt.split(), hyp_cue.txt.split())
        else:
            if words.lower() == "first":
                cue_seg_ranges = [(0, 1)]
            else:
                cue_seg_ranges = [(1, seg_size)]
            # results = levenshtein_seg_fast(
            results = seg_func(
                ref_cue.txt.split(),
                hyp_cue.txt.split(),
                cue_seg_ranges,
                head=True
            )
            seg_size, dist = results[0]

        total_edit_dist += dist
        total_num_words += seg_size

        if dist:
            print(f"\ntim: {ref_cue.bgn_time}")
            print(f"hyp: {hyp_cue.txt}")
            print(f"ref: {ref_cue.txt}")
            print(f"dst: {dist}")

    return total_edit_dist, total_num_words
