# yams
yams: Yet Another Minecraft Server

# Yes: yet another Minecraft server

I've developed this single-file python script to take care of a Minecraft server. My son use to play Minecraft and from 
time to we start a new shared server. When doing that, we have to face several challenges: 

  - to ensure, at every time, that the server is up and running 
  - to ensure that the server is running with the latest version available (or not)
  
To accomplish this task, I've started by building a simple shell script, but recently I've migrated this to python. Migrate to 
python allowed me to implement a downloader of the latest version of the server.


# Installation

Here, I will provided the most detailed instructions to setup a minecraft server, taking into account usual security considerations. 
To enforce security of the server, scope is outside this document and probably you will have to request specialized help. 

Let's go, step by step....

## Prerequisites

  - some knowledge of Linux (Ubuntu preferably)
  - some knowledge of computer networks

## Bring in a linux server

These instructions are for Ubuntu. For other Linux versions, instructions might vary. 

## Create a user dedicated for hosting the server files

For the purpose of this manuail, let's say that the user we are going to create is `minecraft`:

    $ sudo useradd --create-home --shell /bin/bash --user-group minecraft
    
And the home directory will be `/home/minecraft`.
   
## Install the necessary packages 

For run this script you will need python: 

    $ sudo apt-get install python3
    
**Note:** If you will to run this script in a virtual python environment (those created with `virtualenv` or `pytno -m venv`), then 
probably the script minecraft_example.sh will help you. 

## Grab a copy of the minecraft.py python code and deploy in the home directory of the server 

For instance: 

    $ sudo su 
    # cd /home/minecraft 
    # 
    



