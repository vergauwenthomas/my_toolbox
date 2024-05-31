#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 21 10:49:49 2024

@author: thoverga
"""

import os
import yaml
from subprocess import Popen, PIPE, CalledProcessError


# subprocess.call(["ls", "-l"])

bashtools = "/home/thoverga/Documents/github/my_toolbox/bashtools"


# =============================================================================
# Open secrets
# =============================================================================

secretsfile = os.path.join(bashtools, 'secrets.yml')

with open(secretsfile) as stream:
    try:
        secrets = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)






file = "/home/thoverga/Documents/github/my_toolbox/README.md"
target = "/home/thoverga/Documents/github/my_toolbox/bashtools/GELUKT"


# rsync -av path_to_file cu1c@aa-login:/ec/res4/hpcperm/cu1c

cmd = ["rsync", "-avu", file, target]

run_bash_in_python(cmd)




