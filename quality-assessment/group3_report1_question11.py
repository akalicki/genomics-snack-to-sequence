#!/usr/bin/env python
"""
Usage: (python) group3_report1_question11.py

Takes input timing file as processed by "poretools times" from stdin and creates
a dictionary mapping filename to duration as well as one mapping filename to
sequence length. Then, uses these dictionaries to perform a linear regression
between length and duration on the fastq file given as the first argument.

Suggested usage:
poretools times fast5_directory/ | python group3_report1_question11.py <FASTQ FILE>
"""
import sys
from group3_report1_question5 import grouper
from sklearn import linear_model
import re
import numpy as np

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

file_re = re.compile(r":(.*)$")

if __name__ == '__main__':
    with sys.stdin as f:
        f.readline()  # read past header line
        file_to_length, file_to_duration = build_maps(f)
    with open(sys.argv[1]) as f:
        # look for @ and parse for filename
        x = []
        y = []
        for l in grouper(f, 4):
            if l[0][0] == "@":
                fname = file_re.search(l[0].strip()).group(1)
                x.append(file_to_length[fname])
                y.append(file_to_duration[fname])
        r = linear_model.LinearRegression()
        xx = np.transpose(np.matrix(x))
        yy = np.asarray(y)
        r.fit(xx, yy)
        print r.coef_
        print r.intercept_
        print r.score(xx, yy)
