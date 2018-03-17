# GenomeGit

GenomeGit is a distributed version control system based on the creation of git repositories for the storage of genomic data. Currently compatible with Unix systems.

### Prerequisites

The application requires installation of the following dependencies: 
* Python v 2.7+
* [Git](https://git-scm.com/downloads)

### Installation

To run the program, download the *GenomeGit* folder. Then, append to the PATH variable the directory to that folder```PATH=$PATH:ditectory```. You may need to make the main script executable: ```chmod u+x <path_to_GenomeGit/genomegit>```


## Running GenomeGit

To display the GenomeGit welcome message type ```genomegit```.
GenomeGit adapts regular git commands that can be run by typing ```genomegit <git_command>```. [See git documentation for more information on how to use git.](https://git-scm.com/doc)
Additional commands have been created to parse and reconstruct the input files containing genomic data.
To get the list of the most common commands you can type ```genomegit help```.

## Typical usage

### 1. Initializing the repository
The repository can be initialized by typing ```genomegit init```, which will create a *.gnmgit* directory. This directory will contain all the genomic data stored in the repository, including the *.git* repository itself. Additionally, it is possible to clone an existing repository using ```genomegit clone <url>```, which will create a *.gnmgit* with the cloned contents inside.

### 2. Parsing genome assembly files
The genome assembly of interest needs to be provided in form of a FASTA file, located in the same directory where the *.gnmgit* repository has been initialized. This file can then be processed by typing ```genomegit parse <filename>```, which will result in the creation of a *Genome* folder storing all the assembly information in form of git-compatible objects.

Note: Currently only 1 genome can be stored per branch. Any already existing *Genome* folder will be removed when parsing a new genome assembly file.

### 3. Recording changes made in the repository
After parsing the genome assembly file, user may add it to the repository: ```genomegit add <item_name>```, where ```item_name``` stands for the dataset to be added (e.g. Genome, Variants, Annotation...) (Note: Currently only ```Genome``` is supported). To add all datasets, user can type ```genomegit add .```
Then, these changes can be commited: ```genomegit commit -m "commit_message"```.

### 4. Remote repository access
In order to acces a remote repository, it is first needed to add a remote repository address. This can be done by typing ```genomegit remote add <remote_name> <url>```. To be up to date with the remote repository, the user needs to fetch the remote's data and integrate it to the local repository: ```genomegit pull <remote_name> <branch_name>```. Afterwards, user can introduce changes in the local repository and push them into the remote: ```genomegit push <remote_name>```.

### 5. Version log, checking out the desired version and recreating the FASTA file
User can switch to any of the stored assembly versions at any moment by typing ```genomegit checkout <commit_hash>```, where ```<commit_hash>``` stands for the SHA-1 commit hash of the version of interest. To obtain this hash, a review of versions can be viewed by typing ```genomegit log```. Finally, to recreate the original FASTA input file containing the genome assembly type ```genomegit reconstruct <line_length>```, where ```<line_length>``` specifies the number of nucleotides per line in the reconstructed FASTA file (default value is 60, all nucleotides of each sequence can be placed in one line by placing "." instead of an integer). This command will create a *reconstructed.fa* FASTA file (please note that the previous contents of any file named like this will be erased). If the user wants to upload the further files, main branch can be checked out: ```genomegit checkout <branch_name>```.

## Sample data and testing

### Sample data
Two sample assembly files containing *Drosophila Melanogaster* genome have been supplied in form of files *fruit_fly_v1.fa* and *fruit_fly_v2.fa*. These assemblies are publically available in the [NCBI database](https://www.ncbi.nlm.nih.gov/genome?term=vih&cmd=DetailsSearch), and correspond with versions ASM231075v1 (v1) and ASM231077v1 (v2).

### Sample testing protocol

#### Primary upload
1. Initialize the repository ```genomegit init``` in the chosen directory.

Note: You can clone into an existing repository instead ```genomegit clone genomegit@138.250.31.4:GenomeGit```.

2. Move the FASTA files into the directory with GenomeGit repository and parse *fruit_fly_v1.fa* ```genomegit parse fruit_fly_v1.fa```.

3. Record the changes by executing ```genomegit add .``` and ```genomegit commit -m "Version_1"```.

#### Remote access
4. Add the remote repository address ```genomegit remote add scarface genomegit@138.250.31.4:GenomeGit```.

Note: If the repository is not empty, you should pull the data ```genomegit pull scarface <branch>```. ```<branch>``` will usualy be called master.

5. Push your current data ```genomegit push scarface master```.

#### New version upload
7. Parse *fruit_fly_v2.fa* ```genomegit parse fruit_fly_v2.fa```.

8. Record the changes by executing ```genomegit add .``` and ```genomegit commit -m "Version_2"```.

Note:	In older verions of git you may need to include ```-A``` parameter during adding to include the removal of certain file parts. A proprer message will appear if that is the case.

9. Push your current data ```genomegit push scarface master```.

#### Recoverig version 1
10. See the version log ```genomegit log```.

11. Check out version one ```genomegit checkout <V1_commit_hash>```.

Note: In older versions of git, you may need to check out the genome folder afterwards ```genomegit checkout Genome```.

13. Reconstruct the file ```genomegit reconstruct 70```.

14. Make sure to check out to your main branch if you wish to upload the files further ```genomegit checkout <branch_name>```. The default branch should be called 'master'.

## Future plans
Future versions will be able to parse and store additional files containing gene annotations, SNPs variant calling... etc. This files will be auto-updated whenever the user uploads new genome assemblies.

## Authors

* **Patel Vineet**
* **Kourani Mariam**
* **Sanchez Rodriguez Filomeno**
* **Marek Ewa**
* **Bailey Emma**
* **Porc Jakub**
