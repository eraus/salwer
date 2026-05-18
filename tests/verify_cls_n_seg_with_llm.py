from salwer.recipes.class_n_seg_cues_with_llm import (
    _class_n_seg_a_cue,
)

def test_class_n_seg_a_cue():
    """
    Test function with a few examples.
    """
    examples = [
        {
            "hst": "DLL209 to ATC: Departure, Delta Two Oh Nine, direction please.",
            "com": "ATC to DLL209",
            "txt": "Delta Two Oh Nine, turn right, ah, heading two seven zero, direct LINDEN when able, and resume your own navigation.",
            "expected": ""
        },
        {
            "hst": "",
            "com": "AAL1895 to ATC",
            "txt": "Departure, American Eighteen Ninety Five is out of eleven hundred for five.",
            "expected": ""
        },
        # Add more examples if needed
    ]

    for ex in examples:
        result = _class_n_seg_a_cue(ex["hst"], ex["com"], ex["txt"])
        print(f"\nTranscript: {ex['txt']}")
        print(f"LLM Result:  {result}")
        # print(f"Expected: {ex['expected']}")
        print("---")
