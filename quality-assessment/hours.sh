#!/bin/bash
# A script to extract the fast5 files for the first and last hours of a read.
# Expects a file as input produced from "poretools times"
# run in the same directory that poretools was run in
# will create firsthour/pass and lasthour/pass directories
# outputs two fastq files consisting only of 2d reads from the first
# and last hours

FIRST=`awk 'NR == 2 || $10 < min {min = $10} END {print min}' $1`
echo "First hour number: ${FIRST}"

LAST=`awk 'NR == 2 || $10 > max {max = $10} END {print max}' $1`
echo "Last hour number: ${LAST}"

echo 'Copying relevant files into firsthour/lasthour directories...'
rm -rf firsthour
rm -rf lasthour
mkdir firsthour
mkdir lasthour
mkdir firsthour/pass
mkdir lasthour/pass

awk -v f=$FIRST 'NR > 2 && $10 == f {system("cp "$2" firsthour/"$2)}'  $1
awk -v l=$LAST 'NR > 2 && $10 == l {system("cp "$2" lasthour/"$2)}'  $1

echo 'extracting 2D reads in FASTQ format'
poretools fastq --type 2D firsthour/pass/ > pass_start.fastq
poretools fastq --type 2D lasthour/pass/ > pass_end.fastq
