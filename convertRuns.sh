#!/bin/bash

if [ $# -ne 2 ]
  then
    echo "ERROR: Too many or too few arguments, usage: convertRuns <StartRunNumber> <EndRunNumber>"
    exit 1
fi

if [ $(( $2 - $1 )) -lt 0 ]
	then
		echo "ERROR: End run number is smaller than start run number!"
	exit 1
fi 


for run in $(seq $1 $2)
do
	python ./purityAnalysis_pyroot.py -r $run
done
