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

#Epygram stuff
try:
    from toolbox.epy_what import run_epygram_what
    from toolbox.epy_plot import make_regular_2d_plot
    _with_epygram = True
except ModuleNotFoundError:
    rootlog.warning('Toolbox: Epygram is not found, FA-methods are not active.')
    print('(Toolbox: Epygram is not found, FA-methods are not active ... ) ')
    _with_epygram= False


#General stuff




__version__= "0.1.0a"
rootlog.info(f'toolbox v{__version__}')