#!/usr/bin/env python
"""
Usage: (python) group3_report1_question11.py

Takes input timing file as processed by "poretools times" from stdin and creates
a dictionary mapping filename to duration as well as one mapping filename to
sequence length.

Suggested usage:
poretools times fast5_directory/ | python group3_report1_question11.py
"""
import sys

def build_maps(f):
    file_to_length = {}
    file_to_duration = {}
    for line in f:
        data = line.split('\t')
        filename = data[1]
        read_length = data[2]
        duration = data[5]
        file_to_length[filename] = int(read_length)
        file_to_duration[filename] = int(duration)
    return file_to_length, file_to_duration

if __name__ == '__main__':
    with sys.stdin as f:
        f.readline()  # read past header line
        file_to_length, file_to_duration = build_maps(f)
        print file_to_length
        print file_to_duration
