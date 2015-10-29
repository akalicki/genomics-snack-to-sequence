#!/usr/bin/env bash
#
# Usage: ./group3_report1_question8.sh [directory with pass and fail]
# 
# Runs the script for question4. 

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 [directory with pass and fail]" >&2
    exit 1
fi

poretools tabular -q --type 2D $1"/pass/" > 2d_files.txt
poretools tabular -q --type 2D $1"/fail/" >> 2d_files.txt
poretools times -q $1"/pass/" > times.txt
poretools times -q $1"/fail/" >> times.txt
python group3_report1_question8.py

exit 0