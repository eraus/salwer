## Import from Python standard library
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

########################################################################
# File operation functions

def read_file_to_text(filename: str):
    with (open(filename, 'r') as file):
        file_text = file.read()
        file_text += " "  # textGrid parsing needs an extra whitespace
        file.close()
    return file_text


def write_text_to_file(filename: str, file_text: str):
    with open(filename, 'w') as file:
        file.write(file_text)


########################################################################
# String operation functions

def combine_numbers(match_str: str) -> str:
    """Combine discrete numbers like '2 5 0' into '250'."""
    return re.sub(r'\s+', '', match_str)


def search_astr_in_str_list(astr: str, text_list: list[str], index: int):
    len_text_list = len(text_list)
    if index >= len_text_list -1:
        return (None, index)
    while astr not in text_list[index]:
        index += 1
        if index >= len_text_list:
            return (None, index)
    return (text_list[index], index)


def search_either_str_in_str_list(
        str_a: str, str_b: str, text_list: list[str], index: int):
    len_text_list = len(text_list)
    if index >= len_text_list:
        return (None, index)
    while str_a not in text_list[index] and str_b not in text_list[index]:
        index += 1
        if index >= len_text_list:
            return (None, index)
    return (text_list[index], index)


########################################################################
# Time format conversation functions

# Convert ts (time string) to ms (milliseconds):
#     from 00:05.160 to 5160 (robust)
# Works for both VTT and SRT formats
def _ts_to_ms(ts: str):
    ts = ts.replace(",", ".")
    hour_min_sec, milliseconds = ts.split(".")
    if len(hour_min_sec) == 5:
        hour_min_sec = f'00:{hour_min_sec}'
    time = datetime.strptime(hour_min_sec, "%H:%M:%S")
    time_in_sec = time.hour * 3600 + time.minute * 60 + time.second
    time_in_ms = time_in_sec * 1000 + int(f'{milliseconds:0<3}')
    return time_in_ms

# Convert milliseconds to time string:
#     from 5160 to 00:05.160
# ',' delimiter must be specified for SRT format
def _ms_to_ts(milliseconds: int, delimiter: str = ".", hour: bool = True):
    time = datetime.fromtimestamp(milliseconds / 1000, tz=timezone.utc)
    if hour:
        time_text = f'{time:%H:%M:%S}'
    else:
        time_text = f'{time:%M:%S}'
    ms_only = milliseconds % 1000
    time_text += f'{delimiter}{ms_only:03}'
    return time_text

# Convert cue time from ms to string, used for output in SRT/VTT:
def _cue_time_to_text_str(cue, head_tail_coefs):
    head_time = head_tail_coefs[0] # fixed head time
    head_coef = head_tail_coefs[1] # fixed head time coefficient
    tail_time = head_tail_coefs[2] # fixed tail time
    tail_coef = head_tail_coefs[3] # fixed tail time coefficient
    bgn_time = cue.bgn_time
    end_time = cue.end_time
    duration = end_time - bgn_time
    bgn_time = int(bgn_time - head_time - head_coef * duration)
    if bgn_time < 0:
        bgn_time = 0
    end_time = int(end_time + tail_time + tail_coef * duration)
    time_text = _ms_to_ts(bgn_time, delimiter=",", hour=True)
    time_text += ' --> '
    time_text += _ms_to_ts(end_time, delimiter=",", hour=True)
    return time_text



def _clean_transcript(transcript: str) -> str:
    # 1) convert to lower
    transcript = transcript.lower()
    # 2) remove punctuations
    transcript = re.sub(r"[^\w\s]", "", transcript)
    # 3) Remove "er", the filler word
    words = transcript.split()
    words = [w for w in words if w != "er"]
    transcript = " ".join(words)
    return transcript


# Extract the index of the words in different segments in txt using the
# segmentation in seg and the specific segment in seg_sel.
# Note that the output is a list of lists. The component list has the
# starting index and ending index (+1) of the selected segment in the list
# formed by txt. See the test functions in test_wer.py for illustrations.
def _cue_seg_ranges(txt: str, seg: str, seg_sel: Optional[str]):
    if seg_sel is None:
        return []
    txt_lst = txt.split()
    # Clean txt_lst for matching (remove punctuation and convert to lowercase)
    txt_lst_clean = [re.sub(r"[^\w]", "", w).lower() for w in txt_lst]
    ranges = []
    current_pos = 0

    # Find all top-level segments for seg_sel
    pattern = r"\[\(\s*" + re.escape(seg_sel) + r"\d*\s*\)"
    for match in re.finditer(pattern, seg):
        start = match.end()  # after the (seg_sel)
        # Find the matching ] by counting brackets
        count = 1  # the [ is open
        j = start
        while j < len(seg) and count > 0:
            if seg[j] == "[":
                count += 1
            elif seg[j] == "]":
                count -= 1
            j += 1
        if count == 0:
            end = j - 1  # the ]
            segment_text = seg[start:end]
            # Find nested segments in segment_text
            nested_ranges = []
            k = 0
            while k < len(segment_text):
                if segment_text[k : k + 2] == "[(":
                    cnt = 1
                    m = k + 2
                    while m < len(segment_text) and cnt > 0:
                        if segment_text[m] == "[":
                            cnt += 1
                        elif segment_text[m] == "]":
                            cnt -= 1
                        m += 1
                    nested_ranges.append((k, m - 1))
                    k = m
                else:
                    k += 1
            # Split into parts
            parts = []
            prev_end = 0
            for nr in nested_ranges:
                parts.append(segment_text[prev_end : nr[0]].strip())
                prev_end = nr[1] + 1
            parts.append(segment_text[prev_end:].strip())
            ranges, current_pos = _find_indexes(
                ranges, parts, txt_lst_clean, current_pos
            )
    return ranges

# Extract the class of the transmission: 1 to 4 in string.
def _cue_class(cmt: str) -> str:
    return cmt[1]


def _find_indexes(ranges, parts, txt_lst, current_pos):
    for part in parts:
        if not part:
            continue
        part_words = [re.sub(r"[^\w]", "", w).lower() for w in part.split()]
        if not part_words:
            continue
        for idx in range(current_pos, len(txt_lst) - len(part_words) + 1):
            if txt_lst[idx : idx + len(part_words)] == part_words:
                ranges.append([idx, idx + len(part_words)])
                current_pos = idx + len(part_words)
                break
    return ranges, current_pos
