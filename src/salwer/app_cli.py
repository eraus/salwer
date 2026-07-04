from pathlib import Path
import os
import typer
from typing import List

from .recipes.calculate_seg_wer import calculate_seg_wer_
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


@app.command("calculate-seg-wer")
@app.command("csw")
def calculate_seg_wer(
    ref_dir: str = typer.Argument(
        ..., help="Directory containing reference LLM files"
    ),
    hyp_dir: str = typer.Argument(
        ..., help="Directory containing hypothesis JSON files"
    ),
    level: int = typer.Option(3, "--level", "-l"),
    fn_cls: str = typer.Option("1", "--class", "-c",
                            help="Select class to filter by"),
    seg: str = typer.Option("A", "--segment", "-s",
                                help="Select segment to filter by"),
):
    """Calculate class/segment WER between hypothesis & reference transcripts.

    This command compares hypothesis transcripts (from JSON files) with ref
    transcripts and classes/segments (from LLM files) to calculate WER metrics.

    Arguments:
    -  ref_dir: str. Directory containing ref LLM files
    -  hyp_dir: str. Directory containing hypo transcript JSON files
    -  level: int=3. Audio quality level (1, 2, or 3). Cues with stm starting
              with a number greater than level will be dropped.
    -  fn_cls: str="1". Use "--class" to select a class for filtering
    -  seg: str="A". Use "--segment" to select a segment for filtering

    Example:
    -  salalp csw hyp_json_folder ref_llm_folder
    -  salalp csw hyp_json_folder ref_llm_folder --class "2"
    -  salalp csw hyp_json_folder ref_llm_folder --segment "B" --level 1
    """

    return calculate_seg_wer_(ref_dir, hyp_dir, level, fn_cls, seg)


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


@app.command("print-levenshtein-table")
@app.command("plt")
def print_levenshtein_table():
    """Print Levenshtein table using alphabet.

    Arguments:
    -   N/A

    Example:
    -  salalp plt
    """

    return print_levenshtein_table_()