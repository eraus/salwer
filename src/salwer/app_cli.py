from pathlib import Path
import os
import typer
from typing import List

from .recipes.calculate_seg_wer import calculate_seg_wer_
from .recipes.check_class_seg import check_class_seg_


__version__ = "0.1.0"
app = typer.Typer()


########################################################################
# Version command
@app.command()
def version():
    """Print the version."""
    typer.echo(f"Version of salalp: {__version__}")


@app.command("check-class-seg")
@app.command("ccs")
def check_class_seg(
    folder: str = typer.Argument(
        ..., help="Path to folder containing LLM files"),
    diff: int = typer.Option(
        0, "--diff", help="Show seg and txt differences great than diff."),
):
    """Check class and segment of reference transcripts.

    Arguments:
    -  folder: str. Path to folder containing LLM files
    -  diff: bool=False. Use "--diff" to show differences

    Example:
    -  salalp ccs llm_folder
    -  salalp ccs llm_folder --diff
    """

    return check_class_seg_(folder, diff)


@app.command("calculate-seg-wer")
@app.command("csw")
def calculate_seg_wer(
    hyp_folder: str = typer.Argument(
        ..., help="Path to folder containing hypothesis JSON files"
    ),
    ref_folder: str = typer.Argument(
        ..., help="Path to folder containing reference LLM files"
    ),
    class_sel: str = typer.Option("1", "--class",
                                  help="Select class to filter by"),
    seg_sel: str = typer.Option("A", "--segment",
                                help="Select segment to filter by"),
    level: int = typer.Option(3, "--level", "-l"),
):
    """Calculate class/segment WER between hypothesis & reference transcripts.

    This command compares hypothesis transcripts (from JSON files) with ref
    transcripts and classes/segments (from LLM files) to calculate WER metrics.

    Arguments:
    -  hyp_folder: str. Path to folder containing hypo transcript JSON files
    -  ref_folder: str. Path to folder containing ref LLM files
    -  class_sel: str="1". Use "--class" to select a class for filtering
    -  seg_sel: str="A". Use "--segment" to select a segment for filtering
    -  level: int=3. Audio quality level (1, 2, or 3). Cues with stm starting
              with a number greater than level will be dropped.

    Example:
    -  salalp csw hyp_json_folder ref_llm_folder
    -  salalp csw hyp_json_folder ref_llm_folder --class "2"
    -  salalp csw hyp_json_folder ref_llm_folder --segment "B" --level 1
    """

    return calculate_seg_wer_(hyp_folder, ref_folder, class_sel, seg_sel, level)

