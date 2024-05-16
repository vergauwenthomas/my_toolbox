#!/usr/bin/env python3

import argparse
import os
import epygram

parser = argparse.ArgumentParser(description='EPYGRAM plotting as a python wrapper')
parser.add_argument("file", help="FA filename of path.", default='') #argument without prefix

args = parser.parse_args()

fa_file = str(args.file)
assert os.path.isfile(fa_file), f'{args.file} not found.'


epygram.init_env()

data = epygram.formats.resource(fa_file, 'r')
data.what() #Print all info
