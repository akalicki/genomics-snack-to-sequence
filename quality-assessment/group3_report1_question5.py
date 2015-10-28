#!/usr/bin/env python
"""Usage: (python) group3_report1_question5.py <FASTQ FILE>

Calculates the average quality score and standard deviation for all 2D
reads found in the input file.
"""

from itertools import izip_longest
import sys
import re
import math


def grouper(iterable, n, fillvalue=None):
    """Collect data into fixed-length chunks or blocks.
    From 'recipes' page of python itertools documentation."""
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx
    args = [iter(iterable)] * n
    return izip_longest(fillvalue=fillvalue, *args)


def ascii_to_quality(c, maxscore):
    return (ord(c) - 32)/97.0 * maxscore


if __name__ == '__main__':
    total = 0
    count = 0
    all_values = []
    with open(sys.argv[1]) as f:
        for r in grouper(f, 4, ""):
            if re.search('twodirections', r[0]):
                qualscores = [ascii_to_quality(c, 30) for c in r[3]]
                all_values.extend(qualscores)
                count += len(qualscores)
                total += math.fsum(qualscores)
    average = total / count
    print "Number of bases: " + str(count)
    print "Average base-calling quality: " + str(average)
    t = math.fsum([math.pow(q - average, 2) for q in all_values])
    sd = math.sqrt(t / (count - 1))
    print "Base-calling standard deviation: " + str(sd)
    ordered = sorted(all_values)
    if count % 2 == 0:
        med = (ordered[(count - 1) / 2] + ordered[(count - 1) / 2 + 1])/2.0
    else:
        med = ordered[(count - 1) / 2]
    print "Median: " + str(med)
