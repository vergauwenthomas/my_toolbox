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


test = tb.print_diff(nam_deode,
            nam_kmi, write_html='test.html')

# print(test)



#%%



# testfile = '/home/thoverga/Documents/github/my_toolbox/test.html'
# # with open(testfile, 'w') as f:
# #     f.write("<html>")
# #     f.write("<head>")
# #     f.write("<title>My Webpage</title>")
# #     f.write("</head>")
# #     f.write("<body>")
# #     f.write("<h1>Welcome to my webpage!</h1>")
# #     f.write(html_test)
# #     f.write("</body>")
# #     f.write("</html>")
    


# # from termcolor import colored
# #%%

# style = """<style type='text/css'>
# html {
#   font-family: Courier;
# }
# r {
#   color: #ff0000;
# }
# g {
#   color: #00ff00;
# }
# b {
#   color: #0000ff;
# }
# </style>"""

# RED = 'r'
# GREEN = 'g'
# BLUE = 'b'

# def write_html(f, type, str_):
#     f.write('<%(type)s>%(str)s</%(type)s>' % {
#             'type': type, 'str': str_ } )

# os.remove(testfile)
# with open(testfile, 'w') as f:
#     f.write('<html>')
#     f.write(style)
    
#     for line in test.split('\n'):
#         f.write('<pre>' + line + '<br /></pre>' + '\n')
        
    
    
#     # write_html(f, RED, 'My name is so foo..\n')
#     # write_html(f, BLUE, '102838183820038.028391')
    
#     f.write('</html>')
    



#%%

# coltype = 'r'
# string= 'bladibla'

# print('<%(type)s>%(str)s</%(type)s>' % {
#         'type': coltype, 'str': string } )

# print(f'<%coltype)s>%(string)s</%(coltype)s>')
         