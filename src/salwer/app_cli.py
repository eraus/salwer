from pathlib import Path
import os
import typer
from typing import List

from .recipes.calculate_avg_wer import calculate_avg_wer_
from .recipes.calculate_seg_wer import calculate_seg_wer_
from .recipes.calculate_wrd_wer import calculate_wrd_wer_
from .recipes.calculate_wrd_wer2 import calculate_wrd_wer2_
from .recipes.obtain_word_count import obtain_word_count_
from .recipes.inspect_llm_class_n_seg_results import inspect_class_seg_
from .recipes.class_n_seg_cues_with_llm import class_n_seg_cues_
from .recipes.print_levenshtein_table import print_levenshtein_table_


__version__ = "0.1.0"
app = typer.Typer()


########################################################################
# Version command
@app.command()
def version():
    """Print the version."""
    typer.echo(f"Version of salalp: {__version__}")


@app.command("calculate-average-wer")
@app.command("caw")
def calculate_avg_wer(
    ref_dir: str = typer.Argument(
        ..., help="Specify the directory containing reference files."
    ),
    hyp_dir: str = typer.Argument(
        ..., help="Specify the directory containing hypothesis files."
    ),
    level: int = typer.Option(
        3, "--level", "-l",
        help=(
            "Choose audio quality level (1, 2, or 3) and below; "
            "for example, Level 3 will include also Levels 1 and 2. "
            "The value of `level` must match the level value used during ASR."
        )
    ),
    words: str = typer.Option(
        "all", "--words",
        help=(
            "Choose a `section` of interests WER calculation: "
            "'all' for all words, "
            "'first' for the first word, "
            "and 'second+' for all words except the first."
        )
    ),
    approach: str = typer.Option(
        "normal", "--approach", "-a",
        help=(
            "Calculation approach for segment-based Levenshtein distance (LD) "
            "calculation: normal or fast. "
            "This is only applicable if the `words` option is `first` "
            "or `second+`,  with which seg-level WER functions will be used."
        )
    ),
):
    """Calculate the average WER of all, first, and second+ words.

    Arguments:
    -   ref_dir: str. Directory containing ref files (currently, cns files).
    -   hyp_dir: str. Directory containing hyp files (currently, txt files).
    -   level: int=3. Audio quality level (1, 2, or 3). Cues with stm starting
            with a number greater than the value of level will be dropped.
    -   words: str. All, the first, or all-but-the-first. Valid values:
            (1) `all` (default), (2) `first`, and (3) `second+`.
    -   approach: str. The approach used for calculating WER. Valid values:
            (1) `normal` (default) and (2) `fast`.

    Example: (executed in the parent folder of the ref folder)
    -   salwer caw ref b12_aug2_l12 --level 2
    -   salwer caw ref b12_aug2_l12 --level 2 --word first
    -   salwer caw ref b12_aug2_l12 --level 2 --word second+
    -   salwer caw ref b12_aug2_l12 --level 2 --word second+ --approach fast
    """

    return calculate_avg_wer_(ref_dir, hyp_dir, level, words, approach)


@app.command("calculate-seg-wer")
@app.command("csw")
def calculate_seg_wer(
    ref_dir: str = typer.Argument(
        ..., help="Specify the directory containing reference files."
    ),
    hyp_dir: str = typer.Argument(
        ..., help="Specify the directory containing hypothesis files."
    ),
    level: int = typer.Option(
        3, "--level", "-l",
        help=(
            "Choose audio quality level (1, 2, or 3) and below; "
            "for example, level 3 will include also levels 1 and 2. "
            "The level value must match the level used during transcription."
        )
    ),
    fn_cls: str = typer.Option(
        "1", "--class", "-c",
        help=(
            "Select the functional class for WER calculation. "
            "Class is application specific; if no class is used, use default."
        )
    ),
    seg: str = typer.Option(
        "A", "--segment", "-s",
        help="Select a semantic segment for WER calculation."
    ),
    approach: str = typer.Option(
        "normal", "--approach", "-a",
        help=(
            "Calculation approach for segment-based Levenshtein dist (edit): "
            "normal or fast."
        )
    ),
    tight: bool = typer.Option(
        False, "--no-tight/--tight",
        help=(
            "Include prefix drift (PD) before each segment or not; "
            "default to include; to exclude, use --tight in CLI."
        )
    ),
):
    """Calculate (class-based) segment-level WER.

    Arguments:
    -   ref_dir: str. Directory containing ref files (currently, cns files).
    -   hyp_dir: str. Directory containing hyp files (currently, txt files).
    -   level: int=3. Audio quality level (1, 2, or 3). Cues with stm starting
            with a number greater than the value of level will be dropped.
    -   fn_cls: str="1". The functional class for WER calculation.
    -   seg: str="A". The semantic segment for WER calculation.
    -   approach: str. The approach used for calculating WER. Valid values:
        (1) `normal` (default) and (2) `fast`.
    -   tight: Boolean indicator for including prefix drift (PD, or
        hallucination) before each segment or not:
        -   True: Use tight segmemts---do not include PD (default).
        -   False: Do not use tight segments---do include PD.

    Example:
    -  salwer csw ref b12_aug2_l12 --level 2 --approach fast
    """

    return calculate_seg_wer_(ref_dir, hyp_dir,
                              level, fn_cls, seg,
                              approach, tight)


