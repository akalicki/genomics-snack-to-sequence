#!/usr/bin/env python
"""
Usage: (python) group3_report1_question9.py

Takes input timing file as processed by "poretools times" from stdin and plots
the pace of strand sequencing (sequence length per duration in pore) for the
given reads. Requires matplotlib.

Suggested usage:
poretools times fast5_directory/ | python group3_report1_question9.py
"""
import sys
import matplotlib.pyplot as plt

def get_timing(f):
    """Creates lists of sequence lengths pore durations from timing file"""
    sequence_lengths = []
    pore_durations = []
    for line in f:
        data = line.split("\t")
        sequence_lengths.append(int(data[2]))
        pore_durations.append(int(data[5]))
    return sequence_lengths, pore_durations

if __name__ == '__main__':
    with sys.stdin as f:
        f.readline()  # read past header line
        sequence_lengths, pore_durations = get_timing(f)
        plt.plot(pore_durations, sequence_lengths, 'o')
        plt.axis([0, 50, 0, 5000])
        plt.title('Pace of Strand Sequencing')
        plt.xlabel('Duration in Pore (s)')
        plt.ylabel('Sequence Length (bp)')
        plt.show()
