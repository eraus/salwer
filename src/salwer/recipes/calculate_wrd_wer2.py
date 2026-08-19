import csv
from datetime import datetime
import os
from pathlib import Path
import shutil

from salwer.labels import Transcripts
from salwer.levenshtein import (
    levenshtein_word2,
)
from salwer.utils import (
    _clean_transcript,
    _cue_class,
    _cue_seg_ranges,
    read_file_to_text,
)
from salwer.word_dict import (
    word_dict_of_cue,
    merge_word_dicts,
)


def calculate_wrd_wer2_(
    ref_dir: str,
    hyp_dir: str,
    level: int,
    fn_cls: str,
    seg: str,
    err_limit: int,
):
    """Calculate word-level WER between ref and hyp transcripts.

    Args:
        ref_dir: Path to folder containing reference LLM files
        hyp_dir: Path to folder containing hypothesis JSON files
        level: int=3. Audio quality level (1, 2, or 3). Cues with stm starting
              with a number greater than level will be dropped.
        fn_cls: Selected class filter (optional)
        seg: Selected segment filter (optional)
    """
    dir_wrd_dict = {}

    hyp_dir = Path(hyp_dir)
    ref_dir = Path(ref_dir)

    for file in hyp_dir.glob("*.txt"):
        if file.is_file():
            hyp_file = str(file)
            ref_file = str(ref_dir / f"{file.stem}.cns")
            file_wrd_dict = word_dict_of_file(
                ref_file, hyp_file,
                level, fn_cls, seg, err_limit
            )
            dir_wrd_dict = merge_word_dicts(dir_wrd_dict, file_wrd_dict)

    os.makedirs('log', exist_ok=True)
    csv_filename = \
        f"log/word-dict-{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.csv"
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        csvfile.write(f"# ref_dir: {ref_dir}\n")
        csvfile.write(f"# hyp_dir: {hyp_dir}\n")
        csvfile.write(f"# level: {level}\n")
        csvfile.write(f"# fn_cls: {fn_cls}\n")
        csvfile.write(f"# seg: {seg}\n")
        writer = csv.writer(csvfile)
        writer.writerow(['Word', 'Occurrence x 2', 'Error x 2', 'WER'])
        for word in sorted(dir_wrd_dict.keys(),
                           key=lambda w: (-dir_wrd_dict[w][0], w)):
            occurance, error = dir_wrd_dict[word]
            wer = f"{(error/(2*occurance)):.4f}"
            writer.writerow([word, 2*occurance, error, wer])
    shutil.copy(csv_filename, 'log/word-dict.csv')

    total_word, total_dist = 0, 0
    for word in sorted(dir_wrd_dict.keys(),
                       key=lambda w: (-dir_wrd_dict[w][0], w)):
        total_word += dir_wrd_dict[word][0]
        total_dist += dir_wrd_dict[word][1]

    print(f"\nAverage WER: {(total_dist/(2*total_word)):.4f} "
          f"based on {total_word} words. ")


def word_dict_of_file(
    ref_file: str,
    hyp_file: str,
    level: int,
    fn_cls: str,
    seg: str,
    err_limit: int,
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

    return word_dict_of_ann(ref_ann, hyp_ann, fn_cls, seg, err_limit)


def word_dict_of_ann(
    ref_ann: Transcripts,
    hyp_ann: Transcripts,
    fn_cls: str,
    seg: str,
    err_limit: int,
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
        cue_wrd_list = levenshtein_word2(
            ref_cue.txt.split(), hyp_cue.txt.split(), err_limit)

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