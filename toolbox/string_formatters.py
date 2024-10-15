#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Functions for formatting strings that will be printed.

@author: thoverga
"""

import sys
from termcolor import colored


# =============================================================================
# Formatters
# =============================================================================
       

    


def _fmt_str(text, textcolor=None, N_ident=0, max_print_length=120, ident='    ',
             fill_column=True, output='terminal'):
    """ format how text is printed for one hand side. """
    colsize = int((max_print_length-1)/2)
    displ_str = f'{str(ident)*N_ident}{text}'
    
    #check colsize is exceeded (typically by lists)
    if len(displ_str) > colsize:
        if text.count(',') > 0: #assume comma only used in str representation of lists
           displ_str = _fmt_list_text(displ_str,
                                      colsize-2)
        else:
            displ_str = f'{displ_str[:(colsize-3)]}...'
    
    if fill_column:
        displ_str = displ_str.ljust(colsize)
    
    if output == 'terminal':
        displ_str = colored(displ_str, textcolor)
    elif output == 'html':
        displ_str=_fmt_html_str(text=displ_str, color=textcolor)    
    return displ_str

def _fmt_list_text(text, colsize, overflow_indent=2):
    """ Format a string representing a list over multiple lines. """
    chunks = text.split(',')
    chunked_text = ''
    row_bucket=''
    for chunk in chunks:
        #check if a single chunk is valid
        if len(chunk) > colsize:
            chunk = f'{chunk[:(colsize-(4 + overflow_indent))]}...,'
        
        test_row_bucket = f'{row_bucket},{chunk}'
        if ((len(row_bucket) <= colsize) &
            (len(test_row_bucket) > colsize)):
            #flush bucket
            chunked_text += row_bucket + '\n' + ' '*overflow_indent
            row_bucket = ''
        
        row_bucket += chunk+',' 
    
    #add the last row bucket
    chunked_text += row_bucket
    return chunked_text



# =============================================================================
#  CSS/HTML
# =============================================================================
def _fmt_html_str(text, color):
    if color is None:
        #no color
        return f'{text}'
    elif color == 'red':
        return f'<r>{text}</r>'
    elif color == 'blue':
        return f'<b>{text}</b>'
    elif color == 'green':
        return f'<g>{text}</g>'   
    elif color == 'cyan':
        return f'<c>{text}</c>'
    else:
        sys.exit(f'{color} is not a defined css color.')
        
        
css_style = """<style type='text/css'>
html {
  font-family: Courier;
}
r {
  color: #ff0000;
}
g {
  color: #00ff00;
}
b {
  color: #0000ff;
}
c {
  color: #00ffff;
}
</style>"""





        
