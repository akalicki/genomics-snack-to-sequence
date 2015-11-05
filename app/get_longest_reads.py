"""
Places 100 longest reads into a new directory
Places all reads 3000 BP or longer in a folder called "3000BP"
arg 1 = name of directory of fast5 files
arg 2 = name of directory to place longest reads in
"""

import platform
import sys
from glob import glob
import os
import shutil

OS = platform.system()

allReadsDir = sys.argv[1]
longestReadsDir = sys.argv[2]
over3000Dir = "3000BP"

allReads = glob(allReadsDir + '/*.fast5')

try:
    os.stat(longestReadsDir)
except:
    os.mkdir(longestReadsDir)

try:
    os.stat(over3000Dir)
except:
    os.mkdir(over3000Dir)
    
longest100 = [(0, 0)] * 100

for fp in allReads:
    if(OS == "Windows"):
        fsplit = fp.split('\\')
    else:
        fsplit = fp.split('/')
    filename = fsplit[-1]
    os.system("poretools stats " + fp + " > " + "stats.txt")
    stats = open('stats.txt', 'r')
    stats.next()
    stats.next()
    meanReads = stats.next()
    stats.close()
    os.remove('stats.txt')
    print(meanReads)
    
    meanReadsNum = float(meanReads.split()[1])
    
    longest100.sort()
    
    if(meanReadsNum > longest100[0][0]):
        shortestFn = longest100[0][1]
        longest100[0] = (meanReadsNum, filename)
        if(OS == "Windows"):
            shutil.copyfile(allReadsDir + '\\' + filename, longestReadsDir + '\\' + filename)
            if(shortestFn != 0):
                os.remove(longestReadsDir + '\\' + shortestFn)
        else:
            shutil.copyfile(allReadsDir + '/' + filename, longestReadsDir + '/' + filename)
            if(shortestFn != 0):
                os.remove(longestReadsDir + '/' + shortestFn)
            
    if(meanReadsNum >= 3000):
        if(OS == "Windows"):
            shutil.copyfile(allReadsDir + '\\' + filename, over3000Dir + '\\' + filename)
        else:
            shutil.copyfile(allReadsDir + '/' + filename, over3000Dir + '/' + filename)
