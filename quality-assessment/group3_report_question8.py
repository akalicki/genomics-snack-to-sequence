"""
Usage: (python) group3_report1_question8.py
Takes in 2d_files.txt and times.txt from group3_report1_question8.sh
Matches files with those in tabular that are 2d. Extracts read_length and unix_timestamp
from times nanopore function. Makes a scatter plot with the data.

"""

import matplotlib.pyplot as plt
from scipy import stats
import numpy as np

#find 2d filenames from tabular function
filenames = []
with open('2d_files.txt', 'r') as f1:
	f1lines = f1.read().splitlines(True)
with open('times.txt', 'r') as f2:
	f2lines = f2.read().splitlines(True)
for line in f1lines[1:]:
	if len(line.split('\t')[1].split('twodirections:')) >1:
		x = line.split('\t')[1].split('twodirections:')[1]
		filenames.append(x)

#match up 2d filenames with those in times and aggregate those points
timestamp = []
read_length = []
for line in f2lines[1:]:
	elements = line.split('\t')
	filename = elements[1]
	if not elements[0].startswith("channel"):
		timestamp.append(int(elements[4])) #start read time
		read_length.append(int(elements[2])) #read_length

#print out statistics
slope, intercept, r_value, p_value, slope_std_error = stats.linregress(timestamp, read_length)
print "slope: " + str(slope)
print "intercept: " + str(intercept)
print "r_value: " + str(r_value)

#plot graph
plt.scatter(np.asarray(timestamp),np.asarray(read_length))
plt.xlabel('unix timestamp (s)')
plt.ylabel('read length')
plt.title("Q8 Sequence read length over time entered")
plt.axis([np.amin(np.asarray(timestamp)), np.amax(np.asarray(timestamp)), 0, 7000])
plt.savefig("images/q8_plot.png")
#plt.show()