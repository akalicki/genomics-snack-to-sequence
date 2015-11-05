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

TOMATO_SCI_1 = "Solanum lycopersicum"
TOMATO_SCI_2 = "Solanum pennellii"

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
    """Takes a lit of (qseq, hseq) pairs, and returns a confusion matrix"""
    confusion = defaultdict(int)
    for pair in seq_list:
        qseq = pair[0]
        hseq = pair[1]
        for i in range(len(qseq)):
            key = (qseq[i].upper(), hseq[i].upper())
            confusion[key] += 1
    return confusion

bases = ['A','C','G','T','-']
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
