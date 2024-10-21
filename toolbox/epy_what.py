#!/usr/bin/env python3

import argparse
import os
import epygram

from epy_modules.io_methods import construct_filepath

def run_epygram_what(filepath):
    
    filepath = construct_filepath(filepath)

    assert os.path.isfile(filepath), f'{filepath} not found.'
    
    epygram.init_env()

    data = epygram.formats.resource(filepath, 'r')
    data.what() #Print all info




# if __name__ == "__main__":

#     parser = argparse.ArgumentParser(prog='What ??',
#                                      formatter_class=argparse.RawDescriptionHelpFormatter,
#                                      description="""
# What ??: Print out an overview of what is contained by an FA file
# -------------------------------------------------------------------

# There are no special options for this script.
# """
# )

#     parser.add_argument("file", help="FA filename, path of FA file or similar regex expression on filenames.", default='')  # argument without prefix

#     args = parser.parse_args()

#     # Run the application
#     run_epygram_what(str(args.file))



