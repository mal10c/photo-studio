#!/bin/bash

piAddr="172.16.0.1"

# Get the directory containing the script
workingDir=$(dirname $(readlink -f $0))
echo "Working directory: $workingDir"

rsync -avz --progress $workingDir pi@$piAddr:~
