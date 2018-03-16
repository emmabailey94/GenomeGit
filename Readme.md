# GenomeGit

GenomeGit is a distributed version control system for genome assembly data. It uses the git program to create and manage the repository. Currently it is available for the Unix systems.

### Prerequisites

In order to run the program you will need the following programs: Java, python, git.

### Installing

To run the program, download the *GenomeGit* folder. Then, append to the PATH variable the directory to that folder```PATH=$PATH:ditectory```. You may need to make the main script executable: ```chmod u+x <path_to_GenomeGit/genomegit>```


## Running GenomeGit

To display the GenomeGit welcome message type ```genomegit```.
GenomeGit adapts regular git commands that can be run by typing ```genomegit <git_command>```. See git documentation for more information on how to use git: https://git-scm.com/doc.
Additional commands have been created to parse and reconstruct the files.
To get the list of the most common commands you can type ```genomegit help```.

## Typical usage

### Initializing the repository
The repository can be initialized by typing ```genomegit init```. In your current directory a *.gnmgit* folder should be created. All of the repository files will be placed in that folder, including the git repository folder *.git* . You can clone into an existing repository: ```genomegit clone <url>```. A *.gnmgit* folder will be created, and the contents of the repository will be put inside it.

### Parsing the files
You should place the file that you wish to parse into the folder with GenomeGit repository . Then, type ```genomegit parse <filename>```. A *Genome* folder will be created in the repository (*.gnmgit* folder) with the processed file. 
Note: Currently only 1 genome can be stored per branch. Existing *Genome* folder will be removed*.

### Recording changes made to the repository
After uploading the genome you should add it to the repository: ```genomegit add <itemname>```. If you wish to add everything, you can type ```genomegit add .```.
Then, you can commit the changes: ```genomegit commit -m "commit_message"```.

### Remote repository access
In order to acces a remote repository, you first need to add a remote repository address. You can do that by typing ```genomegit remote add <remote_name> <url>```. To be up to date with the repository, you need to fetch the data from it and integrate: ```genomegit pull <remote_name> <branch_name>```. Then, anfter making changes to the repository, you can push the changes: ```genomegit push <remote_name>```.

### Version log, checking out the desired version and recreating the FASTA file
In order to switch to a chosen version of genome, you will need to find out the hash of the commit corresponding to the version of your choice. To review the list of versions of the genome you can type ```genomegit log```. Then you can switch by typing ```genomegit checkout <commit_hash>```. Finally, to recreate the file from the repository, type ```genomegit reconstruct <line_length>```. <line_length> specifies the noumber of nucleotides per line in the output file. Make sure to check out to your main branch if you wish to upload the files further ```genomegit checkout <branch_name>```.

## Sample data and testing

### Data
Test files called *fruit_fly_v1* and *fruit_fly_v2* containing the assembly data of the fruit fly are provided and can be used in testing. An empty repository on the 'Scarface' server can be used

### Sample testing protocol

#### Primary upload
1. 	Initialize the repository ```genomegit init``` in the chosen directory

Note: 	You can clone an existing repository instead ```genomegit clone genomegit@138.250.31.4:GenomeGit```

2. 	Move the FASTA files into the directory with GenomeGit repository and parse *fruit_fly_v1* ```genomegit parse fruit_fly_v1.fa```

3. 	Record the changes by executing ```genomegit add .``` and ```genomegit commit -m "Version_1"```

#### Remote access
4. 	Add the remote repository address ```genomegit remote add scarface genomegit@138.250.31.4:GenomeGit```

Note: 	If the repository is not empty, you should pull the data ```genomegit pull scarface <branch>```. <branch> will usualy be called master.

5. 	Push your current data ```genomegit push scarface master```

#### New version upload
7. 	Parse *fruit_fly_v2* ```genomegit parse fruit_fly_v2.fa```

8. 	Record the changes by executing ```genomegit add .``` and ```genomegit commit -m "Version_2"```

Note:	In older verions of git you may need to include ```-A``` parameter during adding to include the removal of certain file parts. A proprer message will appear if that is the case.

9. 	Push your current data ```genomegit push scarface master```

#### Recoverig version 1
10. 	See the version log ```genomegit log```

11. 	Check out version one ```genomegit checkout <V1_commit_hash>```

Note: 	In older versions of git, you may need to check out the genome folder ```genomegit checkout Genome```

13. 	Reconstruct the file ```genomegit reconstruct 70```

14.	Make sure to check out to your main branch if you wish to upload the files further ```genomegit checkout <branch_name>```. The default branch should be called 'master'.

## Future plans
In the future, we plan to include a possibility to parse and store dependant files such as annotation, variant calling etc.

## Authors

* **Patel Vineet**
* **Kourani Mariam**
* **Sanches Rodriguez Filomeno**
* **Marek Ewa**
* **Bailey Emma**
* **Porc Jakub**
