#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 13:32:26 2024

@author: thoverga
"""
import os



def check_dir_for_broken_links(checkdir):
    print(f'Checking links in {checkdir}:')
    print('---------------------------')
    
    #list links
    linkedfiles = [f for f in os.listdir(checkdir) if os.path.islink(os.path.join(checkdir, f))]
    
    if not bool(linkedfiles):
        print('No sym-links detected')
        print('---------------------------')
        return
    
    broken_links = []
    for f in linkedfiles:
        trgpath=os.path.join(checkdir, f)
        if not os.path.exists(trgpath):
            print(f'Fail : {f} --> link is broken! ')
            broken_links.append(f)
        else: 
            print(f'Ok   : {f}')
        
    print('---------------------------')
    print(f'{len(broken_links)}  broken links found!')



