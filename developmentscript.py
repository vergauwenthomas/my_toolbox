#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 10 14:21:29 2024

@author: thoverga
"""
import pprint
import sys
from pathlib import Path


sys.path.insert(0, Path(__file__).parent)

workdir = Path(__file__).parent

import toolbox as tb



#%%


file1 = "/home/thoverga/Desktop/namelist_e927_surf_deode"
nam_deode =tb.Namelist(file1, 'deode_e927_surf')



file2 = "/home/thoverga/Desktop/namlist_e927_kmi"
nam_kmi = tb.Namelist(file2, 'RMI_e927')


_test = tb.print_diff(nam_deode,
            nam_kmi)



