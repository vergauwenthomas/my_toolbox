#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 16 09:06:16 2024

@author: thoverga
"""


import os
import sys
import shutil
import argparse

main_path = os.path.dirname(__file__)
sys.path.append(main_path)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(prog='PyFA-tool',
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description="""
PyFA: a tool for scientist working with ACCORD-FA files.
--------------------------------------------------------

The following functionality is available:
    * -p, --plot (make as spatial plot of an 2D field.)
    * -d, --describe (print out information of a FA file.)
    * -c, -- convert (convert a FA file to netCDF)""",

                                     epilog='''
                                                Add kwargs as you like as arguments. The position of these arguments is not of importance.
                                                These will be added to the plot functions (matplotlib).
                                                Example: .... vmin=288 vmax=294 cmap=?? ... '''
                                     )

    parser.add_argument("file", help="FA filename, path of FA file or similar regex expression on filenames.", default='')  # argument without prefix

    # Which mode arguments
    parser.add_argument('-p', '--plot', help='Make as spatial plot of a 2D field.',
                        default=True, action='store_true')
    parser.add_argument('-d', '--describe', help='Print out overview info of the FA file',
                        default=False, action='store_true')
    parser.add_argument('-c', '--convert', help='Convert to netCDF',
                        default=False, action='store_true')

    parser.add_argument('--whitelist', help='list of fieldnames to read (seperated by ,). If emtpy, all fields are read.',
                        default='')

    parser.add_argument("--combine_by_validate", help="If file is a regex expression, matching multiple FA files, they are combined on the validate dimension if True.",
                        default=True, action="store_true")

    default_2dfieldname = 'SFX.T2M'
    parser.add_argument("--field", help="fieldname", default=default_2dfieldname)
    parser.add_argument("--proj", help="Reproject to this crs (ex: EPSG:4326)", default='') #default no reproj

    parser.add_argument('kwargs', help='Extra arguments passed to the plot function. (must follow directly the file argurment, and as last arg)', nargs='*')

    args = parser.parse_args()


    #the cli arguments are now attributes of args


    pass