@app.command("calculate-word-wer")
@app.command("cww")
def calculate_wrd_wer(
    ref_dir: str = typer.Argument(
        ..., help="Specify the directory containing reference files."
    ),
    hyp_dir: str = typer.Argument(
        ..., help="Specify the directory containing hypothesis files."
    ),
    level: int = typer.Option(
        3, "--level", "-l",
        help=(
            "Choose audio quality level (1, 2, or 3) and below; "
            "for example, level 3 will include also levels 1 and 2. "
            "The level value must match the level used during transcription."
        )
    ),
    fn_cls: str = typer.Option(
        "all", "--class", "-c",
        help=(
            "Select the functional class for WER calculation. "
            "Default to 'all'. Use the class number if a class should be "
            "specified."
        )
    ),
    seg: str = typer.Option(
        "all", "--segment", "-s",
        help=(
            "Select semantic segment to filter by. Default to 'all'. "
            "Other options are alphabet of the semantic segments."
        )
    ),
    err_limit: float = typer.Option(
        3.0, "--err-limit",
        help=(
            "Choose limit of error (edit) for each word. Note that this is "
            "the decimal form, meaning 3.0 => max 300% WER for each word."
        )
    ),
):
    """Calculate word-level WER and word dictionary for further processing.

    This command calculate word-level WER between ref and hyp trancripts.
    It also save the word dictionary in a log file in log/word-dict.csv.
    Note that we use only the normal version of the levenshtein_word function.

    Arguments:
    -   ref_dir: str. Directory containing ref files (currently, cns files).
    -   hyp_dir: str. Directory containing hyp files (currently, txt files).
    -   level: int=3. Audio quality level (1, 2, or 3). Cues with stm starting
            with a number greater than the value of level will be dropped.
    -   fn_cls: str="all". The functional class for WER calculation.
    -   seg: str="all". The semantic segment for WER calculation.
    -   err_limit: float = 3.0. The limit of error (edit) for each word.
        Note that 3.0 => max 300% WER for each word.

    Example:
    -  salwer cww ref b12_aug2_l12 --level 2
    """

    return calculate_wrd_wer_(ref_dir, hyp_dir, level, fn_cls, seg, err_limit)


@app.command("calculate-word-wer2")
@app.command("cww2")
def calculate_wrd_wer(
    ref_dir: str = typer.Argument(
        ..., help="Specify the directory containing reference files."
    ),
    hyp_dir: str = typer.Argument(
        ..., help="Specify the directory containing hypothesis files."
    ),
    level: int = typer.Option(
        3, "--level", "-l",
        help=(
            "Choose audio quality level (1, 2, or 3) and below; "
            "for example, level 3 will include also levels 1 and 2. "
            "The level value must match the level used during transcription."
        )
    ),
    fn_cls: str = typer.Option(
        "all", "--class", "-c",
        help=(
            "Select the functional class for WER calculation. "
            "Default to 'all'. Use the class number if a class should be "
            "specified."
        )
    ),
    seg: str = typer.Option(
        "all", "--segment", "-s",
        help=(
            "Select semantic segment to filter by. Default to 'all'. "
            "Other options are alphabet of the semantic segments."
        )
    ),
    err_limit: int = typer.Option(
        3, "--err-limit",
        help=(
            "Choose limit of error (edit) for each word. Note that this is "
            "doubled result, meaning 3 => max 150% WER for each word."
        )
    ),
):
    """Calculate word-level WER and word dictionary with Approach 2.

    This command calculate word-level WER between ref and hyp trancripts.
    It also save the word dictionary in a log file in log/word-dict.csv.
    Note that we use only the normal version of the levenshtein_word function.

    Arguments:
    -   ref_dir: str. Directory containing ref files (currently, cns files).
    -   hyp_dir: str. Directory containing hyp files (currently, txt files).
    -   level: int=3. Audio quality level (1, 2, or 3). Cues with stm starting
            with a number greater than the value of level will be dropped.
    -   fn_cls: str="all". The functional class for WER calculation.
    -   seg: str="all". The semantic segment for WER calculation.
    -   err_limit: int = 5. The limit of error (edit) for each word. Note that
        this is doubled result, meaning 5 => max 250% WER for each word.

    Example:
    -  salwer cww2 ref b12_aug2_l12 --level 2
    """

    return calculate_wrd_wer2_(ref_dir, hyp_dir, level, fn_cls, seg, err_limit)


