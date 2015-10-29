"""
Usage: (python) group3_report1_question4.py
Takes in 2d_files.txt and times.txt from group3_report1_question4.sh
Matches files with those in tabular that are 2d. Extracts read_length and duration
from times nanopore function. Adds them up and calculates the time for sequencing a
genome in one read.
"""

import numpy as np

#find 2d filenames from tabular function
filenames = []
with open('2d_files.txt', 'r') as f1:
	f1lines = f1.read().splitlines(True)
with open('times.txt', 'r') as f2:
	f2lines = f2.read().splitlines(True)
for line in f1lines[1:]:
	x = line.split('\t')[1].split('twodirections:')[1]
	filenames.append(x)

#match up 2d filenames with those in times and aggregate those points
duration = []
read_length = []
for line in f2lines[1:]:
	elements = line.split('\t')
	filename = elements[1]
	if filename in filenames:
		duration.append(int(elements[5])) #duration
		read_length.append(int(elements[2])) #read_length

total_seconds = np.sum(np.asarray(duration))
total_read_length = np.sum(np.asarray(read_length))
print total_read_length
human_genome_base_pairs = 3.0e9
print "num days: " + str(((human_genome_base_pairs/total_read_length)*total_seconds)/3600/24)
#also consider the fact that it's diploid

#result
#23552
#2875631
#num days: 284.382028771