#!/bin/bash


echo "---- Setup of Deode-Prototype-env ---- "

#clean env
deactivate #clean conda/python
module purge #clean modules

#load modules
export PATH="$HOME/.local/bin:$PATH"
module load python3/3.10.10-01

#install environment
cd ..
poetry install --no-root #create a poetry environment (but keep the package editable)

#activate env
source $(poetry env info --path)/bin/activate
