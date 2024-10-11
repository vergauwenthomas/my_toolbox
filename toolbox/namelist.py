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


import sys
import pprint

from .read_namelist import read_namelistfile_to_dict
from .diff_namelists import _print_diff, _compute_deepdiff


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
        
        
        
# =============================================================================
# Compairing namlists
# =============================================================================



def print_diff(namelist_a, namelist_b, max_text_lengt=80):
  
    diffdict =_compute_deepdiff(namelist_a, namelist_b)
    _print_diff(namelist_a, namelist_b, diffdict, max_text_lengt)
    
    return diffdict
    



# =============================================================================
# helpers
# =============================================================================

        
    
    
    
    
    