## Import from Python standard library
from dataclasses import dataclass, field
from json import loads as json_load
from json import dumps as json_dump

## This file can be used alone. It can read and write JSON files.

############################################################################
# The Cue class defines basic data structure of each cue in an annotation.
# A cue contains the labels of a segment (or interval) of speech.
@dataclass
class Cue:

    # Class Attributes
    bgn_time: int = 0   # In units of milliseconds
    end_time: int = 0
    stm: str = ""       # STM (Segment Time Marking) speaker string
    cmt: str = ""       # Comment string
    txt: str = ""       # Main transcript string in verbatim format
    cls: str = ""       # The class of the cue. Definitions is task specific.
                        # Example: "ATC-IA", "ATC-OT", "PLT-RA", & "PLT-OT".
    seg: dict = field(default_factory=dict)  # Dict of segmentations. Definition is task specific.
                        # Example of keys: "clsn" (callsign)
    log: str = ""       # Transcript in orthographical format for logging
    nlp: str = ""       # NLP task related string in jsonl format to contain
                        # different fields for different tasks
    avn: str = ""       # Avionics operation related info

    @property
    def length(self):
        return self.end_time - self.bgn_time

    # for printing cues
    def __str__(self):
        return "bgn: " + str(self.bgn_time) + "\nend: " + \
            str(self.end_time) + "\ntxt: " + self.txt

    ########################################################################
    # Normal class methods

    # moves entire cue start and end based on 'time_offset'
    def offset_time(self, time_offset_in_ms: int):
        self.bgn_time += time_offset_in_ms
        self.end_time += time_offset_in_ms


############################################################################
# The Transcripts class defines a collection of cues for a single file.
# This is a simplified version intended for use in other applications.
class Transcripts:

    # Class Attributes
    cues: list[Cue] = field(default_factory=list)
    has_silence: bool | None = None
    filename: str = ""

    # Constructor
    def __init__(self, cues: list[Cue] = None,
                 has_silence: bool | None = None,
                 filename: str = ""):
        if cues is not None:
            self.cues = cues
            self.has_silence = has_silence
            self.filename = filename

    # List of cues is sorted and the max time is at the end of cues
    @property
    def max_time(self):
        if len(self.cues) > 0:
            return self.cues[-1].end_time
        else:
            return 0

    ########################################################################
    # Basic class methods:
    #   add_silence
    #   remove_silence
    #   offset_time
    #   from_json_text

    # -----------------------------------------------------------------------
    # Add and remove silence

    def add_silence(self, silence: str = "[Silence]"):
        """Add cues with specified (silence) string in empty intervals.

        Assume no cues overlap; will error when overlap exists."""
        # Check if silence is needed in the beginning
        if self.cues[0].bgn_time != 0:
            self.cues.insert(0, Cue(bgn_time=0,
                                    end_time=self.cues[0].bgn_time,
                                    txt=silence))

        i = 1  # Index to insert a silence cue if needed
        # Check between each cue to see if end time and start time match up
        while i < len(self.cues):
            prev_end_time = self.cues[i - 1].end_time
            next_bgn_time = self.cues[i].bgn_time
            if prev_end_time < next_bgn_time:
                # If they don't match, add silence cue
                self.cues.insert(i, Cue(bgn_time=prev_end_time,
                                        end_time=next_bgn_time,
                                        txt=silence))
                i += 1
            elif prev_end_time > next_bgn_time:
                raise ValueError(
                    "Overlap between intervals exists. Perform "
                    "'remove_overlap' to resolve automatically or "
                    "'check_overlap' to check results and resolve manually "
                    "in the original file.")
            i += 1
        self.has_silence = True

    def remove_silence(self):
        """Remove all cues with silence: "[Silence]" or empty string "".

        By default, we only work for the basic layer.
        This function needs fixing to work with multi-tier text;
        currently it just guesses based on the first tier - works for now."""
        self.cues = [cue for cue in self.cues
                     if cue.txt.lower() not in ("[silence]", "")]
        self.has_silence = False

    # -----------------------------------------------------------------------
    # Time-related class methods

    # offsets time of entire Transcript by offsetting time of each cue
    def offset_time(self, time_offset_in_ms: int):
        for cue in self.cues:
            cue.offset_time(time_offset_in_ms)


    # -----------------------------------------------------------------------
    # File IO methods - delegated to I/O modules
    def to_json_text(self):
        return _to_json_text(self)

    @classmethod
    def from_json_text(cls, file_text: str, filename: str = ""):
        return _from_json_text(cls, file_text, filename)

    @classmethod
    def from_edtd_text(cls, file_text: str, filename: str = ""):
        return _from_edtd_text(cls, file_text, filename)

    @classmethod
    def from_txt_llm_text(cls, file_text: str, level: int = 3):
        return _from_txt_llm_text(cls, file_text, level)

    @classmethod
    def from_asr_pred_text(cls, file_text: str, filename: str = ""):
        return _from_asr_pred_text(cls, file_text, filename)

