#!/usr/bin/env python
"""
Usage: (python) group3_report1_question1.py <JSON_FILE_INDEX>

Takes a BlastJSON file index, loops through each file defined to parse tomato
sequence information, build a confusion matrix, and filter insertion/deletion
data.
"""
import sys
import json
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np
import re
import pylab as pl

TOMATO_SCI_1 = "Solanum lycopersicum"
TOMATO_SCI_2 = "Solanum pennellii"
BASES = ['A', 'C', 'G', 'T']

def file_to_seqs(filename):
    """Given BlastOutput json, return a list of all tomato (qseq, hseq) pairs"""
    seqs = []
    with open(filename) as f:
        results = json.loads(f.read())["BlastOutput2"]["report"]["results"]
        hits = results["search"]["hits"]
        for hit in hits:
            sciname = hit["description"][0]["sciname"]
            if sciname != TOMATO_SCI_1 and sciname != TOMATO_SCI_2:
                continue
            for hsp in hit["hsps"]:
                seqs.append((hsp["qseq"], hsp["hseq"]))
    return seqs

def seqs_to_confusion(seq_list):
    """Takes a lit of (qseq, hseq) pairs, and returns a confusion array"""
    confusion = defaultdict(int)
    for pair in seq_list:
        qseq = pair[0]
        hseq = pair[1]
        for i in range(len(qseq)):
            key = (qseq[i].upper(), hseq[i].upper())
            confusion[key] += 1
    return confusion

bases = ['A','C','G','T','-']
def confusion_to_nucleotides(confusion):
    """Takes a confusion array, and prints histogram of nucleotide composition
       for insertions and deletions"""
    insertions = [ confusion[(c, '-')] for c in BASES ]
    deletions = [ confusion[('-', c)] for c in BASES ]
    create_barchart(BASES, insertions, "Nucleotide composition of insertions", 'g')
    create_barchart(BASES, deletions, "Nucleotide composition of deletions", 'r')

def create_barchart(values, counts, title, col):
    """Create a pyplot barchart for given x and y values"""
    ind = np.arange(len(values))
    width = 0.8
    fig, ax = plt.subplots()
    ax.bar(ind, counts, width, color=col)
    ax.set_xlabel("Bases")
    ax.set_ylabel("Count")
    ax.set_title(title)
    ax.set_xticks(ind + width / 2)
    ax.set_xticklabels(values)
    plt.show()

def sizeLength(seq, lengths):
    x = [m.start() for m in re.finditer('-', seq)]
    length = 0
    for i in range(0, len(x)):
        if (i==len(x)-1 or x[i]!=x[i+1]-1):
            length += 1
            if lengths.has_key(length):
                lengths[length] += 1
            else:
                lengths[length] = 1
            length = 0
        else:
            length += 1
    return lengths

def createHistogram(data, title, q, col):
    X = np.arange(len(data))
    pl.bar(X, data.values(), align='center', width=0.5, color=col)
    pl.xticks(X, data.keys())
    ymax = max(data.values()) + 1
    pl.ylim(0, ymax)
    pl.title(title + " (" + q + ")")
    pl.ylabel("Frequency")
    pl.xlabel("Lengths")
    pl.savefig(title + "-" + q)
    pl.clf()

def makeLengthDistribution(sequence):
    insertions = {}
    deletions = {}
    for i in sequence:
        insertions = sizeLength(i[1], insertions) # - in hseq
        deletions = sizeLength(i[0], deletions) # - in qseq
    print "insertion length dictionary distribution"
    print insertions
    print "deletion length dictionary distribution"
    print deletions
    createHistogram(deletions, "Length Distribution", "Deletions", 'r')
    createHistogram(insertions, "Length Distribution", "Insertions", 'g')

if __name__ == '__main__':
    seqs = []
    with open(sys.argv[1]) as f:
        files = json.loads(f.read())["BlastJSON"]
        for filename in files:
            seqs.extend(file_to_seqs(filename["File"]))
    confusiondict = seqs_to_confusion(seqs)
    for b1 in bases:
        for b2 in bases:
            print b1 + " " + b2 + " " + str(confusiondict[(b1, b2)])
    confusion = seqs_to_confusion(seqs)
    confusion_to_nucleotides(confusion)
    makeLengthDistribution(seqs)
