# Readme of the files_for_wer folder

## Normalization of the transcripts:

-   Remove any non-ASCII leters.
    -   Via the `replace_curly_apostrophes(text)` function.
-   Connect separate terms.
    -   "U S Air" -> "USAir"; "U S" -> "US"; "T W A" ==> "TWA"; "I L S" ==> "ILS"; "D M E" ==> "DME"; "V F R" ==> "VFR"; "I M C" ==> "IMC"; "D C" ==> "DC". To search in VS Code, use "\b\w\s\w\b" with Regex.
    -   Via the `map_fixed_expressions(text, tables.preprocess_eval_fixed_map_tbl)` function.
-   Map common ATC words.
    -   "niner" -> "nine".
-   Expand irregular_contractions.
    -   "Let's" -> "Let us"; "won't" -> "will not".
    -   Via the `expand_irregular_contractions(text, tables.preprocess_contraction_map_tbl)` function.
-   Expand contractioni suffixes.
    -   "xxn't" -> "xx not"; "xx'll" -> "xx will"; "xx've" -> "xx have"; "xx're" -> "xx are"
    -   Via the `expand_contraction_suffixes(text)` function.
-   Resolve Apostrophe s. A simple replacement like
    -   "xx's" -> "xx is".
    -   Note that there may be errors, such as "USAir's" -> "USAir" or "it's got" -> "it has got". These cases are manually corrected here although we can create a simple parser for this purpose. This parser is not included since it is in the domain of NLP.
    -   Via the `resolve_apostrophe_s(text, tables.callsign_owners)` function.
-   Remove anything in angle brackets.
    -   `<pause>` and similar.
    -   Via the `remove_non_speech_markers(text)` function.
-   Remove false starts.
    -   They are expressed as "*".
    -   Via the `remove_false_starts(text)` function.
-   Remove filler words.
    -   "er " -> "", " er," -> "", " er." -> ".", "Er, " -> "",  and the like.
    -   Via the `remove_fillers(text, tables.preprocess_eval_filler_map_tbl)` function.
-   Standardize terms with "and"
    -   "climb and maintain" -> "climb maintain".
    -   "descend and maintain" -> "descend maintain".
    -   "descent and maintain" -> "descend maintain".
-   Skip the change of "'d".