########################################################################
# File IO for JSON

def _to_json_text(self, include_attrs=None):
    self.remove_silence()

    # Define which attributes to include
    attrs = include_attrs or ["bgn_time", "end_time", "stm", "cmt", "txt"]

    cues_data = []
    for cue in self.cues:
        cue_dict = {attr: getattr(cue, attr)
                    for attr in attrs if hasattr(cue, attr)}
        cues_data.append(cue_dict)

    json_obj = {
        "cues": cues_data,
        "has_silence": self.has_silence,
        "filename": self.filename
    }
    return json_dump(json_obj, indent=2)


def _from_json_text(cls, file_text: str, filename: str = ""):
    if file_text:
        json_obj = json_load(file_text)
        cues = []
        for cue in json_obj["cues"]:
            cues.append(Cue(bgn_time=cue.get("bgn_time", 0),
                            end_time=cue.get("end_time", 0),
                            stm=cue.get("stm", ""),
                            cmt=cue.get("cmt", ""),
                            txt=cue.get("txt", "")))

        annotation = cls(cues=cues, has_silence=json_obj["has_silence"])
        annotation.filename = json_obj["filename"]
        return annotation
    else:
        return cls(cues=[], has_silence=False)

# File IO for other format

# See the above commented code for the format of this edtd file:
# LLM to txt
def _from_edtd_text(cls, file_text: str, filename: str = ""):
    text_list = file_text.splitlines()
    # Remove blank lines
    text_list = [tx for tx in text_list if len(tx.strip()) > 0]
    cues = []
    index = 0
    len_text_list = len(text_list)

    while index < len_text_list:
        stm = text_list[index][5:]
        index += 1
        bgn_time = int(text_list[index][5:])
        index += 2
        LLM = text_list[index][5:]
        index += 1

        cue = Cue(bgn_time=bgn_time, end_time=bgn_time, stm=stm, txt=LLM)
        cues.append(cue)

    return cls(cues=cues, has_silence=False)


# See the above commented code for the format of this edtd file:
# LLM to cmt; txt to txt
def _from_txt_llm_text(cls, file_text: str, level: int = 3):
    text_list = file_text.splitlines()
    # Remove blank lines
    text_list = [tx for tx in text_list if len(tx.strip()) > 0]
    cues = []
    index = 0
    len_text_list = len(text_list)

    while index < len_text_list:
        stm = text_list[index][5:].strip()
        if int(stm[0]) > level:
            index += 4
            continue
        index += 1
        bgn_time = int(text_list[index][5:])
        index += 1
        txt = text_list[index][5:].strip()
        index += 1
        LLM = text_list[index][5:].strip()
        index += 1

        cue = Cue(bgn_time=bgn_time, end_time=bgn_time,
                  stm=stm, cmt=LLM, txt=txt)
        cues.append(cue)

    return cls(cues=cues, has_silence=False)


# From the ASR Prediction Text
def _from_asr_pred_text(cls, file_text: str, filename: str = ""):
    text_list = file_text.splitlines()
    # Remove blank lines
    text_list = [tx for tx in text_list if len(tx.strip()) > 0]
    cues = []
    index = 0
    len_text_list = len(text_list)

    while index < len_text_list:
        stm = text_list[index][5:]
        index += 1
        times_sec_str = text_list[index][5:]
        times_ms_int = (round(float(x) * 1000) for x in times_sec_str.split())
        bgn_time, end_time = times_ms_int
        index += 1
        txt = text_list[index][5:]
        index += 1

        cue = Cue(bgn_time=bgn_time, end_time=end_time, stm=stm, txt=txt)
        cues.append(cue)

    return cls(cues=cues, has_silence=False)
