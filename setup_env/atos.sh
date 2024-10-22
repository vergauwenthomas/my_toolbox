#!/bin/bash


CURDIR=$PWD
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

echo "---- Setup of toolbox environment ---- "

#clean env
deactivate #clean conda/python
module purge #clean modules

#load modules
export PATH="$HOME/.local/bin:$PATH"
module load python3/3.10.10-01
module load prgenv/intel #this can be change, is needed for ecmwf toolbox

#for using PYfa
module load gdal/3.6.2
module load git/2.39.1
module load rstudio


#install environment
cd ${SCRIPT_DIR}/..
#develop phase:
poetry update
poetry install --with pyfa --no-root #create a poetry environment (but keep the package editable)

#non-develop
#poetry install

#activate env
source $(poetry env info --path)/bin/activate


cd $CURDIR
