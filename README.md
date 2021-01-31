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

    # curl https://raw.githubusercontent.com/rlunaro/yams/main/src/minecraft.py --output minecraft.py

After that, give execution permissions to the script. 

Edit the script and configure these variables: 

    JAVA_HOME=""
    
    MINECRAFT_INSTALL=""
    
The first must point the current java setup you have in your minecraft server and the later must point to the directory you 
are running this launcher. 

## Run the "setup" option of the launcher

First, run the script with the `setup` argument: 

    $ ./minecraft.py setup
    
This will make the download of the minecraft server to the latest version. 





## Additional configuration 

The file **`logging_example.json`** is an example on how the logging can be configured in order to properly diagnose this 
launcher and keep a decent logging. Even it can be configure to log with the rest of the logs of the machine. 

## Known problems 

### directory MINECRAFT_INSTALL does not exist

This is caused because you haven't properly configured the variable MINECRAFT_INSTALL in the script. You have to edit the 
script, with an editor of your choice, and set to this directory the directory in which your script is. 

For instance, if your `minecraft.py` is installed in `/home/minecraft/` the variable MINECRAFT_INSTALL would look like this: 

    MINECRAFT_INSTALL="/home/minecraft"
    
### java executable not found

This is caused because you haven't set properly the variable JAVA_HOME in the script. You have to edit it with an editor
of your choice. 

Let's say that java is installed under `/usr/lib/jvm/java-11-openjdk-amd64`, then your JAVA_HOME variable would look like this:

    JAVA_HOME = "/usr/lib/jvm/java-11-openjdk-amd64"

### Error in the checking of new server version

If you found this error from time to time in the logging, it's normal: this can be caused for a temporary down of the minecraft servers. 

On the other hand, **if you found this error the very first you are running this script**, there is a problem, because the script 
can't donwload the latest version of the server. I recommend you to check your internet connection and try again a bit later.

**If you are in a corporate environment,** (I wonder who are running a minecraft server in a corporate environment) this problem can 
be caused because you need a proxy to access the internet. Unfortunately, I've didn't make any arrangement to support proxy connections 
in this script, however, let me know. I always are receptive about request for this little tiny project, but I have to tell you 
that I won't make the fixing quickly. I have an hectic day-to-day and finding ne necessary time to fix this takes me time. 







