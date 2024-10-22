#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 13:19:31 2024

@author: thoverga
"""
import os
from pathlib import Path
import pandas as pd
import json


# =============================================================================
# How it works
# =============================================================================

# The explanations of groups and setttings are stored as a json file in the package.
# Because it is not practical to work directly in the json files, there is
# an online google sheet containing the same information: 

#     https://docs.google.com/spreadsheets/d/1qvwju807GBhnCQ5TOdgdqjIMPUWumCi9dEs1XwYfjvU/edit?usp=sharing
    
# The file is publicly-readable. If you want to edit this file ask thomas (or the owner) for permission. 


# There is a function to update your local explanation files(JSON) from the online sheet.

# Local defenition files
def_file = os.path.join(str(Path(__file__).parent), 'namelist_def.json')



#online defenition file
sheet_name = 'namelist' 
human_url='https://docs.google.com/spreadsheets/d/1qvwju807GBhnCQ5TOdgdqjIMPUWumCi9dEs1XwYfjvU/edit?usp=sharing'
sheet_id = '1qvwju807GBhnCQ5TOdgdqjIMPUWumCi9dEs1XwYfjvU'


def get_defenitions():
    with open(def_file) as f:
        d = json.load(f)
    return d



def _construct_new_df_from_reference(Namelist, trg_csv_file):
    """ This method is NOT designed for users. This method is called when
        a new online dataframe must be made from a new reference namelist.
        """
        
    namdict = Namelist.namelist
    dflist = []
    for key, val in namdict.items():
        #always print group first without settings --> so group explenation can be written
        series = pd.Series({'groupname': key,
                  'settingname': None,
                  'value': None})
        
        dflist.append(series.to_frame().transpose())
        
        if bool(val):
            for setname, value in val.items():
                series = pd.Series({'groupname': key,
                          'settingname': setname,
                          'value': value})
                dflist.append(series.to_frame().transpose())
                
    df = pd.concat(dflist)
    
    #write to file
    df.to_csv(trg_csv_file, index=False)



    
def _get_name_def_from_online():
        
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
    #read online sheet
    df = pd.read_csv(url, header=0, sep=None, index_col=False, dtype={'Value': 'str'})

    #split in groups and settings
    groupsdf = df[df['Setting'].isna()]
    settingsdf = df[df['Setting'].notna()]

    #Construct def dict, start with groups and later add the specific settings
    def_dict = groupsdf.fillna('').set_index('Groupname').to_dict(orient='index')

    #format list values
    def_dict = {_key:{'tags': val['Tags'].replace(' ','').split(','), #list of tags
                          'Explenation': val['Explenation'],
                          'Extra info': val['Extra info'],
                          'Settings': {}} for _key, val in def_dict.items()}


    #add settings to the groups
    settingsdf = settingsdf.fillna('')
    for _idx, row in settingsdf.iterrows():
        setdict = dict(row)
        #updatedict
        update_dict = {setdict['Setting']: {'value': setdict['Value'],
                                            'Explenation': setdict['Explenation'],
                                            'Extra info': setdict['Extra info']}}
        
        #add the setting to the defenitions
        def_dict[setdict['Groupname']]['Settings'].update(update_dict)
    
    # overwrite the local defenitions
    # os.remove(def_file) #clear the file
    
    with open(def_file, 'w', encoding='utf-8') as f:
        json.dump(def_dict, f, ensure_ascii=False, indent=4)
    
    print('Local defenitions are updated with online table!')    


 