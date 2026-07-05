from pathlib import Path
import typer
from typing import Optional

from salwer.labels import Transcripts
from salwer.utils import (
    _clean_transcript,
    read_file_to_text,
)
from salwer.word_dict import (
    word_count_of_cue,
    merge_word_count_dicts
)

def obtain_word_count_(
    txt_dir: str,
    level: int,
):
    """Obtain the word count dict: key = word; value = number of occurrence.

    Args:
        txt_dir: Path to dir containing the transcript files
        level: int=3. Audio quality level (1, 2, or 3). Cues with stm starting
              with a number greater than level will be dropped.
    """
    dir_wrd_dict = {}

    txt_dir = Path(txt_dir)

    for file in txt_dir.glob("*.cns"):
        if file.is_file():
            txt_file = str(file)
            # Read from original JSON file (without prefix)
            file_wrd_dict = wrd_count_of_file(txt_file, level)
            dir_wrd_dict = merge_word_count_dicts(dir_wrd_dict, file_wrd_dict)

    print("\n\nResults:")
    for key, val in dir_wrd_dict.items():
        print(f"{key = }; {val = }")


def wrd_count_of_file(
    txt_file: str,
    level: int,
):
    text = read_file_to_text(txt_file)
    ann = Transcripts.from_ref_cns_text(text, level)
    return wrd_count_of_ann(ann)


def wrd_count_of_ann(
    ann: Transcripts,
):
    file_wrd_dict = {}
    for i in range(len(ann.cues)):
        cue = ann.cues[i]
        cue.txt = _clean_transcript(cue.txt)
        cue_wrd_dict = word_count_of_cue(cue.txt)

        file_wrd_dict = merge_word_count_dicts(file_wrd_dict, cue_wrd_dict)

    return file_wrd_dict
