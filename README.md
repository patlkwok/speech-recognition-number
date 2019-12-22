## Improving Performances of Speech Recognizers on Numbers
#### Final Project for COMS E6998-7 (Fall 2019) by Patrick Kwok (lk2754@columbia.edu)
GitHub repository for this project: https://github.com/patlkwok/speech-recognition-number

December 21, 2019

### Introduction
This repository contains the Python code for a "toolbox" useful for speech recognition and speech synthesis purposes. This "toolbox" contains functions for generating all possible methods for saying, or spelling out, numbers within a given sentence, as well as the corresponding probabilities for each of the possible methods.

In the future, given these possible methods and corresponding probabilities, alignments with the audio can be performed, and the most probable spelt-out form for each number given both the sentence and the audio can be determined. Eventually, the Arabic numerals in the training transcript can be replaced with the most likely spelt-out forms, and this will have an effect of improving the performances of speech recognizers on numbers.

### Contents
1. `get_number_type.py` contains the Python code for getting types of numerals given context, or input sentences. Here we define "numeral" as a word (string that does not contain spaces) that contains at least one digit (0, 1, 2, ..., 9), which includes both "simple numerals" consisting exclusively of digits (e.g. "365", "1999") and "mixed numerals" consisting of both digits and non-digit characters (e.g. "B737", "-5.25", "100%"). The possible types of numerals include year number ("y", also covering house numbers, highway numbers and room numbers that are read similarly as year numbers), serial number ("s", e.g. phone numbers), time of day ("t", e.g. "3:45"), ordinal number ("o", e.g. "32nd") and (regular) cardinal number ("c", e.g. "365", "-5.25"). In particular, the `get_type` function returns the possible types of a numeral as well as their probabilities given the numeral itself and its surrounding context.

2. `read_numbers.py` contains the Python code for "reading", or generating the possible spelt-out forms, of a numeral given its type or possible types (with probabilities). In particular, the `read_num_type` function returns the possible spelt-out forms of a numeral, as well as their probabilities, given the (fixed) type of this numeral. Similarly, the `read_num` function returns the possible spelt-out forms of a numeral, as well as their probabilities, given the possible types (with probabilities) of this numeral.

3. `run.py` contains the Python code for running the tests. The `read_num_sentence` function returns a list of possible spelt-out forms (with probabilities) for each number in the input sentence, and the main function `get_all_possibles` returns a list of possible ways of speaking out the entire sentence (with probabilities) given the input sentence that contains numerals.

4. `test.txt` is a text file that contains sample sentences for testing purposes. Each line in the text file corresponds to a sample sentence.

5. `out.txt` is the output text file that will be created once the test is performed on `test.txt`. This text file consists of "blocks" separated by two empty lines, with each "block" corresponding to a sample sentence in `test.txt`. In each "block", the first line repeats the original sentence containing Arabic numerals, then each line after that is a possible way of speaking (or spelling) out the entire sentence, with its probability. For example, suppose `1200 days ago in mid 2016` is the input sentence, then the output line `0.3 | twelve hundred days ago in mid two thousand sixteen` means that `twelve hundred days ago in mid two thousand sixteen` is one of the possible ways of speaking out the input sentence, and the probability that the input sentence is spoken out in this way is 0.3.

### How to run the code
The code is written in Python 3. When running the code please make sure that the Python version is `3.x`. Assuming the working directory is the same as the directory containing the Python code, the code can be run using the command `python run.py [test_dir] [output_dir]`, for example `python run.py test.txt out.txt`.

There are two arguments: `[test_dir]` is the location (with file name) of the input text file containing test sentences, formatted in the way described above (one line for each sentence), and `[output_dir]` is the location (with file name) where the output text file will be saved. Any text file (not necessarily `test.txt`) can be used for testing purposes as long as the text file is formatted in the correct way (one line for each sentence).

If the working directory is not the same as the directory containing the Python code, or if the test file is not in the same folder as the Python code, then `run.py`, `[test_dir]` and `[output_dir]` must be the complete directory (with file names) of these files.
