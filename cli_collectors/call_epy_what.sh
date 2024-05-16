#!/bin/bash

file=$1
echo $file
cur_loc=`pwd`
filepath=${cur_loc}/${file}

EPY_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )


python3 ${EPY_DIR}/epy_what.py ${filepath}

