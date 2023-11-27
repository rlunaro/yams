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
    
**Note:** If you will to run this script in a virtual python environment (those created with `virtualenv` or `python -m venv`), then 
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

## Opening firewalls

The server will need the port 25000 to communicate with its clients. You must open this port in the server firewall to accomplish this. 
In Ubuntu, this is done by running (as root): 

    # ufw allow 25000
    
Maybe the firewall is not running at all: 

    # ufw status 
    Status: inactive
    
This is not the safest configuration (unless you have a hardware firewall set up), but in the later case no configuration
is needed at all. 

## Run the "setup" option of the launcher

First, run the script with the `setup` argument: 

    $ ./minecraft.py setup
    
This will make the download of the minecraft server to the latest version. 

## Make a test start of the server 

Run: 

    $ ./minecraft.py start 
    
To start the server as a test. You will find that nothing happens or _almost_ nothing happens. A new file `console.log` have 
happeared in the directory. If you check out the contents: 

   $ more console.log
   [10:29:31] [main/ERROR]: Failed to load properties from file: server.properties
   [10:29:32] [main/WARN]: Failed to load eula.txt
   [10:29:32] [main/INFO]: You need to agree to the EULA in order to run the server. Go to eula.txt for more info.
 
 and, checking the eula.txt file: 
 
   $ more eula.txt
   #By changing the setting below to TRUE you are indicating your agreement to our EULA (https://account.mojang.com/documents/minecraft_eula).
   #Sun Jan 31 10:29:32 CET 2021
   eula=false

 It says that you have to accept the End User License Agreement. You can download it in the 
 [given address](https://account.mojang.com/documents/minecraft_eula), (or read it online), think 
 about carefully and after that, you can change `eula=false` for `eula=true` _only if you agree 
 to the terms of the license_. 
 
 If you have made the later step, you can launch the server again: 
 
     $ ./minecraft.py start 
 
 And this time, something happens. There is a java process that is eating an important part of the machine: 
 
    $ ps aux | grep java
    minecraft     5530  312 12.5 4924776 488288 pts/0  Sl   10:35   0:15 /usr/lib/jvm/java-11-openjdk-amd64/bin/java 
    -Xms1300M -Xmx1500M -Djava.awt.headless=true -jar /home/rluna/machines/minecraft/minecraft.jar nogui

That's it!!!! you have got it!!!!

## Make a test of the stop of the server 

To stop the server, just execute: 

    $ ./minecraft.py stop 
    
And that's it: no java process will remain after that (unless you are running many servers in paralell in the same machine). 

## Configure the script as systemd service

By configuring your minecraft service as a systemd service, you will gain two important things: 

  1. Whenever you start the machine, it will start the service _automagically_
  2. Whenever you shut down the machine, it will shut down the service for you (or at least, it will try)

Given that:

  * our installation is in `/home/minecraft`
  * the user that will start this service is `minecraft`
  * the java virtual machine is in `/usr/lib/jvm/java-11-openjdk-amd64`
  
A suitable configuration would be: 

	[Unit]
	Description=A Minecraft service
	After=network.target auditd.service syslog.service
    ConditionPathExists=/home/minecraft/minecraft.py
    ConditionPathExists=/usr/lib/jvm/java-11-openjdk-amd64/bin/java

	[Service]
	Type=forking
	User=minecraft
	WorkingDirectory=/home/minecraft
	ExecStart=/home/minecraft/minecraft.py start
	ExecStop=/home/minecraft/minecraft.py stop
	PIDFile=/home/minecraft/pidfile
	Restart=always

	[Install]
	Alias=minecraft.service


Write your own `minecraft.service` file and then move it to the '/lib/systemd/system' directory: 

    # mv minecraft.service /lib/systemd/system
    # chown root:root /lib/systemd/system/minecraft.service
    # chmod g=r,o=r /lib/systemd/system/minecraft.service
    
And create the corresponding symbolic links: 

    # ln -s /lib/systemd/system/minecraft.service /etc/systemd/system
    # ln -s /lib/systemd/system/minecraft.service /etc/systemd/system/multi-user.target.wants/

Then, you are ready to start the service: 

    # systemctl daemon-reload
    # systemctl enable minecraft.service
    
**And that's all!!!** Everytime the machine rstarts, it will restart the minecraft service. 

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







