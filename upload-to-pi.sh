#!/bin/bash

piAddr="132.250.60.1"

# Get the directory containing the script
workingDir=$(dirname $(readlink -f $0))
echo "Working directory: $workingDir"

rsync -avz --progress $workingDir pi@$piAddr:~
