####
##	***PART 1. CREATE FUNCTIONS (SUBROUTINES)***
####

#Make the imports
import sys
import os
import re

#Define the parse contig function. This function will take a nucleotide sequence, athe number of the sequence count, the map file, the current folder and the
#sequence index as input parameters. It will create a file for each contig, but if the 250.000 nt threshold is reached it will create a folder contaiing equally
#sized files. Additionally it has to return the updated index.
def parse_cntg(seq,number,map_file,folder,seq_index):
	#Save the input arguments
	current_nucleotides=seq
	i=number
	map=map_file
	current_dir=folder
	index=seq_index
	#If the file is empty, this means the sequence started with Ns (this may occur during scaffold parsing).
	#In this case, do not write a contig file (it would be empty)
	if(len(current_nucleotides)==0):
		pass
	#If the length of the contig is smaller than 250.000 nt, write a single file
	elif (len(current_nucleotides)<250000):
		#Write the file
		output_file=open(current_dir+"/Sequence"+str(i), "w+")
		output_file.write(current_nucleotides)
		output_file.close()
		#Write in the map file
		map.write(current_dir+"/Sequence"+str(i)+"\t"+str(index)+" "+str(index+len(current_nucleotides)-1)+"\n")
		index=index+len(current_nucleotides)
	#If this contig is bigger than 250.000 nt, split it into files of 100.000 nt each
	else:
		#Divide the current contig into chunks of 100.000 nt
		chunks=[current_nucleotides[y:y+100000] for y in range(0, len(current_nucleotides), 100000)]
		#Create a new folder to store those chunks
		current_dir=current_dir+"/Sequence"+str(i)
		os.mkdir(current_dir)
		#Create chunk_count
		chunk_count=0
		#Write each chunk in a separate file
		for chunk in chunks:
			chunk_count=chunk_count+1
			#Write the file
			output_file=open(current_dir+"/Sequence"+str(chunk_count),"w+")
			output_file.write(chunk)
			output_file.close()
			#Write in the map file
			map.write(current_dir+"/Sequence"+str(chunk_count)+"\t"+str(index)+" "+str(index+len(chunk)-1)+"\n")
			index=index+len(chunk)
	#Return the updated index
	return index

#Define the parse scaffold function. It has to return an updated index.
def parse_scf(seq,folder,map_file,seq_index):
	#Save the arguments
	current_nucleotides=seq
	current_dir=folder
	map=map_file
	#Store all the contigs in one list
	contig_list=re.split("N+", current_nucleotides)
	#Store all the gaps in one list and remove any empty element
	gap_list=re.split("[^N]+", current_nucleotides)
	gap_list=test=filter(None,gap_list)
	#Initiate the index, the count of subsequences and the current subsequence
	subseq_count=0
	index=seq_index
	current_subsequence=""
	#Loop through all the contigs in the list
	for x in range(0,len(contig_list)):
		#Add the current contig into the current subsequence
		current_subsequence=current_subsequence+contig_list[x]
		#If this is the last contig, write the current subsequence into a file
		if(x==len(contig_list)-1):
			subseq_count=subseq_count+1
			index=parse_cntg(seq=current_subsequence,number=subseq_count,map_file=map,folder=current_dir,seq_index=index)
		#If the next gap is smaller than 25, iterate to the next contig. DONT FORGET TO ADD THOSE Ns!!!
		elif(len(gap_list[x])<25):
			current_subsequence=current_subsequence+gap_list[x]
			continue
		#Otherwise store the current subsequence in a new file
		else:
			subseq_count=subseq_count+1
			index=parse_cntg(seq=current_subsequence,number=subseq_count,map_file=map,folder=current_dir,seq_index=index)
			map.write("N\t"+str(index)+" "+str(index+len(gap_list[x])-1)+"\n")
			index=index+len(gap_list[x])
			current_subsequence=""
	#Return the updated index
	return index

#Create a method to parse the super subsequences
def parse_super(seq_list,gap_list,folder,map_file):
	#Save the arguments
	super_subseq_list=seq_list
	super_gaps_list=gap_list
	current_dir=folder
	map=map_file
	#Subsequence count is 0 and index is 1
	subseq_count=0
	index=1
	#For each of the super subsequences, determine their class and act accordingly
	for x in range(0, len(super_subseq_list)):
		subseq_count=subseq_count+1
		#If the super subsequence is empty (this will occur when the sequence starts or ends with Ns) dont do anything, only update the map if necessary
		if(len(super_subseq_list[x])==0):
			#Unless this empty supergap is at the end (this would mean the sequence ends with Ns), update the map file
			if(x!=len(super_gaps_list)):
				map.write("N\t"+str(index)+" "+str(index+len(super_gaps_list[x])-1)+"\n")
				index=index+len(super_gaps_list[x])
		#If this sequence is a contig, store its content in a new file and write the roadmap
		elif(IsContig(super_subseq_list[x])):
			#Parse the contig
			index=parse_cntg(seq=super_subseq_list[x],number=subseq_count,map_file=map,folder=current_dir,seq_index=index)
			#Only if this is not the last super subsequence, write in the map file the Ns
			if(x!=len(super_gaps_list)):
				#Write in the map file
				map.write("N\t"+str(index)+" "+str(index+len(super_gaps_list[x])-1)+"\n")
				index=index+len(super_gaps_list[x])
		#If this sequence is a scaffold, store its contigs in a new folder
		else:
			#Create a new folder to allocate the scaffold
			current_subfolder=current_dir+"/Sequence"+str(subseq_count)
			os.mkdir(current_subfolder)
			#Parse the scaffold
			index=parse_scf(seq=super_subseq_list[x],folder=current_subfolder,map_file=map,seq_index=index)
			#Only if this is not the last super subsequence, write in the map file the N gap
			if(x!=len(super_gaps_list)):
				#Write the map file
				map.write("N\t"+str(index)+" "+str(index+len(super_gaps_list[x])-1)+"\n")
				index=index+len(super_gaps_list[x])

