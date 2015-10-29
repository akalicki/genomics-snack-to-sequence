#!/usr/bin/env python
"""
Usage: (python) group3_report1_question9.py

Takes input timing file as processed by "poretools times" from stdin and plots
the pace of strand sequencing (sequence length per duration in pore) for the
given reads. Requires matplotlib.

Suggested usage:
poretools times fast5_directory/ | python group3_report1_question9.py
"""
import math
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import sys

def get_timing(f):
    """Creates lists of pore durations and sequence lengths from timing file"""
    sequence_lengths = []
    pore_durations = []
    for line in f:
        data = line.split("\t")
        sequence_lengths.append(int(data[2]))
        pore_durations.append(int(data[5]))
    return pore_durations, sequence_lengths

if __name__ == '__main__':
    with sys.stdin as f:
        f.readline()  # read past header line
        pore_durations, sequence_lengths = get_timing(f)
        linear_fit = np.polyfit(pore_durations, sequence_lengths, deg=1)

        # plot sequence data and attempt to find a linear fit
        fig, ax = plt.subplots()
        x = np.random.random_integers(-10, 100, 50)
        ax.plot(x, linear_fit[0] * x + linear_fit[1], color='red')
        ax.scatter(pore_durations, sequence_lengths, alpha=0.4)

        # create plot labels
        scatter_patch = mpatches.Patch(color='blue', label='Sequence Data')
        fit_patch = mpatches.Patch(color='red', label='Linear Fit')

        # plot data and linear fit
        plt.axis([0, 100, 0, 5000])
        plt.title('Pace of Strand Sequencing')
        plt.xlabel('Duration in Pore (s)')
        plt.ylabel('Sequence Length (bp)')
        plt.legend(
            [scatter_patch, fit_patch],
            ['Sequence Data', 'Linear Fit: y = %.1fx + %.1f'
                % (linear_fit[0], linear_fit[1])]
        )
        plt.show()
