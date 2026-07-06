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
from salwer.word_dict import (
    word_dict_of_cue,
    merge_word_dicts,
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

    dir_wrd_dict = {}

    hyp_dir = Path(hyp_dir)
    ref_dir = Path(ref_dir)

    for file in hyp_dir.glob("*.txt"):
        if file.is_file():
            hyp_file = str(file)
            ref_file = str(ref_dir / f"{file.stem}.cns")
            file_wrd_dict = word_dict_of_file(
                ref_file, hyp_file,
                level, fn_cls, seg,
            )
            dir_wrd_dict = merge_word_dicts(dir_wrd_dict, file_wrd_dict)

    print("\n\nResults:")
    for word in sorted(dir_wrd_dict.keys(), key=lambda w: (-dir_wrd_dict[w][0], w)):
        print(f"{word}; {dir_wrd_dict[word]}")


def word_dict_of_file(
    ref_file: str,
    hyp_file: str,
    level: int,
    fn_cls: Optional[str],
    seg: Optional[str],
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

    return word_dict_of_ann(ref_ann, hyp_ann, fn_cls, seg)


def word_dict_of_ann(
    ref_ann: Transcripts,
    hyp_ann: Transcripts,
    fn_cls: Optional[str],
    seg: Optional[str],
):
    file_wrd_dict = {}
    for i in range(len(ref_ann.cues)):
        ref_cue = ref_ann.cues[i]
        hyp_cue = hyp_ann.cues[i]
        cue_class = _cue_class(ref_cue.cns)
        if fn_cls != "all" and cue_class != fn_cls:
            continue

        ref_cue.txt = _clean_transcript(ref_cue.txt)
        hyp_cue.txt = _clean_transcript(hyp_cue.txt)
        cue_wrd_list = levenshtein_word(
            ref_cue.txt.split(), hyp_cue.txt.split())

        if seg != "all":
            cue_seg_ranges = _cue_seg_ranges(ref_cue.txt, ref_cue.cns, seg)
            cue_wrd_list = _get_seg_wrd_list(cue_wrd_list, cue_seg_ranges)

        cue_wrd_dict = word_dict_of_cue(cue_wrd_list)
        file_wrd_dict = merge_word_dicts(file_wrd_dict, cue_wrd_dict)
    return file_wrd_dict


def _get_seg_wrd_list(cue_wrd_list, cue_seg_ranges):
    result = []
    for start, end in cue_seg_ranges:
        result.extend(cue_wrd_list[start:end])
    return result