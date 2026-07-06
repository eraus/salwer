import copy
from pathlib import Path
import re
import typer
from typing import Optional

from salwer.labels import Transcripts
from salwer.utils import (
    _clean_transcript,
    _cue_class,
    _cue_seg_ranges,
    read_file_to_text,
)
from salwer.levenshtein import (
    levenshtein_word,
    levenshtein_seg,
)


def calculate_wrd_wer_(
    ref_dir: str,
    hyp_dir: str,
    level: int,
    fn_cls: str,
    seg: str,
    lower: int,
    upper: int,
    word: str,
    lumped: str,
):
    """Calculate word-level WER between ref and hyp transcripts.

    Args:
        ref_dir: Path to folder containing reference LLM files
        hyp_dir: Path to folder containing hypothesis JSON files
        level: int=3. Audio quality level (1, 2, or 3). Cues with stm starting
              with a number greater than level will be dropped.
        fn_cls: Selected class filter (optional)
        seg: Selected segment filter (optional)

        ----

    fn_cls: str = typer.Option(
        "all", "--class", "-c",
        help=(
            "Select functional class to filter by. Default to 'all'. "
            "Other options are numerical numbers of the functional classes."
        )
    ),
    seg: str = typer.Option(
        "all", "--segment", "-s",
        help=(
            "Select semantic segment to filter by. Default to 'all'. "
            "Other options are alphabet of the semantic segments."
        )
    ),
    lower: int = typer.Option(
        1, "--lower",
        help="Set lower limit of word count for WER calculation."
    ),
    upper: int = typer.Option(
        10000000, "--upper",
        help="Set upperer limit of word count for WER calculation."
    ),
    word: str = typer.Option(
        "all--words", "--word", "-w",
        help=(
            "Choose a specific word for WER calculation. "
            "If the value is `all-words`, we will calculate the WER of all "
            "words within the above boundaries."
        )
    ),
    lumped: str = typer.Option(
        "no", "--lumped",
        help=(
            "Choose to use lumped or separate output. This is a binary valuu, "
            "which can be 'no' or 'yes'."
        )
    ),
    """
    # Check the options. TBD




    total_edit_dist = 0
    total_num_words = 0

    hyp_dir = Path(hyp_dir)
    ref_dir = Path(ref_dir)

    if seg is None:
        raise ValueError("Missing appropriate Segment Selector")

    for file in hyp_dir.glob("*.txt"):
        if file.is_file():
            hyp_file = str(file)
            # Read from original JSON file (without prefix)
            ref_file = str(ref_dir / f"{file.stem}.cns")
            # ref_file = str(ref_dir / f"{file.stem}.llm")
            edit_dist, num_words = word_dist_of_file(
                ref_file, hyp_file,
                level, fn_cls, seg,
            )
            total_edit_dist += edit_dist
            total_num_words += num_words

    print("\n\nResults:")
    if total_num_words > 0:
        wer = total_edit_dist / total_num_words
        typer.echo(f"WER of class {fn_cls} and seg {seg} is {wer}")
    typer.echo(
        f"Total edit distance {total_edit_dist}; total number of words "
        f"{total_num_words}."
    )


def word_dist_of_file(
    ref_file: str,
    hyp_file: str,
    level: int,
    fn_cls: Optional[str],
    seg: Optional[str],
    approach: str,
    head: str,
):
    ref_text = read_file_to_text(ref_file)
    ref_ann = Transcripts.from_ref_cns_text(ref_text, level)
    hyp_text = read_file_to_text(hyp_file)
    hyp_ann = Transcripts.from_asr_pred_text(hyp_text)

    print(f"{ref_file = }; {hyp_file = }------------------------------------")
    if len(ref_ann.cues) != len(hyp_ann.cues):
        raise ValueError(
            f"Num of cues mismatch: {len(ref_ann.cues)} vs {len(hyp_ann.cues)}!"
        )

    return seg_dist_of_ann(ref_ann, hyp_ann, fn_cls, seg, approach, head)


def seg_dist_of_ann(
    ref_ann: Transcripts,
    hyp_ann: Transcripts,
    fn_cls: Optional[str],
    seg: Optional[str],
    approach: str,
    head: str,
):
    # Define a mapping outside the loop for efficiency
    approach_map = {
        "normal": levenshtein_seg,
        "fast": levenshtein_seg_fast,
    }
    seg_func = approach_map.get(approach.lower(), levenshtein_seg)

# Then use it:
    use_head = True if head.lower() == "yes" else False
    total_edit_dist = 0
    total_num_words = 0
    for i in range(len(ref_ann.cues)):
        ref_cue = ref_ann.cues[i]
        hyp_cue = hyp_ann.cues[i]
        cue_class = _cue_class(ref_cue.cns)
        if fn_cls is not None and cue_class != fn_cls:
            continue

        ref_cue.txt = _clean_transcript(ref_cue.txt)
        hyp_cue.txt = _clean_transcript(hyp_cue.txt)
        cue_seg_ranges = _cue_seg_ranges(ref_cue.txt, ref_cue.cns, seg)

        cue_num_words, cue_edit_dist = 0, 0
        if cue_seg_ranges:
            results = seg_func(
                ref_cue.txt.split(),
                hyp_cue.txt.split(),
                cue_seg_ranges,
                use_head
            )
            for seg_size, edit_dist in results:
                cue_edit_dist += edit_dist
                cue_num_words += seg_size

            total_edit_dist += cue_edit_dist
            total_num_words += cue_num_words

        if cue_edit_dist:
            print(f"\ntim: {ref_cue.bgn_time}")
            print(f"hyp: {hyp_cue.txt}")
            print(f"ref: {ref_cue.txt}")
            print(f"seg: {ref_cue.cns}")
            # print(f"seg: {ref_cue.cmt}")
            print(f"dst: {cue_edit_dist}")

    return total_edit_dist, total_num_words
