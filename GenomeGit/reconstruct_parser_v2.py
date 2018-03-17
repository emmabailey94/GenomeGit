#	README: HOW TO USE THE PROGRAM
#	Needs to be called inside the Genome directory so that it can find the seqID, the map file and the file paths in the map file make sense. A reconstructed
#	fasta file will be created one directory above the Genome folder. The first and only argument it takes is the number of nucleotides per line to be included
#	in the reconstructed file. If this argument equals ".", then all the sequence will be reconstructed into one line.

#	NOW THE CODE:

#Make the imports
import os
import sys
import re

#	PART 1. STORE THE SEQUENCE IDs

#Open the seqID file and store each of the IDs (one per line) in a list
seq_list=[]
seq_file=open("./seqIDs.txt","r")
line=seq_file.readline()
while line:
	seq_list.append(line)
	line=seq_file.readline()
#Close the seq ID file
seq_file.close()

#	PART 2. APPEND THE CONTIG SEQUENCES TO THE RECONSTRUCTED FASTA FILE

#First, determine the number of nucleotides per line to be used in the reconstructed file
one_line=False
#If the number of arguments is 0, the default line size is 60
if(len(sys.argv)==1):
	line_size=60
	#Inform the user
	print("Now begining reconstruction of the genomic data. Defaulting to 60 nucleotides per line.")

#If the user introduces a dot for the first parameter, the line size will be the total length of the sequence
elif(str(sys.argv[1])=="."):
	one_line=True
	#Inform the user
	print("Now begining reconstruction of the genomic data. Reconstructed fasta file will contain all the nucletoides of each sequence fitted into one line")

#Only if the number specified by the user is an actual number, use it as the line size
elif (sys.argv[1].isdigit()):
	if(int(sys.argv[1])>0):
		line_size=int(sys.argv[1])
	#Inform the user
	print("Now begining reconstruction of the genomic data. Reconstructed fasta file will contain "+str(line_size)+" nucleotides per line.")

#Otherwise the input was not valid
else:
	print("Please select a valid positive number as the line size of the reconstructed FASTA file. Default value is 60.")
	sys.exit()

#Open a reconstruct file which will be the reconstructed fasta
reconstruct=open("../reconstructed.fa","w+")
#Open the input map file and read the first line
map=open("./Map.txt","r")
line=map.readline()
#Initiate required variables
seq_count=-1
current_sequence=""
#Loop through the lines of the map file
while line:
	#If the line starts with ">", it corresponds with a new sequence
	if(line[0]==">"):
		seq_count+=1
		#Unless this is the first sequence, write the currently stored sequence in the reconstructed file.
		if(seq_count!=0):
			#Write the seq ID
			reconstruct.write(seq_list[seq_count-1])
			#If the user wants all the sequence in one line, do so
			if(one_line):
				reconstruct.write(current_sequence+"\n")
				#Empty current sequence
				current_sequence=""
			#Otherwise use the specified line size
			else:
				reconstruct.write('\n'.join(current_sequence[y:y+line_size] for y in range(0, len(current_sequence), line_size))+"\n")
				#Empty current sequence
				current_sequence=""
	#If the line does not start with an > or a N, it corresponds with the path to a sequence file
	elif(line[0]!="N"):
		#Split the line using the \t. The first field should correspond with the full path to the contig file.
		line=re.split("\t",line)
		input_file=open(line[0],"r")
		#Open the file, store all its lines and remove all whitespaces and \n characters
		file_content=input_file.read()
		file_content=re.sub('\s+','',file_content)
		#Store all the sequence of the contig file
		current_sequence=current_sequence+file_content
	#Otherwise the line corresponds to a gap
	else:
		#Split the line using the \t and then with the \s. The start is the first number and the stop the second one
		line=re.split("\t",line)
		line=line[1]
		line=re.split(" ",line)
		#Add the gap into the current sequence. The size of the gap is the difference between the stop and the start plus one
		current_sequence=current_sequence+"N"*int(int(line[1])-int(line[0])+1)
	#Read the next line
	line=map.readline()

#Add the last sequence left out of the loop
reconstruct.write(seq_list[seq_count])
if(one_line):
	reconstruct.write(current_sequence+"\n")
else:
	reconstruct.write('\n'.join(current_sequence[y:y+line_size] for y in range(0, len(current_sequence), line_size))+"\n")

#Close all the files
map.close()
reconstruct.close()
