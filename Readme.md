# GenomeGit

GenomeGit is a distributed version control system for genome assembly data and dependent files such as annotation, variant calling and alignment. It uses the git program to create and manage the repository. Currently it is available for the Unix systems.


### Prerequisites

In order to run the program you will need the following programs: Java, python, git.


### Installing

To run the program, download the *GenomeGit* folder. Then, append to the PATH variable the directory to that folder.

```
PATH=$PATH:ditectory
```

## Running GenomeGit

To display the GenomeGit welcome message type ```genomegit```.
GenomeGit adapts regular git commands that can be run by typing ```genomegit <git_command>```.
Additional commands have been created to parse the files.
To get the list of the most common commands you can type ```genomegit help```.

## Typical usage

### Initializing the repository
The repository can be initialized by typing ```genomegit init```. In your current directory a *.gnmgit* folder should be created. All of the repository files will be placed in that folder, including git repository folder *.git* . You can clone into an existing repository: ```genomegit clone <url>```. A *.gnmgit* folder will be created, and the contents of the repository will be put inside it.

### Parsing the files
You should place the file that you wish to parse into the GenomeGit repository directory. Then, type ```genomegit parse <filename>```. A *Genome* folder will be created in the repository (*.gnmgit* folder) with the processed file. 
Note: Currently only 1 genome can be stored per branch. Existing *Genome* folder will be removed*.

### Recording changes made to the repository
After uploading the genome you should add it to the repository: ```genomegit add <itemname>```. If you wish to add the parsed file to the repository, you can type ```genomegit add .```.
Then, you can commit the changes: ```genomegit commit -m "commit_message"```.

### Remote repository access
In order to acces a remote repository, you firs need to add a remote repository address. You can do that by typing ```genomegit remote add <remote_name> <url>```. To be up to date with the repository, you need to fetch the data from it and integrate: ```genomegit pull```. Then, anfter making changes to the repository, you can push the changes: ```genomegit push```.

### Version log, checking out the desired version and recreating the FASTA file
In order to switch to a chosen version of genome, you will need to find out the hash of the commit corresponding to the version of your choice. To review the list of versions of the genome you can type ```genomegit log```. Then you can switch by typing ```genomegit checkout <commit_hash>```. Finally, to recreate the file from the repository, type ```genomegit reconstruct```.

## Sample data and testing

### Data
Test files called *fruit_fly_v1* and *fruit_fly_v2* containing the assembly data of the fruit fly are provided and can be used in testing.

### Sample testing protocol

#### Primary upload
1. Initialize the repository ```genomegit init``` in the chosen directory
2. Move the faste files into the chosen directory and parse *fruit_fly_v1* ```genomegit parse fruit_fly_v1```
3. Record the changes by executing ```genomegit add .```, ```genomegit commit -m "Version_1"```
#### Remote access
4. Add the remote repository address ```genomegit remote add scarface genomegit@138.250.31.4:Desktop/GenomeGit```
5. Pull the data ```genomegit pull```
6. Push your current data ```genomegit push```
#### New version upload
7. Parse *fruit_fly_v2* ```genomegit parse fruit_fly_v1```
8. Record the changes by executing ```genomegit add .```, ```genomegit commit -m "Version_2"```
9. Push your current data ```genomegit push```


## Authors

* **Patel Vineet**
* **Kourani Mariam**
* **Sanches Rodriguez Filomeno**
* **Marek Ewa**
* **Bailey Emma**
* **Porc Jakub**
