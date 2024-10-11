#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 11 17:41:54 2024

@author: thoverga
"""
import sys
import nested_diff
from termcolor import colored


# =============================================================================
# Hardcode settings
# =============================================================================

column_char = '''|'''

# =============================================================================
# Main
# =============================================================================

def _print_diff(namelist_a, namelist_b, diffdict, max_print_length=120):
    
    #Print header
    colsize = int((max_print_length-1)/2)
        
    lstr = str(namelist_a.name.upper().center(colsize))
    rstr = str(namelist_b.name.upper().center(colsize))
    
    header=f'{lstr}{column_char}{rstr}\n {"-"*max_print_length}\n'
    
    print(header)
    
    for Groupname, groupdiff in diffdict['D'].items():
        _printgroup(namleft=namelist_a,
                    namright=namelist_b,
                    Groupname=Groupname,
                    groupdiff = groupdiff,
                    max_print_length=max_print_length,
                    diffvalue_color='red',
                    missing_in_other='cyan')
          
def _compute_deepdiff(namelist_a, namelist_b):
    return nested_diff.diff(namelist_a.namelist, namelist_b.namelist)

        
        
# =============================================================================
# Methods
# =============================================================================




def _printgroup(namleft, namright, Groupname, groupdiff, max_print_length=120,
                diffvalue_color='red', missing_in_other='cyan',
                ):
    
    colsize = int((max_print_length-1)/2)
    #print groupname left
    if Groupname in namleft.namelist.keys():
        rgroupcolor=None #print in default colors
        lgroupname=Groupname
    else:
        rgroupcolor=missing_in_other #print in default colors
        lgroupname=''

    
    if Groupname in namright.namelist.keys():
        lgroupcolor=None #print in default colors
        rgroupname=Groupname
    else:
        lgroupcolor=missing_in_other #print in default colors
        rgroupname=''
        
    #print line
    print(_fmt_str(lgroupname, lgroupcolor),column_char, _fmt_str(rgroupname, rgroupcolor) )
   
    
    # go trough the values
    for difftype, setdif in groupdiff.items():
        if difftype == 'U':
            #All group settings are unchanged!
            if setdif == {}:
                print(_fmt_str(text=setdif, N_ident=1), column_char, _fmt_str(text=setdif, N_ident=1))
                # print(f'{pindent + str(setdif)}'.ljust(colsize),'|', f'{pindent + str(setdif)}'.ljust(colsize))
            else:
                for lsetname in setdif.keys():
                    value = setdif[lsetname]
                    if isinstance(value, list):
                        value = value #TODO 
                    #print setting names
                    print(_fmt_str(text=f'{lsetname}: {value}', N_ident=1), column_char, _fmt_str(text=f'{lsetname}: {value}', N_ident=1))
                   
            
        
        elif difftype == 'R':
            #all group values do not exist in right
            if setdif == {}:
                print(_fmt_str(text=setdif, N_ident=1, textcolor=missing_in_other), column_char, _fmt_str(text=""))
                
            else:
                for lsetname in setdif.keys():
                    value = setdif[lsetname]
                    if isinstance(value, list):
                        value = value #TODO 
                    
                    #print setting names
                    print(_fmt_str(text=f'{lsetname}: {value}', N_ident=1, textcolor=missing_in_other), column_char, _fmt_str(text="", N_ident=1))
                    # print(colored(f'{pindent + lsetname}: {value}'.ljust(colsize), missing_in_other), '|')
        
        elif difftype == 'A':
            #all group values do not exist in left
            if setdif == {}:
                print(_fmt_str(text=""), column_char,_fmt_str(text=setdif, N_ident=1, textcolor=missing_in_other))
                # print(''.ljust(colsize), '|', colored(f'{pindent + str(setdif)}'.ljust(colsize), missing_in_other))
            else:
                for rsetname in setdif.keys():
                    value = setdif[rsetname]
                    if isinstance(value, list):
                        value = value #TODO 
                    
                    #print setting names
                    print( _fmt_str(text="", N_ident=1), column_char, _fmt_str(text=f'{rsetname}: {value}', N_ident=1, textcolor=missing_in_other))
                    # print(''.ljust(colsize), '|', colored(f'{pindent + rsetname}: {value}'.ljust(colsize), missing_in_other))
        
        elif difftype == 'D':
            #(some) values are different
            for setname in setdif.keys():
                if 'U' in setdif[setname].keys():
                    ltext = f"{setname}: {setdif[setname]['U']}"
                    rtext = f"{setname}: {setdif[setname]['U']}"
                    
                    print(_fmt_str(text=ltext, N_ident=1),
                          column_char,
                          _fmt_str(text=rtext, N_ident=1))
                    
             
                elif 'R' in setdif[setname].keys():
                    #setting not defined in right
                    ltext = f"{setname}: {setdif[setname]['R']}"
                    rtext = ''
                    
                    print(_fmt_str(text=ltext, N_ident=1, textcolor=missing_in_other),
                          column_char,
                          _fmt_str(text=rtext, N_ident=1))
                    
                elif 'A' in setdif[setname].keys():
                    ltext=''
                    rtext = f"{setname}: {setdif[setname]['A']}"
                    print(_fmt_str(text=ltext, N_ident=1),
                          column_char,
                          _fmt_str(text=rtext, N_ident=1, textcolor=missing_in_other))
              
                elif 'N' in setdif[setname]:
                    # #values are different
                    lvalue =  setdif[setname]['O']
                    rvalue = setdif[setname]['N']
                
                    print(_fmt_str(text=f'{setname}: {lvalue}', N_ident=1, textcolor=diffvalue_color),
                          column_char,
                          _fmt_str(text=f'{setname}: {rvalue}', N_ident=1, textcolor=diffvalue_color))
                    pass
                else:
                    sys.exit(f'Not forseen difftype : {setname} in {setdif}')
                    

        else:
            sys.exit(f'Not forseen difftype : {difftype}')





            
            
# =============================================================================
# Formatters
# =============================================================================
       

def _fmt_str(text, textcolor=None, N_ident=0, max_print_length=120, ident='    '):
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
    displ_str = displ_str.ljust(colsize)
    return colored(displ_str, textcolor)




def _fmt_list_text(text, colsize, overflow_indent=2):
    """ Format a string representing a list over multiple lines. """
    chunks = text.split(',')
    chunked_text = ''
    row_bucket=''
    for chunk in chunks:
        #check if a single chunk is valid
        if len(chunk) > colsize:
            chunk = f'{chunk[:(colsize-(4 + len(overflow_indent)))]}...,'
        
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
