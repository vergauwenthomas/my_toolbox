#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Functions for formatting strings that will be printed.

@author: thoverga
"""

import sys
from termcolor import colored
from copy import copy


# =============================================================================
# Formatters
# =============================================================================

known_fmt_labels=['[tab]',
                  '[empty]',
                  '[columnsep]',
                  '[color]',
                  '[red]',
                  '[blue]',
                  '[cyan]',
                  '[green]',
                  f'[{None}]']




def _fmt_text_structure(text, max_print_line, no_list):
    column_sep = """/""" #keep it 1-character!
    #2. format into columns
    if '[columnsep]' in text:
        columized_text = ""
        ncols = text.count('[columnsep]') + 1
        colsize = int(max_print_line/ncols) - (ncols-1)
        
        curent_column=0
        
        
        for coltext in text.split('[columnsep]'):
            #compute identation size
            row_ident = coltext.count('[tab]')*4
            
            
            #Create a string without formatters, and the original
            # coltext=coltext.replace('[tab]', '    ').replace('[empty]', '')
            purecoltext = copy(coltext) #coltext must keep colorformatters!
            for lab in known_fmt_labels:
                purecoltext = purecoltext.replace(lab, '')
        
            if purecoltext == '':
                #empty row
                coltext = "".ljust(colsize)
            
            #check if pure col text is smaller than colsize
            elif len(purecoltext) <= colsize:
                #oke, now ljust to colsize
                coltext = coltext.replace(purecoltext, purecoltext.ljust(colsize-row_ident))
            else:
                #check if a list is displayed
                if ((purecoltext.count(',') > 1) & (not no_list)):
                    #format as list
                    formated_coltext = _fmt_list_text(text=purecoltext, 
                                             row_ident=row_ident,
                                             current_column=curent_column,
                                             colsize=colsize,
                                             column_sep=column_sep)
                    coltext = coltext.replace(purecoltext, formated_coltext)
                    
                else:
                     #truncate string
                     coltext = purecoltext[:(colsize-3)] + '...'
            
            # now ljust the text without ljusting the format labels
            columized_text += coltext + column_sep
            curent_column+=1
            
        text = columized_text[:-1] #drop last column sep
    
        
    text = text.replace('[tab]', '    ').replace('[empty]', '')
    return text
        
        
    


def _colorize_text(text, output_type):
    if '[color]' in text:
        colored_text = ''
        for textpart in text.split('[color]'):
    
            if textpart.startswith('[red]'):
                subtext = textpart.replace('[red]', '')
                trg_color='red'
             
            elif textpart.startswith('[blue]'):
                subtext = textpart.replace('[blue]', '')
                trg_color='blue'
            elif textpart.startswith('[cyan]'):
                subtext = textpart.replace('[cyan]', '')
                trg_color='cyan'
            elif textpart.startswith('[green]'):
                subtext = textpart.replace('[green]', '')
                trg_color='green'
            else:
                colored_text+=textpart
                continue
            
            if output_type == 'terminal':
                colored_text += colored(subtext, trg_color)
            elif output_type == 'html':
                colored_text += f'<{trg_color}>{subtext}</{trg_color}>'
            else:
                sys.exit(f'unknown output_type: {output_type}')
        
        text=colored_text
    
    return text





def _fmt_str(text, max_print_length=120,
             fill_space=True, output='terminal', no_list=False):
    """ format how text is printed for one hand side. """
    #1. format text
    text = _fmt_text_structure(text, max_print_length, no_list)
    
    #2. format colors 
    text=_colorize_text(text, output)
    return text






def _fmt_list_text(text, row_ident, current_column, column_sep, colsize, overflow_indent=2):
    """ Format a string representing a list over multiple lines. """
    chunks = text.split(',')
    chunked_text = ''
    
    
    #add first row
    first_row =f'{"".ljust(row_ident)}{text.split(",")[0]}'
    if len(first_row) > colsize:
        first_row = f'{first_row[:-3]}...'
    chunked_text += first_row + ',' + '\n'
    
    
    #each row (except the first) start with this prefix
    if current_column > 0:
        row_prefix =''.ljust(colsize) + column_sep + ''.ljust(row_ident+overflow_indent)
        
    else:
        row_prefix = ''.ljust(row_ident+overflow_indent)
    
    rowtext=''
    for chunk in chunks[1:]:
        # print(f'current rowbuckt: {row_bucket}')
        # #check if a single chunk can fit the row
        if (len(chunk) + row_ident + overflow_indent) > colsize:

            chunk=chunk[:(colsize-len(row_prefix)-4)]

            
        test_rowtext = f'{rowtext},{chunk}'
        if ((len(rowtext) + row_ident + overflow_indent <= colsize) &
            (len(test_rowtext) + row_ident + overflow_indent > colsize)):
            #current row reacht its maximum size
            chunked_text += row_prefix + rowtext + '\n' #add prefix
           
            #start new_row
            rowtext=""
         
        #append to row
        rowtext += chunk + ','

    #add the last row bucket
    chunked_text +=row_prefix + rowtext
    
    
    #add column spaces and spereator 
    
    return chunked_text


# =============================================================================
#  CSS/HTML
# =============================================================================
css_style = """<style type='text/css'>
html {
  font-family: Courier;
}
red {
  color: #ff0000;
}
green {
  color: #008b1e;
}
blue {
  color: #0000ff;
}
cyan {
  color: #00ffff;
}
</style>"""




        