@app.command("class-n-seg-cues")
@app.command("csc")
def class_n_seg_cues(
    src: str = typer.Argument(..., help="Path to source file or directory"),
    dst: str = typer.Argument(None, help="Path to output file (ignored in --dir mode)"),
    dir_mode: bool = typer.Option(
        False, "--dir", help="Process directories instead of single files"
    ),
):
    """Create class and segmentation fields for cues.

    Arguments:
    -  src: str. Path to source file or directory
    -  dst: str. Path to output file (for single file mode)
    -  dir_mode: bool=False. Use "--dir" for directory mode

    Examples:
    -  single file: salalp csc input.json output.json
    -  directory: salalp csc input_dir output_dir --dir
    """

    return class_n_seg_cues_(src, dst, dir_mode)


@app.command("inspect-class-seg")
@app.command("ics")
def inspect_class_seg(
    folder: str = typer.Argument(
        ..., help="Path to folder containing LLM files"),
    diff: int = typer.Option(
        0, "--diff", help="Show seg and txt differences great than diff."),
):
    """Inspect class and segment of reference transcripts.

    Arguments:
    -  folder: str. Path to folder containing LLM files
    -  diff: bool=False. Use "--diff" to show differences

    Example:
    -  salalp ccs llm_folder
    -  salalp ccs llm_folder --diff
    """

    return inspect_class_seg_(folder, diff)


@app.command("obtain-word-count")
@app.command("owc")
def obtain_word_count(
    txt_dir: str = typer.Argument(
        ..., help="Directory containing the transcript files"
    ),
    level: int = typer.Option(
        3, "--level", "-l",
        help=(
            "Choose audio quality level (1, 2, or 3) and below; "
            "for example, level 3 will include also levels 1 and 2. "
            "The level value must match the level used during training."
        )
    ),
    porder: str = typer.Option(
        "value", "--porder", "-s",
        help="Select the print order: 'value' (default) or 'key'"
    ),
):
    """Obtain word count for training or test datasets.

    This command is used to obtain the word count which is needed for
    word-level WER analysis or language usage analysis.

    Arguments:
    -   txt_dir: str. Dir containing transcript files (currently, cns files).
    -   level: int=3. Audio quality level (1, 2, or 3). Cues with stm starting
            with a number greater than the value of level will be dropped.
    -   porder: str="value". The order to print the word-dict for word count.

    Example:
    -  salwer owc ref --level 3
    -  salwer owc ref --level 3 --porder key
    """

    return obtain_word_count_(txt_dir, level, porder)


@app.command("print-levenshtein-table")
@app.command("plt")
def print_levenshtein_table(
    s: str = typer.Argument(
        help=(
            "The source string of alphabets (usually J to R) such as "
            "'J k   M   O'."
        )
    ),
    t: str = typer.Argument(help="The target string of alphabets"),
):
    """Print Levenshtein table using alphabet.

    Arguments:
    -   s: str. The source string of alphabets.
    -   t: str. The target string of alphabets.

    Example:
    -  salalp plt 'J k   M   O' 'J K L M N O'
       Note that the above sequences are usually planned as follows first:
       s = 'J k   M   O'
       t = 'J K L M N O'
    """

    return print_levenshtein_table_(s, t)
