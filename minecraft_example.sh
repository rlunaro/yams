#!/bin/bash
#
# minecraft.sh
#
#

PYTHONIOENCODING=UTF-8

if [ -z "$minecraft_home" ] 
then  
    minecraft_home="PUT-HERE-THE-HOME-OF-YOUR-APPLICATION"
    PYTHONPATH="$minecraft_home;$minecraft_home/src"
    PYTHON_HOME="$minecraft_home"
    PATH="$PYTHON_HOME/bin:$PATH"
    PYTHON_EXE="$PYTHON_HOME/bin/python"
fi

"$PYTHON_EXE" -u "$minecraft_home/main.py" \
--config="config.yaml" \
--logging="logging.json" \
$1 $2 $3 $4 $5



