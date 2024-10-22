#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 10 14:21:29 2024

@author: thoverga
"""
import pprint
import sys
import os
from pathlib import Path


sys.path.insert(0, Path(__file__).parent)

workdir = Path(__file__).parent

import toolbox as tb



#%%





file1 = "/home/thoverga/Desktop/namelist_e927_surf_deode"
nam_deode =tb.Namelist(file1, 'deode_e927_surf')



file2 = "/home/thoverga/Desktop/namlist_e927_kmi"
nam_kmi = tb.Namelist(file2, 'RMI_e927')


nam_kmi.explain(write_html='testhtml.html')


# test = tb.print_diff(nam_deode,
#             nam_kmi,
#             write_html=None,
#             # write_html='test.html',
#             )
# print(test)

#%%
from copy import copy
from toolbox.string_formatters import known_fmt_labels

teststring = '[tab][color][cyan]YTKEddddd_NL%NREQIN: 0[color][columnsep][empty]'

# printtest = _fmt_str(teststring, max_print_length=120)
from termcolor import colored
import re





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
            
            # print(f'  --> without labels: {purecoltext}')
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
                    print('format as list !!!')
                    formated_coltext = _fmt_list_text(text=purecoltext, 
                                             row_ident=row_ident,
                                             current_column=curent_column,
                                             colsize=colsize,
                                             column_sep=column_sep)
                    coltext = coltext.replace(purecoltext, formated_coltext)
                    
                else:
                     #truncate string
                     # print('truncate !!')
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
            print('Trucate element! ')
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



def _fmt_str(text, max_print_length=120,
             fill_space=True, output='terminal', no_list=False):
    """ format how text is printed for one hand side. """
    print(f' String to format: \n{text}')
    #1. format text
    text = _fmt_text_structure(text, max_print_length, no_list)
    
    #2. format colors 
    text=_colorize_text(text, output)
    
    #3. set identation
    displ_str = text

    print(displ_str)
    return displ_str


key='FPVBH(0:87)'
value =  ['0.0000000000',
 '0.0000000000',
 '0.0000000000',
 '0.0000000000',
 '0.0000000000',
 '0.0000000000',
 '0.0000000000',
 '0.0000000000',
 '0.0000000000',
 '0.0000000000',
 '0.0000000000',
 '0.0000000000',
 '0.0000853058',
 '0.0004494320',
 '0.0012157032',
 '0.0024971551',
 '0.0044046099',
 '0.0070479403',
 '0.0105358929',
 '0.0149753307',
 '0.0204701548',
 '0.0271200160',
 '0.0350188823',
 '0.0442535121',
 '0.0549018829',
 '0.0670316250',
 '0.0806985139',
 '0.0959450775',
 '0.1127993721',
 '0.1312739822',
 '0.1513652922',
 '0.1724677859',
 '0.1938794495',
 '0.2154561806',
 '0.2370811471',
 '0.2586622343',
 '0.2801289663',
 '0.3014292262',
 '0.3225260049',
 '0.3433943361',
 '0.3640185136',
 '0.3843896442',
 '0.4045035564',
 '0.4243590641',
 '0.4439565704',
 '0.4632969856',
 '0.4823809320',
 '0.5012082037',
 '0.5197774489',
 '0.5380860456',
 '0.5561301398',
 '0.5739048188',
 '0.5914043953',
 '0.6086227780',
 '0.6255539091',
 '0.6421922501',
 '0.6585333012',
 '0.6745741403',
 '0.6903139733',
 '0.7057546845',
 '0.7209013844',
 '0.7357629483',
 '0.7503525439',
 '0.7646881455',
 '0.7787930335',
 '0.7926962759',
 '0.8064331909',
 '0.8200457823',
 '0.8333213105',
 '0.8460198864',
 '0.8581535648',
 '0.8697344112',
 '0.8807743822',
 '0.8912852204',
 '0.9012783620',
 '0.9107648541',
 '0.9197552800',
 '0.9282596898',
 '0.9362875344',
 '0.9438475989',
 '0.9509479333',
 '0.9575957744',
 '0.9637974544',
 '0.9695582842',
 '0.9748823965',
 '0.9797725203',
 '0.9842296313',
 '0.9882523549',
 '0.9918358070',
 '0.9949687797',
 '0.9976215149',
 '1.0000000000']


to_fmt_strs=[
    # '[empty][columnsep][tab][color][cyan]LMPHYS: True[color]',
    # '[tab][color][cyan]LAEROLAN: True[color][columnsep][empty]',
    # 'NAERAD[columnsep]NAERAD',
    f'[empty][columnsep][tab][color][cyan]{key}: {value}[color]',
    f'[tab][color][cyan]{key}: {value}[color][columnsep][empty]',
    ]

printcol = 90
for tostr in to_fmt_strs:
    _fmt_str(tostr, max_print_length=printcol)
    print(''.ljust(int(printcol/2)-1) + ';')

# _dummy = _fmt_str(teststring,  max_print_length=60)
maxrow = str(' '.ljust(printcol-1) + '*')
print(maxrow)


