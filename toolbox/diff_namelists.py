#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 11 17:41:54 2024

@author: thoverga
"""
import sys
import nested_diff


from .string_formatters import _fmt_str


# =============================================================================
# Hardcode settings
# =============================================================================

column_char = '''|'''

# =============================================================================
# Main
# =============================================================================

def _print_diff(namelist_a, namelist_b, diffdict, max_print_length=120, 
                html_formatted=False):
    
    
    #Print header
    colsize = int((max_print_length-1)/2)
        
    lstr = str(namelist_a.name.upper().center(colsize))
    rstr = str(namelist_b.name.upper().center(colsize))
    
    header=f'{lstr}{column_char}{rstr}\n {"-"*max_print_length}\n'
    
    groupstr=''
    
    if html_formatted:
        output_format='html'
        diffvalue_col ='red'
        missing_in_other_col='blue'
    else:
        output_format='terminal'
        diffvalue_col ='red'
        missing_in_other_col='cyan'
        
    
    for Groupname, groupdiff in diffdict['D'].items():
        groupstr +=  _printgroup(namleft=namelist_a,
                                namright=namelist_b,
                                Groupname=Groupname,
                                groupdiff = groupdiff,
                                max_print_length=max_print_length,
                                diffvalue_color=diffvalue_col,
                                missing_in_other=missing_in_other_col,
                                output_format=output_format)
        
    if html_formatted:
        html_lines=[]
        html_lines.append(f'<p><b>{header}</b>') #write header in bold
        for line in groupstr.split('\n'): #iterate over every line
            html_lines.append(f'<pre>' + line + '<br /></pre>' + '\n')
        
        html_lines.append('</p>')
        return html_lines
    else:
        
        return header + groupstr
          
def _compute_deepdiff(namelist_a, namelist_b):
    return nested_diff.diff(namelist_a.namelist, namelist_b.namelist)

        
        
# =============================================================================
# Methods
# =============================================================================



def _printgroup(namleft, namright, Groupname, groupdiff, max_print_length=120,
                diffvalue_color='red', missing_in_other='cyan', output_format='terminal'
                ):
    
    groupstr = ""
    if Groupname == 'FPVALH(0:87)':
         print('gevonden')
    
    #option 1: groupname knonwn by left and right
    if((Groupname in namleft.namelist.keys()) &
       (Groupname in namright.namelist.keys())):
        
        groupstr += _fmt_str(f'{Groupname}[columnsep]{Groupname}',
                             max_print_length=max_print_length,
                             output=output_format)+'\n'
    
    #option 2: groupname known by left not by right
    elif((Groupname in namleft.namelist.keys()) &
       (Groupname not in namright.namelist.keys())):
        groupstr += _fmt_str(f'[color][{missing_in_other}]{Groupname}[color][columnsep][empty]',
                             max_print_length=max_print_length,
                             output=output_format)+'\n'
    
    #option 3: groupname knonw by rigth not by left
    elif((Groupname not in namleft.namelist.keys()) &
       (Groupname in namright.namelist.keys())):
        
        
        
        groupstr += _fmt_str(f'[empty][columnsep][color][{missing_in_other}]{Groupname}[color]',
                             max_print_length=max_print_length,
                             output=output_format)+'\n'
    
    else:
        sys.exit('Unforseen situation.')
 
        
    
    # go trough the values
    for difftype, setdif in groupdiff.items():
        if difftype == 'U':
            #All group settings are unchanged!
            if setdif == {}:
                groupstr +=  _fmt_str('[tab]{}[columnsep][tab]{}',
                                     max_print_length=max_print_length,
                                     output=output_format)+'\n'
            else:
                for lsetname in setdif.keys():
                    value = setdif[lsetname]
                    if isinstance(value, list):
                        value = value #TODO 
                    #print setting names
                    groupstr += _fmt_str(text=(f'[tab]{lsetname}: {value}[columnsep]' + 
                                               f'[tab]{lsetname}: {value}'),
                                         max_print_length=max_print_length,
                                         output=output_format)+'\n'
                    
                   
        elif difftype == 'R':
            #all group values do not exist in right
            if setdif == {}:
                groupstr += _fmt_str(text=(f'[tab][color][{missing_in_other}]{setdif}[color][columnsep]' + 
                                           '[empty]'),
                                     max_print_length=max_print_length,
                                     output=output_format)+'\n'
                
            else:
                for lsetname in setdif.keys():
                    value = setdif[lsetname]
                    if isinstance(value, list):
                        value = value #TODO 
                    
                    #print setting names
                    groupstr += _fmt_str(text=(f'[tab][color][{missing_in_other}]{lsetname}: {value}[color][columnsep]' +
                                   '[empty]'),
                             max_print_length=max_print_length,
                             output=output_format)+'\n'

                  
        elif difftype == 'A':
            #all group values do not exist in left
            if setdif == {}:
                groupstr += _fmt_str(text=('[empty][columnsep]' +
                                           f'[tab][color][{missing_in_other}]{setdif}[color]'),
                             max_print_length=max_print_length,
                             output=output_format)+'\n'

                for rsetname in setdif.keys():
                    value = setdif[rsetname]
                    if isinstance(value, list):
                        value = value #TODO 
                        
                    groupstr += _fmt_str(text=('[empty][columnsep]' +
                                               f'[tab][color][{missing_in_other}]{rsetname}: {value}[color]'),
                                 max_print_length=max_print_length,
                                 output=output_format)+'\n'
                    
        elif difftype == 'D':
            #(some) values are different
            for setname in setdif.keys():
                if 'U' in setdif[setname].keys():
                    value = setdif[setname]['U']
               
                    groupstr += _fmt_str(text=(f'[tab]{setname}: {value}[columnsep]'+
                                               f'[tab]{setname}: {value}'),
                                 max_print_length=max_print_length,
                                 output=output_format)+'\n'

                elif 'R' in setdif[setname].keys():
                    #setting not defined in right
                    lvalue=setdif[setname]['R']

                    groupstr += _fmt_str(text=(f'[tab][color][{missing_in_other}]{setname}: {lvalue}[color][columnsep]'+
                                               '[empty]'),
                                 max_print_length=max_print_length,
                                 output=output_format)+'\n'

                elif 'A' in setdif[setname].keys():
                    rvalue=setdif[setname]['A']

                    groupstr += _fmt_str(text=('[empty][columnsep]'+
                                               f'[tab][color][{missing_in_other}]{setname}: {rvalue}[color]'),
                                 max_print_length=max_print_length,
                                 output=output_format)+'\n'
  
                elif 'N' in setdif[setname]:
                    # #values are different
                    lvalue =  setdif[setname]['O']
                    rvalue = setdif[setname]['N']
                    groupstr += _fmt_str(text=( f'[tab][color][{diffvalue_color}]{setname}: {lvalue}[color][columnsep]' +
                                               f'[tab][color][{diffvalue_color}]{setname}: {rvalue}[color]'),
                                 max_print_length=max_print_length,
                                 output=output_format)+'\n'

                else:
                    sys.exit(f'Not forseen difftype : {setname} in {setdif}')
                    

        else:
            sys.exit(f'Not forseen difftype : {difftype}')

    return groupstr



    