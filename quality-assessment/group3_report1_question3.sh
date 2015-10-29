#!/usr/bin/env bash
#
# Usage: ./group3_report1_question3.sh [fast5_directory] [save_path]
# 
# Takes a directory full of FAST5 files as well as an optional path for saving,
# then plots the cumulative base pairs sequenced as a function of time. The save
# path can either be a PNG or a PDF if it is included. Requires poretools as
# well as the ggplot2 R package for graphing.

if [ "$#" -ne 1 ] && [ "$#" -ne 2 ]; then
    echo "Usage: $0 [fast5_directory] [save_path]" >&2
    exit 1
fi

# plot cumulative basepairs vs time for reads in folder
if [ "$#" -eq 2 ]; then
    poretools yield_plot --plot-type basepairs --saveas $2 $1
else
    poretools yield_plot --plot-type basepairs $1
fi

exit 0
