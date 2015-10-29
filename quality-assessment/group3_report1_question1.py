#!/usr/bin/env python
"""
Usage: (python) group3_report1_question1.py <PASS FILE> <FAIL FILE>

Reads a pair of input FASTQ file as processed by poretools and counts
the number of 1D and 2D reads that were found in each, as well as the
number of 2D reads found in both.
"""
import sys
import re


filename_re = re.compile(r"ch(\d+)_file(\d+)_strand_(.*):")


def parse_filename_line(s):
    """Returns a 3-tuple consisting of channel number, file number,
    and boolean flag true if 2D read"""
    matches = filename_re.search(s)
    if matches:
        channel_number = int(matches.group(1))
        file_number = int(matches.group(2))
        twodirections = (matches.group(3) == "twodirections")
        return (channel_number, file_number, twodirections)


def get_reads(f):
    """Creates sets of 1d and 2d reads found in f."""
    reads2d = set([])
    reads1d = set([])
    for line in f.readlines():
        if line[0] == '@':  # skip most irrelevant lines
            z = parse_filename_line(line)
            if z:
                if z[2]:
                    reads2d.add((z[0], z[1]))
                else:
                    reads1d.add((z[0], z[1]))
    return (reads2d, reads1d)

if __name__ == '__main__':
    with open(sys.argv[1]) as passfile, open(sys.argv[2]) as failfile:
        pass2d, pass1d = get_reads(passfile)
        fail2d, fail1d = get_reads(failfile)
        num_1d_pass = len(pass1d)
        num_1d_fail = len(fail1d)
        num_2d_pass = len(pass2d)
        num_2d_fail = len(fail2d)
        print ("Passed: %d 2D reads; %d 1D reads; %.2f%% 2D" % (num_2d_pass,
            num_1d_pass, 100.0 * num_2d_pass / (num_1d_pass+num_2d_pass)))
        print ("Failed: %d 2D reads; %d 1D reads; %.2f%% 2D" % (num_2d_fail,
            num_1d_fail, 100.0 * num_2d_fail / (num_1d_fail+num_2d_fail)))
