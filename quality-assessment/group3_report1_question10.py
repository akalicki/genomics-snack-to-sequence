"""
Problem 10
places files in 'pass' folder in new folder called '2D' inside 'pass'
places files in 'fail' folder in new folder called '2D' inside 'fail'
runs poretools nucdist on each 2D folder using os module, saves result to nucdist.txt
parses percent and prints
ran into issue with interpreting the file 
"2D2DMINION01_3_minnows_3015_1_ch275_file42_strand.fast5" in 'pass' and found 
it to be corrupt; removed this file from the folder
"""

import sys
import os
import shutil
from glob import glob
import h5py

passFiles = glob('pass/*.fast5')
failFiles = glob('fail/*.fast5')

try:
    os.stat('pass/2D')
except:
    os.mkdir('pass/2D')
try:
    os.stat('fail/2D')
except:
    os.mkdir('fail/2D')

for fp in passFiles:
    f = h5py.File(fp,'r')
    fsplit = fp.split('\\') # change this to forward slash if not Windows
    filename = fsplit[-1]
    if 'BaseCalled_2D' in f['Analyses']['Basecall_2D_000'].keys():
        shutil.copyfile('pass/'+filename, 'pass/2D/'+filename)
    f.close()

for fp in failFiles:
    f = h5py.File(fp,'r')
    fsplit = fp.split('\\') # change this to forward slash if not Windows
    filename = fsplit[-1]
    if 'BaseCalled_2D' in f['Analyses']['Basecall_2D_000'].keys():
        shutil.copyfile('fail/'+filename, 'fail/2D/'+filename)
    f.close()

os.system("poretools nucdist pass/2D > nucdist.txt")
nucdist = open('nucdist.txt', 'r')
passAdata = nucdist.next()
passApercent = float(passAdata.split()[3]) * 100
passCdata = nucdist.next()
passCpercent = float(passCdata.split()[3]) * 100
passTdata = nucdist.next()
passTpercent = float(passTdata.split()[3]) * 100
passGdata = nucdist.next()
passGpercent = float(passGdata.split()[3]) * 100
nucdist.close()
os.remove('nucdist.txt')

print "Passed: A %f%%, C %f%%, T %f%%, G %f%%" % (passApercent, passCpercent, passTpercent, passGpercent)

os.system("poretools nucdist fail/2D > nucdist.txt")
nucdist = open('nucdist.txt', 'r')
failAdata = nucdist.next()
failApercent = float(failAdata.split()[3]) * 100
failCdata = nucdist.next()
failCpercent = float(failCdata.split()[3]) * 100
failTdata = nucdist.next()
failTpercent = float(failTdata.split()[3]) * 100
failGdata = nucdist.next()
failGpercent = float(failGdata.split()[3]) * 100
nucdist.close()
os.remove('nucdist.txt')

print "Failed: A %f%%, C %f%%, T %f%%, G %f%%" % (failApercent, failCpercent, failTpercent, failGpercent)