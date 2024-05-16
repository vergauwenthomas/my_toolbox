#!/usr/bin/env python3

import argparse
import os
import epygram
def run_epygram_what(filepath):
    
    filepath = construct_filepath(filepath)

    assert os.path.isfile(filepath), f'{filepath} not found.'
    
    epygram.init_env()

    data = epygram.formats.resource(filepath, 'r')
    data.what() #Print all info
    
def construct_filepath(file_arg):
    """ Checks if the file is relative defined and if so add the pwd. """
    if str('/') not in file_arg:
        #relative path
        return os.path.join(os.getcwd(), file_arg)
    else:
        return file_arg



if __name__ == "__main__":

    parser = argparse.ArgumentParser(prog='What ??',
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description="""
What ??: Print out an overview of what is contained by an FA file
-------------------------------------------------------------------

There are no special options for this script.
"""
)

    parser.add_argument("file", help="FA filename, path of FA file or similar regex expression on filenames.", default='')  # argument without prefix

    args = parser.parse_args()

    # Run the application
    run_epygram_what(str(args.file))



