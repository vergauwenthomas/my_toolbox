#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 10:04:23 2024

@author: thoverga
"""
import argparse
import os
import sys
from pathlib import Path

# =============================================================================
# import toolbox
# =============================================================================

sys.path.insert(0, str(Path(__file__).parents[1]))
import toolbox as tb
# =============================================================================
# CLI methods
# =============================================================================

def _apply_namlist_diff(file_a, file_b, target_html, max_textlength):
    nam_a =tb.Namelist(file_a, file_a)
    nam_b = tb.Namelist(file_b, file_b)
    
    if not bool(target_html):
        trg_html = None
    else:
        trg_html = target_html
    
    
    diffstr = tb.print_diff(namelist_a=nam_a,
                            namelist_b = nam_b,
                            write_html=trg_html,
                            max_text_lengt=max_textlength)
    if not bool(target_html):
        print(diffstr)
    
    
def _explain_namelist(file, target_html, max_text_length):
    namlist =tb.Namelist(file, file)
    
    if not bool(target_html):
        trg_html = None
    else:
        trg_html = target_html
    print('trg html: ', trg_html)
    explainstr = namlist.explain(write_html=trg_html,
                                 max_text_length=max_text_length)
    if not bool(target_html):
        print(explainstr)
    
    
    
def _update_local_namelist_def():
    tb._get_name_def_from_online()
    


# =============================================================================
# Helpers
# =============================================================================

def _get_file(filearg):
    #check if filearg is a path
    if os.path.exists(filearg):
        return filearg
    
    #check if this is the filename
    if (os.path.isfile(os.path.join(os.getcwd(), filearg))):
        return os.path.join(os.getcwd(), filearg)
    
    else:
        sys.exit(f'{filearg} is not a file.')

# =============================================================================
# Parser and main
# =============================================================================

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='toolbox',
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description=f"""
A toolbox for working with NWP/Climate model output.
--------------------------------------------------------

 Note: The used defenitions are define in this online sheet: https://docs.google.com/spreadsheets/d/1qvwju807GBhnCQ5TOdgdqjIMPUWumCi9dEs1XwYfjvU/edit?usp=sharing
    """,

                                     epilog=f'toolbox version: {tb.__version__}'
                                     )
        
    
    # =============================================================================
    # Namelist methods     
    # =============================================================================
    
    default_printlength=110
    # arguments that require a fileB as input
    subparsers = parser.add_subparsers(help='sub-commands help')
    
    # Print difference between two namelists
    sp = subparsers.add_parser('diff', help='Print out the difference between two namelist.')
    sp.set_defaults(cmd = 'diff')
    sp.add_argument("file A", help="filename, path or similar regex expression of namlist A (presented on the left side).", default='')  # argument without prefix
    sp.add_argument("file B", help="filename, path or similar regex expression of namlist B (presented on the right side) ", default='')  # argument without prefix
    sp.add_argument('-to_file', help='Diff output is writen to a (HTML) file. Give the filename',
                    default='')
        
    sp.add_argument('-print_length',
                    help=f'The maximum number of characters to print on one line. The default is {default_printlength}.',
                    default=default_printlength)
    
    
    # Explain a namelist
    sp = subparsers.add_parser('explain', help='Print out the namelist and explain the settings.')
    sp.set_defaults(cmd = 'explain')
    sp.add_argument("file", help="filename, path or similar regex expression of the namelist to explain.", default='')  # argument without prefix
    sp.add_argument('-to_file', help='Explain-output is writen to a (HTML) file. Give the filename',
                    default='')
        
    sp.add_argument('-print_length',
                    help=f'The maximum number of characters to print on one line. The default is {default_printlength}.',
                    default=default_printlength)
  

    #Update the explanations of settings using the online table  
    sp = subparsers.add_parser('Update_defenitions', help='Update the local copy of the namelist defenitions from the online google sheet.')
    sp.set_defaults(cmd = 'update_def')

    
    # =============================================================================
    #  FA methods
    # =============================================================================
    if tb._with_epygram:
        #WHAT
        sp = subparsers.add_parser('what', help='Print out an overview of an FA file.')
        sp.set_defaults(cmd = 'what')
        sp.add_argument("file", help="filename, path or similar regex expression of the FA file to explain.", default='')  # argument without prefix
        
        #WHAT
        sp = subparsers.add_parser('plot', help='Make a 2D plot of a field of an FA file.')
        sp.set_defaults(cmd = 'plot')
        sp.add_argument("file", help="filename, path or similar regex expression of the FA file to explain.", default='')  # argument without prefix
        sp.add_argument("fieldname", help="The name of the field to plot.", default='')  # argument without prefix
        sp.add_argument('-l', '--level', help='The level of the field, if None, the lowest level is plotted',
                            default=None)
        sp.add_argument('--backend', help='The plotting backend for cartoplot/mpl (use Qt5 for interactive --> needs Qt5 module)',
                            default='Qt5')
        



    # =============================================================================
    # General Methods    
    # =============================================================================


    args = vars(parser.parse_args())
    if not bool(args):
        parser.print_help()
        sys.exit()

    if args['cmd'] == 'diff': 
        _apply_namlist_diff(file_a = str(_get_file(args['file A'])),
                            file_b = str(_get_file(args['file B'])),
                            target_html = str(args['to_file']),
                            max_textlength = int(args['print_length']))

    if args['cmd'] == 'explain': 
        _explain_namelist(file=_get_file(args['file']),
                          target_html = str(args['to_file']),
                          max_text_length = int(args['print_length']))
                          
    if args['cmd'] == 'update_def': 
        _update_local_namelist_def()
        
    if args['cmd'] == 'what': 
        tb.run_epygram_what(_get_file(args['file']))
        
    if args['cmd'] == 'plot': 
        #typecast
        if args.level is not None:
            level = int(args.level)
        else:
            level=None
        
        tb.make_regular_2d_plot(file=_get_file(args['file']),
                             fieldname=str(args['file']),
                             level=level,
                             backend=str(args['backend']))
        
       
       
        
        
        
        