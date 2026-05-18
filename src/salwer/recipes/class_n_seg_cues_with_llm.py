import json
import os
from pathlib import Path
import re
import shutil

import typer
from openai import OpenAI

from salwer.utils import read_file_to_text
from salwer.labels import Transcripts

"""Recipe to functionally classify and semantically segment cues via LLM.

Note:
  - The input file should be JSON with the format for each cue defined in
    class Cue.
  - The output file should be cns:
    - Functionally classified and semantically segmented
    - There will be a new cns field for each cue
"""

# The following are only for reference purposes:
# # Mapping from class number to class string
# CLASS_MAPPING = {
#     "1": "ATC-IA",
#     "2": "PLT-RA",
#     "3": "ATC-OT",
#     "4": "PLT-OT",
# }

# # Mapping from letter to seg key
# SEG_LETTER_MAPPING = {
#     "A": "clsn",   # callsign
#     "B": "actn",   # action
#     "C": "valu",   # value
#     "D": "ackg",   # acknowledge
#     "E": "info",   # information
#     "F": "cond",   # condition
#     "G": "facl",   # facility
#     "H": "navi",   # navaid/navigation
#     "I": "grnt",   # greeting
#     "J": "othr",   # other
# }

# # Mapping from number suffix to type
# TYPE_SUFFIX_MAPPING = {
#     "1": "altm",   # altimeter
#     "2": "altd",   # altitude
#     "3": "freq",   # frequency
#     "4": "hdng",   # heading
#     "5": "sped",   # speed
#     "6": "sqwk",   # squawk
# }


def class_n_seg_cues_(src: str, dst: str, dir_mode: bool):
    """Functionally classify and semantically segment cues using LLM."""

    if dir_mode:    # dir processing
        src_dir = Path(src)
        dst_dir = Path(dst)
        shutil.rmtree(dst_dir, ignore_errors=True)
        dst_dir.mkdir(parents=True, exist_ok=True)

        for file in src_dir.glob("*.json"):
            if file.is_file():
                src_file = str(file)
                dst_file = str((dst_dir / file.name).with_suffix(".cns"))
                _class_n_seg_cues_of_a_file(src_file, dst_file)
        typer.echo(f"Processed files saved to {dst_dir}")
    else:           # single file processing
        _class_n_seg_cues_of_a_file(src, dst)


def _class_n_seg_cues_of_a_file(src_file: str, dst_file: str):
    """Revise casing and punctuation in a single JSON file using LLM."""
    typer.echo(f"Processing file {src_file}")
    text = read_file_to_text(src_file)
    ann = Transcripts.from_json_text(text)
    # ann.filename = src_file  # Set filename for the function
    _cls_n_seg_each_cue_in_ann_with_llm(ann)
    output_text = ann.to_cns_text()

    with open(dst_file, "w", encoding="utf-8") as f:
        f.write(output_text)
    typer.echo(f"Conversion saved to {dst_file}")


def _cls_n_seg_each_cue_in_ann_with_llm(ann):
    """
    Process each cue of an annotation w/ LLM for classification & segmentation.
    """
    HISTORY_DEPTH = 3   # The depth of the history for each aircraft
    # Extract ATC station, e.g., from "b_asr_text_cmc\dca_lc_4.txt" get "lc"
    filename = ann.filename
    parts = filename.split('_')
    if len(parts) > 2:
        atc = parts[-2].upper()
    else:
        raise ValueError("Cannot find ATC in the filename.")

    all_hst = {} # A dict for all histories

    for cue in ann.cues:
        stm = cue.stm       # e.g., "1>DAL1103>LC-3"
        parts = stm.split('>')
        spkr = parts[1]     # The speaker of the comm
        lsnr = parts[2]     # The listener of the comm
        if atc in spkr:
            spkr = "ATC"
            aircraft = lsnr
        else:
            lsnr = "ATC"
            aircraft = spkr
        # There are cases that neither is ATC, but we don't really care.

        if aircraft == "NO":    # This is for comment cues only
            continue

        com = f"{spkr} to {lsnr}"

        hst = ' '.join(all_hst[aircraft]) if aircraft in all_hst \
            else f"No history for {aircraft}"

        txt = cue.txt
        llm_return = _class_n_seg_a_cue(hst=hst, com_direction=com, txt=txt)

        # Strip non-ASCII characters
        original = llm_return
        llm_return = re.sub(r'[^\x00-\x7F]+', '', llm_return)
        if original != llm_return:
            print(f"Non-ASCII characters removed: {original} -> {llm_return}")

        # Update history
        if aircraft != "UNK":
            if aircraft not in all_hst:
                all_hst[aircraft] = []
            if len(all_hst[aircraft]) >= HISTORY_DEPTH:
                all_hst[aircraft] = all_hst[aircraft][1:]
            all_hst[aircraft].append(f"From {com}: {txt}")

        cue.cns = llm_return
        print(f"{cue.cns = }")


