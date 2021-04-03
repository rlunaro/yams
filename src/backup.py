#!/usr/bin/python
'''
Copyright 2021 superman_ha_muerto@yahoo.com

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.


@author: rluna
'''
import logging
import sys
import os
import os.path
import zipfile
import datetime
import subprocess

DIRECTORY_TO_MAKE_BACKUP = "/home/rluna/tmp/bck_orig"
# the #strat# placeholder will be replaced by "daily", "weekly" or whatever
# after that will be the filename
BACKUP_DEST_DIR = "/home/rluna/tmp/bck_dest/#strat#/15guys.zip"
# you can put hiere your own command, but if you leave as "None", it will 
# use a plain zip file which is OK for a vast majority of cases
# if you want to use a backup command, the string #sourceDir#
# will be replace by the directory to backup and the string #destFile# 
# with the directory of the backup file
BACKUP_COMMAND=None
PRE_BACKUP_COMMAND = [ "systemctl", "stop", "minecraft" ] 
POST_BACKUP_COMMAND = [ "systemctl", "start", "minecraft" ]


EXIT_OK = 0
EXIT_ERROR = 255

MONDAY = 0
TUESDAY = 1
WEDNESDAY = 2 
THURSDAY = 3
FRIDAY = 4
SATURDAY = 5 
SUNDAY = 6


def setupLogger( logging_file : str ):
    with open( logging_file, 'rt', encoding='utf-8') as log_file_json: 
        loggingConfig = json.load( log_file_json )
    logging.config.dictConfig( loggingConfig )
    
    
def removeRootDir( str1 : str, prefix : str ) -> str : 
    if str1.startswith( prefix ) : 
        return str1[len(prefix)+1:]
    else: 
        return str1 

def zipdir( sourcePath : str, destFile : str ):
    '''make a zip file from sourcePath into a destFile
    '''
    with zipfile.ZipFile( destFile, 'w', compression = zipfile.ZIP_DEFLATED, compresslevel = 9 ) as zipf : 
        for root, dirs, files in os.walk( sourcePath, followlinks = True ) : 
            relativePath = removeRootDir( root, sourcePath )
            for file in files : 
                zipf.write( os.path.join( root, file ), os.path.join( relativePath, file ) )


def doBackup( sourcePath : str, destFile : str ):
    if BACKUP_COMMAND : 
        bckCommand = BACKUP_COMMAND
        bckCommand = bckCommand.replace( "#sourceDir#", sourcePath )
        bckCommand = bckCommand.replace( "#destFile#", destFile )
        print( 'yaveremos ' )
    else :
        zipdir( sourcePath, destFile )

def createDirIfNotExists( sourcePath : str ): 
    dirname = os.path.dirname( sourcePath )
    if not os.path.exists( dirname ): 
        os.makedirs( dirname )

def dailyStrategy( sourcePath : str, destFile : str, stratDir = "daily/" ):
    day = f"{datetime.datetime.today().day:02}"
    destFile = destFile.replace( "#strat#", stratDir + day )
    createDirIfNotExists( destFile )
    doBackup( sourcePath, destFile )

def weeklyStrategy( sourcePath : str, destFile : str, stratDir = "weekly/" ):
    weekDay = f"{datetime.datetime.today().weekday():02}"
    destFile = destFile.replace( "#strat#", stratDir + weekDay )
    createDirIfNotExists( destFile )
    doBackup( sourcePath, destFile )

def monthlyStrategy( sourcePath : str, destFile : str, stratDir = "monthly/" ):
    # monthly strategy will be executed only the day one of the month
    if datetime.datetime.today().day == 1 : 
        month = f"{datetime.datetime.today().month:02}"
        destFile = destFile.replace( "#strat#", stratDir + month )
        createDirIfNotExists( destFile )
        doBackup( sourcePath, destFile )
    else:
        logging.debug("no monthly strategy is done because it's not day one of the month")

def yearlyStrategy( sourcePath : str, destFile : str, stratDir = "yearly/" ):
    # yearly strategy will be executed only the day one of January
    if datetime.datetime.today().day == 1 and datetime.datetime.today().month == 1 : 
        year = f"{datetime.datetime.today().year:04}"
        destFile = destFile.replace( "#strat#", stratDir + year )
        createDirIfNotExists( destFile )
        doBackup( sourcePath, destFile )
    else:
        logging.debug("no monthly strategy is done because it's not day one of the month")

if __name__ == '__main__':
    if os.path.exists( "logging.json" ):
        setupLogger( "logging.json" )
    else : 
        # minimal logging config 
        logging.basicConfig( format='%(message)s', level=logging.ERROR )

    subprocess.run( PRE_BACKUP_COMMAND )
    for strategy in [ weeklyStrategy, monthlyStrategy ] :
        strategy( DIRECTORY_TO_MAKE_BACKUP, BACKUP_DEST_DIR )
    subprocess.run( POST_BACKUP_COMMAND )
        
    sys.exit( EXIT_OK )



