#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 10 14:15:18 2024

@author: thoverga
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 10 14:12:05 2024

@author: thoverga
"""

import os
from pathlib import Path
import sys
import pprint

from .read_namelist import read_namelistfile_to_dict
from .diff_namelists import _print_diff, _compute_deepdiff
from .string_formatters import _fmt_str, css_style
from .namelist_interpret.io_namelist_explainer import get_defenitions


class Namelist(object):
    def __init__(self, file, name):
    
        self.file = file
        self.namelist = {} #namelist in nested dict structure
        self.name = str(name) #only for printing information
        
        # Read file
        self._read_namelist()
    
    def __str__(self):
        return pprint.pformat(self.namelist)
    
    
    def _read_namelist(self):
        """ Read in a namelistfile and put it in a nested dict structure. """
        namedict = read_namelistfile_to_dict(file=self.file)
        self.namelist = namedict
        
        
    def explain(self, tags="ALL", write_html=None, max_text_length=120):
        #TODO: Implement TAG filter
        column_char = '''   -->  '''
        
        #Setup html target path
        if write_html is None:
            output_format='terminal'
        else:
            output_format='html'
            #test if string is a path to a file
            if os.path.exists(write_html):
                trg_html = write_html
                #remove file
                os.remove(write_html)
            else:
                #assume writ_html is a filename to create in the current workdir
                if str(write_html).endswith('.html'):
                    trg_html = os.path.join(os.getcwd(), write_html)
                else:
                    trg_html = os.path.join(os.getcwd(), f'{write_html}.html')
        
        #read the defenitions
        defdict = get_defenitions()
            
        colsize = int((max_text_length-1)/2)
            
        # write header
        lstr = str(self.name.upper().center(colsize))
        rstr = f"Explanation with tags={tags}"        
        header=f'{lstr}{column_char}{rstr}\n {"-"*max_text_length}\n'


        # Write lines 
        groupstr = ""
        for groupname, val in self.namelist.items():
            if groupname not in defdict.keys():
                groupdef, groupinfo = 'Unknown', ''
                group_is_known=False
            else:
                groupdef=defdict[groupname]['Explenation']
                groupinfo = defdict[groupname]['Extra info']
                group_is_known=True
            
            #Get expelenation and info of group
            groupstr += _fmt_str(text = f'{groupname} --> [color][green]{groupdef}: {groupinfo}[color]',
                                 max_print_length=max_text_length,
                                 output=output_format,
                                 no_list=True) + '\n'
            # groupstr += (_fmt_str(text=f'{groupname}', N_ident=0, fill_column=False, output=output_format) +
            #              column_char +
            #              _fmt_str(text=f'{groupdef}: {groupinfo}', N_ident=0,
            #                       textcolor='green', output=output_format,
            #                       no_list=True) + 
            #              '\n')
            
            for settingname, setvalue in val.items():
                if not group_is_known:
                    settingdef = ''
                    settinginfo=''
                elif settingname in defdict[groupname]['Settings']:
                    settingdef = defdict[groupname]['Settings'][settingname]['Explenation']
                    settinginfo = defdict[groupname]['Settings'][settingname]['Extra info']
                else:
                    settingdef = 'Unknown'
                    settinginfo=''
                
                groupstr += _fmt_str(text=f'[tab]{settingname}: {setvalue} --> [color][green]{settingdef} : {settinginfo}[color]',
                                     max_print_length=max_text_length,
                                     output=output_format,
                                     no_list=True) + '\n'
                # groupstr += (_fmt_str(text=f'{settingname}: {setvalue}', N_ident=1, fill_column=False, output=output_format) +
                #              column_char +
                #              _fmt_str(text=f'{settingdef} {settinginfo}',
                #                       N_ident=1, textcolor='green',
                #                       output=output_format,
                #                       no_list=True) + 
                #              '\n')
            
        if output_format == 'html':
            #write to html file
            with open(trg_html, 'w') as f:
                f.write('<html>')
                f.write(css_style)
                f.write(f'<p><b>{header}</b>')
                for line in groupstr.split('\n'):
                    f.write(f'<pre>' + line + '<br /></pre>' + '\n')
                
                f.write('</p>')
                f.write('</html>')
            
            print(f'Explenation is written to: {trg_html}')
            return 
        return groupstr

        
        
# =============================================================================
# Compairing namlists
# =============================================================================


def print_diff(namelist_a, namelist_b, 
               write_html=None,
               max_text_lengt=120):
    
    diffdict =_compute_deepdiff(namelist_a, namelist_b)
    
    if write_html is None:
        html_formatted=False
    else:
        html_formatted=True
        #test if string is a path to a file
        if os.path.exists(write_html):
            trg_html = write_html
            #remove file
            os.remove(write_html)
        else:
            #assume writ_html is a filename to create in the current workdir
            if str(write_html).endswith('.html'):
                trg_html = os.path.join(os.getcwd(), write_html)
            else:
                trg_html = os.path.join(os.getcwd(), f'{write_html}.html')
            
        
    
    printstr = _print_diff(namelist_a=namelist_a,
                           namelist_b=namelist_b,
                           diffdict=diffdict,
                           max_print_length=max_text_lengt,
                           html_formatted=html_formatted)
    
    if html_formatted:
        #write to html file
        with open(trg_html, 'w') as f:
            f.write('<html>')
            f.write(css_style)
            
            for line in printstr:
                f.write(line)
            
            f.write('</html>')
        
        print(f'Diff is writen to: {trg_html}')
  
    
       
    
    return printstr 
    






# =============================================================================
# helpers
# =============================================================================

        
    
    
    
    
    