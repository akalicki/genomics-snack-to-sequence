import subprocess
import sys
import matplotlib.pyplot as plt
import numpy as np


def getHistogramData(poretools_command):
	proc = subprocess.Popen(poretools_command, stdout=subprocess.PIPE, shell=True)
	data = []
	odd = True
	for read in proc.stdout:
		if not odd:
			data.append(len(read))
		odd = not odd
	return data

def createHistogram(data, d, q):
	plt.hist(np.asarray(data))
	plt.title(d + " (" + q + ")")
	plt.ylabel("Frequency")
	plt.xlabel("Length of Read (nucleotides)")
	plt.savefig(d + "-" + q)
	plt.clf()

path_pass = sys.argv[1] # file path for pass reads
path_fail = sys.argv[2] # file path for fail reads

# Histogram of 1D pass
poretools_command = "poretools fasta --type fwd,rev " + path_pass
data = getHistogramData(poretools_command)
createHistogram(data, "1D", "Pass")

# Histogram of 2D pass
poretools_command = "poretools fasta --type 2D " + path_pass
data = getHistogramData(poretools_command)
createHistogram(data, "2D", "Pass")

# Histogram of 1D fail
poretools_command = "poretools fasta --type fwd,rev " + path_fail
data = getHistogramData(poretools_command)
createHistogram(data, "1D", "Fail")

# Histogram of 2D fail
poretools_command = "poretools fasta --type 2D " + path_fail
data = getHistogramData(poretools_command)
createHistogram(data, "2D", "Fail")
