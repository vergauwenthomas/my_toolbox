#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 17 13:37:38 2024

@author: thoverga
"""
import datetime
import pandas as pd
import os
import yaml
from pathlib import Path


toolbox_dir = Path(__file__).resolve().parents[1]
telecom_base_dir = '/mnt/HDS_ALADIN/ALADIN/telecom'




start="2020-08-02T02:00:00Z"
end = "2020-08-02T03:00:00Z"


# =============================================================================
# Helpers
# =============================================================================

def run_bash_in_python(cmd_list):
    """ Run a bash command, the input is a list.
    (The output and error are streamed to a print statement)
    """

    #Pipe output of command in real-time !!!!
    with Popen(cmd_list, stdout=PIPE, bufsize=1, universal_newlines=True) as p:
        for line in p.stdout:
            print(line, end='') # process line here

    if p.returncode != 0:
        raise CalledProcessError(p.returncode, p.args)

    return



def get_secrets():
    """ Read the secrets yaml file and return a dict of secrets."""
    secretsfile = os.path.join(bashtools, 'secrets.yml')

    with open(secretsfile) as stream:
        try:
            secrets = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    return secrets

# =============================================================================
# TUNNEL: KILI --> ATOS
# =============================================================================

def creat_teleport_tunnel():
    """ Setup the teleport login, using the secrets file. """
    #lauch a bash script
    run_bash_in_python(['source', 'bashtools/auth_to_atos.sh']) #Setup teleport

    return

def transfer_file(filepath, target_path, atos_login='aa-login'):
    """ Transfer a file (from kili), to ATOS. """
    #Read secrets
    secrets = get_secrets()

    cmd = ['rsync',
           '-avu',
           f'{filepath}',
           f'{secrets["ecmwf_username"]}@{atos_login}:{target_path}']

   run_bash_in_python(cmd)
   return


#%% testing
print('creating tunnel')
creat_teleport_tunnel()

print('done with tunnel')
file = "/home/thoverga/fileserver/home/error"
target = "/home/cu1c/."

transfer_file(file, target)


print('file transferd')
#%%



# =============================================================================
# KILI-SIDED: Construct paths to telecom files
# =============================================================================


def construct_datetime_telecom_map(startstr, endstr,
                                   telecom_basedir='/mnt/HDS_ALADIN/ALADIN/telecom',
                                   telecom_file_fmt = '%Y%m%dr%H',
                                   telecom_file_prefix='telecom-',
                                   telecom_file_postfix='.tar',
                                   include_cycles=[0,6,12,18]):

    #Construct datetrange
    startdt = pd.to_datetime(startstr)
    enddt = pd.to_datetime(endstr)
    targetsdt = pd.date_range(start=startdt,
                               end=enddt,
                               freq=pd.Timedelta('1h'))

    def find_nearest_cycle(dt, candidate_cycles=include_cycles):
        candidate_cycles.sort()
        candidates = pd.Series([pd.to_datetime(f'{dt.year}-{str(dt.month).zfill(2)}-{str(dt.day).zfill(2)}T{str(cycle).zfill(2)}:00:00Z') for cycle in candidate_cycles])
        diff = candidates - dt
        diff = diff[diff.dt.total_seconds()<=0]
        return candidates.loc[diff.index[-1]]


    def path_constructor(cycledt, fmt=telecom_file_fmt, prefix=telecom_file_prefix,
                         postfix=telecom_file_postfix):
        filename = f"{prefix}{cycledt.strftime(fmt)}{postfix}" #i.g. telecom-20220811r06.tar
        path = os.path.join(telecom_base_dir,
                            f'{cycledt.year}', #year
                            f'{str(cycledt.month).zfill(2)}', #month
                            f'{str(cycledt.day).zfill(2)}', #month
                            filename)
        return path

    dt_to_telecom_map = {}
    for dt in targetsdt:
        cycle_dt = find_nearest_cycle(dt)
        path = path_constructor(cycle_dt)
        dt_to_telecom_map[dt] = path

    return dt_to_telecom_map





















