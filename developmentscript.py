#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 10 14:21:29 2024

@author: thoverga
"""
import pprint
from scripts.Namelist import Namelist

file1 = "/home/thoverga/Desktop/namelist_e927_surf_deode"
nam_deode =Namelist(file1, 'deode_e927_surface')



file2 = "/home/thoverga/Desktop/namlist_e927_kmi"
nam_kmi = Namelist(file2, 'RMI_e927')


# print(nam_kmi)


nam_a = nam_deode.namelist
nam_b = nam_kmi.namelist


#difference 1: settings in A not mentioned in B
print('found in A but not in B')
for groupname, setdict in nam_a.items():
    if not bool(setdict):
        continue
    
    if groupname not in nam_b.keys():
        print(f' * {groupname}:')
        pprint.pprint(setdict)
        continue
        
    #Now scan for the settings names
    for settingname, _values in setdict.items():
        if settingname not in nam_b[groupname].keys():
            print(f' * {groupname}:')
            pprint.pprint(setdict)
        


#diff 2: settings in B not mentioned in A
print('found in B but not in A')
for groupname, setdict in nam_b.items():
    if not bool(setdict):
        continue
    
    if groupname not in nam_a.keys():
        print(f' * {groupname}:')
        pprint.pprint(setdict)

# diff 3 settings different between A an B (both namelist have this setting)


# diff 4 empty namelist mentioned in A not in B

#diff 5 empty namelist mentioned in B not in A

