"""
Converts a folder of fast5 files into fasta files
arg 1 = name of fast5 directory
arg 2 = name of fasta directory
"""

import sys
import platform
from glob import glob
import os

OS = platform.system()
fast5dir = sys.argv[1]
fastadir = sys.argv[2]

fast5Files = glob(fast5dir + '/*.fast5')

try:
    os.stat(fastadir)
except:
    os.mkdir(fastadir)

for fp in fast5Files:
    if(OS == "Windows"):
        fsplit = fp.split('\\')
    else:
        fsplit = fp.split('/')
    filename = fsplit[-1]
    os.system("poretools fasta " + fp + " > " + fastadir + "/" + filename + ".txt")