#Create a parse nucleotides function
def parse_nucleotides(seq,number,map_file):
	#Store the arguments
	current_nucleotides=seq
	i=number
	map=map_file
	#If this sequence is a contig, store its content in a new file and write the roadmap
	if(IsContig(current_nucleotides)):
		#Write the info about the current sequence in the map file
		map.write(">Sequence"+str(i)+"\t"+str(len(current_nucleotides))+"\n")
		#Parse the contig
		parse_cntg(seq=current_nucleotides,number=i,map_file=map,folder=".",seq_index=1)
	#If this sequence is a scaffold, store its contigs in a new folder
	elif(IsScaffold(current_nucleotides)):
		#Create a directory and write the map
		current_dir="./Sequence"+str(i)
		os.mkdir(current_dir)
		map.write(">Sequence"+str(i)+"\t"+str(len(current_nucleotides))+"\n")
		#Parse the scaffold
		parse_scf(seq=current_nucleotides,folder=current_dir,map_file=map,seq_index=1)
	#If it is not a contig or a scaffold, it is a chromosome
	else:
		#Create a directory and write the map
		current_dir="./Sequence"+str(i)
		os.mkdir(current_dir)
		map.write(">Sequence"+str(i)+"\t"+str(len(current_nucleotides))+"\n")
		#Store all the subsequences separated by N-10000+ gaps in a list
		pattern="N"*10000
		super_subseq_list=re.split(pattern+"+",current_nucleotides)
		#Store all the N-10000+ gaps in one list, remove empty elements and those which are lower than 10.000
		super_gaps_list=re.split("[^N]+", current_nucleotides)
		super_gaps_list=filter(None,super_gaps_list)
		super_gaps_list=[g for g in super_gaps_list if len(g) >= 10000]
		#If there are no super gaps, the whole sequence is like a large scaffold
		if(len(super_gaps_list)==0):
			#All the sequence is a large scaffold
			parse_scf(seq=current_nucleotides,folder=current_dir,map_file=map,seq_index=1)
		#Otherwise parse each super subsequence
		else:
			#Parse each of the super subsequences
			parse_super(seq_list=super_subseq_list,gap_list=super_gaps_list,folder=current_dir,map_file=map)

#Define a the contig and the scaffold classification function
def IsContig(seq):
	#Check if it has gaps bigger than N-25, in which case this is a contig
	if(current_nucleotides.find("NNNNNNNNNNNNNNNNNNNNNNNNN")==-1):
		return True
	else:
		return False
def IsScaffold(seq):
	#If it has N-25 gaps and its length is lower than 1.000.000, this is a scaffold
	if(len(current_nucleotides)<1000000):
		return True
	else:
		return False

####
##	***PART 2. PARSE THE INPUT FILE***
####

#Load the input file
input_path=sys.argv[1]
input_file=open(input_path, "r")
line=input_file.readline
#Initiate necessary variables
i=0
current_nucleotides=""
map=open("Map.txt", "w+")
invalid_input=True
#Loop through the lines of the file
line=input_file.readline()
while line:
	#Only read the line if it does not start with a # (description lines can start with this)
	if(line[0]!="#"):
		#Remove all new lines (sequence stored as a big line)
		line=line.rstrip()
		#If the line starts with that symbol, this is a new sequence
		if (line[0]==">"):
			#The input file is not invalid anymore
			invalid_input=False
			#Unless this is the first sequence, write a file with its nucleotides
			if(current_nucleotides!=""):
				parse_nucleotides(seq=current_nucleotides,number=i,map_file=map)
			#Add one to the sequence count
			i=i+1
			#Empty the current nucleotides
			current_nucleotides=""
		#Otherwise store the current sequence in the current_nucleotides variable
		else:
			current_nucleotides=current_nucleotides+line

		#Read the new line
		line=input_file.readline()

#If when the parsing is finished, the input file has not been validated, raise an exception
if(invalid_input):
	print("\n\n\t***INPUT ERROR: Please make sure to input a valid FASTA format file***\n")
	sys.exit()

#Parse the last sequence left out of the loop
parse_nucleotides(seq=current_nucleotides,number=i,map_file=map)
#Close the map file
map.close()
