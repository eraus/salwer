# Readme for SaLWER

## Running examples

### Functionaly classify and semantically segment each cue

There are two versions. One is the file version, and the other is directory version.

The original transcript files should be in a JSON format. Later we will support VTT format.

The output will be in the cns (Classification and Segmentation) format.

This is done using the following `salwer csc atc0json atc0cns --dir`.


### Check the classification and segmentation results of LLM

This is done by running `salwer ccs atc0cns`.

These cues that have different total number of words and total WER words will be printed so that we can pay close attention to the result. Note that this does not guanrentee the correctness of the result. It just provide another layer of checking.

### Calculate the segmented WER

