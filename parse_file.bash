#!bin/bash

##Usage:
##First argument: Full path to fasta file containing the sequence

source="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

##Create a directory to contain the genome. If it already exists, delete its contents.
if [ -d ./Genome ]; then
	rm -r ./Genome/*
else
	mkdir ./Genome
fi

##Enter the new directory
cd ./Genome

##Create seqIDs file inside the directory
grep -o -E "^>.*" $1 > seqIDs.txt
##Determine the number of sequences
sequence_number=$(grep -c ">" $1)

#Only if the number of sequence is higher than one, proceed to parse it
if [ $sequence_number -gt 0 ]; then
	##Parse the fasta file
	echo "Now processing $1 containing $sequence_number sequences:"
	date

	##Call python script to parse all the sequences in the input file
	## ***FILE PATH NEEDS TO BE CHANGED HERE***
	python ${source}/parse_seq.py $1

	##Inform the user the process is doe
	echo ""
	echo "Genome parsing finished:"
	date
else
	echo "No sequences were detected in $1"
	echo "Please make sure to input a valid fasta file"
fi
