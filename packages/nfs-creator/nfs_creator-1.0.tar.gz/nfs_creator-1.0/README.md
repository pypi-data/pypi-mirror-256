# wimex-nfs

## Name
WIMEX NFS creator.

## Test and Deploy

❌ : exportfs failed!. exportfs: duplicated export entries:
exportfs:       *:/var/data
exportfs:       *:/var/data

To fix the above error, edit this file and remove the newly added entries: 
```sudo vi /etc/exports```
Remove the lines added at the bottom. Both of the duplicate entries.

Tested on Ubuntu and CentOS Stream 8.

## Description
Wimex NFS creator (creates an NFS export/share/dir) is a utility package that can be installed via pip. It's used to test the host system of installation of nfs utility tools and check if the services are running. It's responsible to install NFS if it's not already installed and also responsible to create an NFS export.

## Installation
```sudo pip3 install nfs-creator```

## Usage
```
from nfs_creator import nfs_creator
nfs_creator() # by default the nfs export would be created at /var/data/

# provide a custom path
nfs_creator('/var/application')
```
## Authors and acknowledgment
@mujeebishaque 

## License
Closed Source

## Project status
Complete - Open for improvements.