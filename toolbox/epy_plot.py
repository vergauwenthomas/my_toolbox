#!/usr/bin/env python3

#This script is a simple application based on the tutorial; http://www.umr-cnrm.fr/gmapdoc/meshtml/EPYGRAM1.2.15/tutorial/fields.html

import os,sys
import matplotlib.pyplot as plt
import argparse
import epygram
epygram.init_env()

from epy_modules.io_methods import read_file, read_2d_field, construct_filepath
epygram.config.activate_plugins
#epygram.config.noninteractive_backend = 'Qt5'


def make_regular_2d_plot(file, fieldname, level=None, backend='Qt5'):

	fullpath = construct_filepath(str(file))
	r = read_file(filepath=fullpath)
	field = read_2d_field(r, fieldname, level)

	epygram.config.noninteractive_backend = 'Qt5'
	fig, ax = field.cartoplot()

	plt.show()
	return



# if __name__ == "__main__":

#     parser = argparse.ArgumentParser(prog='plot_me',
#                                      formatter_class=argparse.RawDescriptionHelpFormatter,
#                                      description="""
# plot_me: a simple plotting tool for FA files using Epygram
# --------------------------------------------------------

# The following functionality is available:
#     * -f, --fieldname (make as spatial plot of this 2D field.)
#     * -l, --level(print out information of a FA file.)
#     * --backend (Qt5,  agg, ... )
#     """,

#                                      epilog='''
#                                                 @Thomas Vergauwen (thomas.vergauwen@meteo.be), credits to the Epygram-team. '''
#                                      )

#     parser.add_argument("file", help="FA filename, path of FA file or similar regex expression on filenames.", default='')  # argument without prefix

#     # Which mode arguments
#     parser.add_argument('-f', '--fieldname', help='Make as spatial plot of this 2D field (identifier can contain regex but must point to unique fieldname).',
#                         default="surftemperature")
#     parser.add_argument('-l', '--level', help='The level of the field, if None, the lowest level is plotted',
#                         default=None)
#     parser.add_argument('--backend', help='The plotting backend for cartoplot/mpl (use Qt5 for interactive --> needs Qt5 module)',
#                         default='Qt5')
#     args = parser.parse_args()
    
#     #typecast
#     if args.level is not None:
#         level = int(args.level)
#     else:
#         level=None
    
#     make_regular_2d_plot(file=str(args.file),
#                          fieldname=str(args.fieldname),
#                          level=level,
#                          backend=str(args.backend))
