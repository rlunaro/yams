#!/usr/bin/python
'''
Copyright 2021, superman_ha_muerto@yahoo.com

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
import logging.config
import os
import os.path
import sys
import re
import requests 
import json 
import subprocess
import time

JAVA_HOME = ""
JAVA = f"{JAVA_HOME}/bin/java"

MINECRAFT_INSTALL = "/home/rluna/machines/minecraft"
MINECRAFT_JAR = f"{MINECRAFT_INSTALL}/minecraft.jar"
PIDFILE = f"{MINECRAFT_INSTALL}/pidfile"

VERSION_MANIFEST_URL = 'https://launchermeta.mojang.com/mc/game/version_manifest.json'
NEW_FILE_TEMPLATE = 'minecraft_server.#version#.jar'

def setupLogger( logging_file : str ):
    with open( logging_file, 'rt', encoding='utf-8') as log_file_json: 
        loggingConfig = json.load( log_file_json )
    logging.config.dictConfig( loggingConfig )

def install_last_version_if_needed( install_dir : str, version_manifest_url : str, destination_symlink : str ): 
    logging.info("checking if there is need for new versions to install...")
    last_installed_version = get_last_installed_version( install_dir ) 
    version_manifest_json = get_version_manifest( version_manifest_url )
    latest_available_version = parse_version( version_manifest_json['latest']['release'] )
    logging.info( f"installed version is {last_installed_version}. Last available version is {latest_available_version}")
    if latest_available_version > last_installed_version : 
        last_available_version_str = version_manifest_json['latest']['release']
        logging.info(f"proceeding to install version {last_available_version_str}")
        destination_filename = NEW_FILE_TEMPLATE.replace('#version#', last_available_version_str )
        download_new_version( version_manifest_json, last_available_version_str, destination_filename )
        create_symlink( destination_symlink, destination_filename )
    else: 
        logging.info("no need to install anything")

def get_last_installed_version( install_dir : str ):
    versionFiles = [ x for x in os.listdir( install_dir ) if re.match( "minecraft_server\\.[0-9\\.]+\\.jar", x ) ]
    lastVersion = [0,0,0]
    for versionFile in versionFiles : 
        currentVersion = parse_version( versionFile )
        if lastVersion < currentVersion : 
            lastVersion = currentVersion 
    return lastVersion

def parse_version( file : str ):
    result = [0, 0, 0]
    try: 
        match1 = re.search( '(?i)([0-9\\.]+)', file )
        if len(match1.groups()) > 0 :
            match2 = re.search( '(?i)([0-9]+)\\.?([0-9]*)\\.?([0-9]*)', match1.group(1) )
            if len( match2.groups()) > 0 and len(match2.group(1)) > 0 : 
                result[0] = int(match2.group(1))
            if len( match2.groups()) > 1 and len(match2.group(2)) > 0 :
                result[1] = int(match2.group(2))
            if len( match2.groups()) > 2 and len(match2.group(3)) > 0 :
                result[2] = int(match2.group(3))
    except Exception as ex: 
        logger.error( "Error parsing version from file %s", file )
        logger.error( ex ) 
    return result

def get_version_manifest( version_manifest_url : str ):
    response = requests.get( VERSION_MANIFEST_URL )
    version_manifest_json = json.loads( response.content )
    return version_manifest_json 

def download_new_version( version_manifest_json, version_id : str, destination_filename : str ):
    version_data = get_version_data_by_id( version_manifest_json, version_id )
    download_url = get_download_url_for( version_data['url'], 'server' )
    logging.info( f"downloading new version {version_id} from {download_url}" )
    download_file( download_url, destination_filename )
    
def get_version_data_by_id( version_manifest_json : dict, version_id : str ):
    version_data = None
    for version_record in version_manifest_json['versions'] : 
        if version_record["id"] == version_id : 
            version_data = version_record 
            break
    return version_data 

def get_download_url_for( download_url : str, client_or_server : str ):
    logging.info( f"getting specific version info from {download_url}")
    response = requests.get( download_url ) 
    response_json = json.loads( response.content )
    server_download_url = response_json['downloads'][client_or_server]['url']
    return server_download_url

def download_file( download_url : str, filename : str ):
    logging.debug( f"downloading new version of server from {download_url}")
    response = requests.get( download_url )
    with open( filename, "wb" ) as server_file : 
        server_file.write( response.content )

def create_symlink( sym_link_name : str, dest_file : str ):
    if os.path.exists( sym_link_name ): 
        os.remove( sym_link_name )
    os.symlink( dest_file, sym_link_name )

def safety_checks( ):
    ''' 
    do some checks in the setup, to be sure that the 
    enviroment is safe to start the server 
    '''
    ok = True
    logging.info( "checking that directory %s exists...", MINECRAFT_INSTALL )
    if not os.path.isdir( MINECRAFT_INSTALL ): 
        logging.error( "directory MINECRAFT_INSTALL does not exist" )
        logging.error( "current value is %s", MINECRAFT_INSTALL )
        ok = False
    if not os.path.isfile( JAVA ): 
        logging.error( "java executable not found" )
        logging.error( "you can configure it by editing the variable JAVA_HOME")
        logging.error( "current value is %s", JAVA )
        ok = False
    return ok

def save_process_id( pid : str ):
    with open( PIDFILE, "wt" ) as pidfile: 
        pidfile.write( str( pid ) )

def read_process_id( ):
    with open( PIDFILE, "rt" ) as pidfile: 
        return pidfile.read()

     
if __name__ == '__main__':
    if os.path.exists( "logging.json" ):
        setupLogger( "logging.json" )
    else : 
        # minimal logging config 
        logging.basicConfig( format='%(message)s', level=logging.ERROR )
        
    if len( sys.argv ) == 1: 
        print( f"Usage: {sys.argv[0]} [setup|start|stop]" )
        sys.exit( -1 )
        
    command = sys.argv[1]

    if not safety_checks() : 
        sys.exit( -2 )
    
    try:
        install_last_version_if_needed( MINECRAFT_INSTALL, VERSION_MANIFEST_URL, MINECRAFT_JAR )
    except Exception as ex: 
        logging.error( "Error in the checking of new server version: " )
        logging.error( "This could be because of a temporary server down or an internet glitch")
        logging.error( "However, you should check if the message appears every time the server start")

    if command == "start" : 
        logging.info( "Starting minecraft server...")
        with open("console.log", "at", encoding="UTF-8") as output: 
            process = subprocess.Popen( [JAVA,
                            "-Xms1300M",
                            "-Xmx1500M",
                            "-Djava.awt.headless=true",
                            "-jar",
                            MINECRAFT_JAR,
                            "nogui"], 
                            stdout = output, 
                            stderr = subprocess.STDOUT ) 
        
        save_process_id( process.pid )
        logging.info( "done" )

    if command == "stop" : 
        logging.info( "Stopping minecraft server...")
        pid_value = read_process_id()
        subprocess.run( [ "kill", pid_value ] )
        time.sleep( 4 )
        subprocess.run( [ "kill", "-9", pid_value ] )
        logging.info( "done" )
        
    sys.exit( 0 )
    
