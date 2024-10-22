#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 11 09:47:14 2024

@author: thoverga
"""

import logging

# Create the Root logger
rootlog = logging.getLogger(__name__)  # logger name is <metobs-toolkit>
rootlog.setLevel(logging.DEBUG)  # set rootlogger on debug


#Namelist stuff
from toolbox.namelist import Namelist, print_diff
from .namelist_interpret.io_namelist_explainer import _get_name_def_from_online

#Pyfa stuff
try:
    import pyfa_tool as pyfa
    _with_pyfa = True
except ModuleNotFoundError:
    rootlog.warning('Toolbox: Pyfa is not found, FA-methods are not active.')
    print('(Toolbox: Pyfa is not found, FA-methods are not active ... ) ')
    _with_pyfa= False


#General stuff
__version__= "0.1.0a"
rootlog.info(f'toolbox v{__version__}')