def _class_n_seg_a_cue(hst: str, com_direction: str, txt: str) -> str:
    """
    Classify and segment the transcript using LLM.

    Args:
        hst: The past communication directions and transcripts.
        com_direction: The communication direction (from x to y).
        txt: The transcript text.

    Returns:
        Revised transcript with proper casing and punctuation.
    """
    client = OpenAI(
        api_key=os.getenv("OPENROUTER_API_KEY"),
        base_url="https://openrouter.ai/api/v1",
    )

    prompt = f"""
You are an expert in ATC (Air Traffic Control) communications. You have two tasks. The first one is to classify the given transcript into one of the following classes according to the descriptions following the classes:

1. "ATC-IA". ATC instructions for pilot to perform immediate avionics operations (e.g., changing heading or altitude).
2. "PLT-RA". Pilot readback that corresponds to ATC-IA messages.
3. "ATC-OT". Other ATC transmissions, including future-phase instructions (such as keep speed to a certain waypoint), acknowledgments, and routine exchanges. There is no pressure to extract future-phase instructions as pilots will have enough time for these actions.
4. "PLT-OT". Other pilot transmissions, including readbacks for non-avionics instructions, requests, and routine exchanges.

Your second task is to segment the transcripts into different parts:

A. callsign. Aircraft identifier present in all above classes.
B. action. Verb indicating the avionics operation (e.g., "climb," "descend," "turn") in ATC-IA or PLT-RA. For action , we need to attach the type. For example, we have (1) altimeter, (2) altitude, (3) frequency, (4) heading, (5) speed, and (6) squawk.
C. value. Numeric parameters (e.g., altitude, heading, frequency) in ATC-IA or PLT-RA. For value, we need to attach the type as well. For example, we have (1) altimeter, (2) altitude, (3) frequency, (4) heading, (5) speed, and (6) squawk.
D. acknowledge. Short confirmations like "roger," "wilco," "affirm", "will do", and "radar contact" in all above classes.
E. info. Expressions used for providing info only, such as "going from 4 to 5" if not in readback. (If in readback, it will be action and value.)
F. condition. Condition phrases indicating when an action should occur (e.g., "after passing," "when able") in ATC-IA or PLT-RA.
G. facility. Identifiers for various facilities that do not have their unique name (except city names). These include ATC position, runway, ILS, and DME.
H. navaid. Named geographic points for navigation aids (e.g., "JFK VOR," "ALBANY") used in all above classes.
I. greeting. Salutations such as "good morning", "good day", "hello", and "good bye" in all above classes.
J. other. Everything that cannot be classified into the above segments.

Below are pairs of transcripts and returns, where the return has class and segmentation implemented:

P1:
Transcript: "Northwest Five Seventy Nine, Departure, radar contact."
Return: "(1) [(A) Northwest Five Seventy Nine] [(G) Departure] [(D) radar contact]"

P2:
Transcript: "Delta Nine Fifty Nine, contact Dulles Departure on one three four point two."
Return: "(1) [(A) Delta Nine Fifty Nine] [(B3) contact] [(G) Dulles Departure] [(C3) one three four point two]"

P3:
Transcript: "Thirty four two, Delta Nine Fifty Nine, good day sir."
Return: "(2) [(C3) Thirty four two] [(A) Delta Nine Fifty Nine] [(I) good day sir]"

P4:
Transcript: "Pat Zero Six Zero, turn right heading three six zero."
Return: "(1) [(A) Pat Zero Six Zero] [(B4) turn right heading] [(C4) three six zero]"

P5:
Transcript: "Right three six zero, Zero Six Zero."
Return: "(2) [(B4) Right] [(C4) three six zero] [(A) Zero Six Zero]"

P6:
Transcript: "Departure, Challenger One Oh One Sierra Kilo, out of twelve hundred for five thousand, up the river."
Return: "(4) [(G) Departure] [(A) Challenger One Oh One Sierra Kilo] [(E) out of twelve hundred for five thousand, up the river]"

P7:
Transcript: "Challenger One Oh One Sierra Kilo, Washington Departure, radar contact."
Return: "(2) [(A) Challenger One Oh One Sierra Kilo] [(G) Washington Departure] [(E) radar contact]"

The conversation history is: "{hst}"
The current communication is from "{com_direction}"
The transcript is: "{txt}"

Return only the class and segments, nothing else.
"""

    response = client.chat.completions.create(
        # model="openai/gpt-5.2",
        model="openai/gpt-5.4-mini",
        # model="qwen/qwen3.6-plus:free",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=2000,
        temperature=0.02,
    )

    revised_txt = response.choices[0].message.content.strip()
    return revised_txt
