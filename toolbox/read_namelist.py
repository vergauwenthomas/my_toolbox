#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 11 17:34:53 2024

@author: thoverga
"""
import sys
import logging

logger = logging.getLogger(__name__)

def read_namelistfile_to_dict(file):
    #Read raw namelist file into a list of strings for each line
    filerawlist = []
    with open(file, 'r', encoding='UTF-8') as file:
        while line := file.readline():
            fmtline=line.replace(' ', '').rstrip()
            filerawlist.append(fmtline)
                
    
    #clean up common bad structures
    filerawlist = format_single_setting_per_row(filerawlist)
    filerawlist = format_add_comma_to_end_of_line(filerawlist)
    filerawlist = format_indented_values(filerawlist)
    
    # self._filerawlist = filerawlist
    
    
    #construct the dictionary
    namedict = {}
    skiplist = [] #these are the lines that are already assigned
    
       
    
    
    n_lines = len(filerawlist)
    
    for index in range(n_lines):
        logger.debug(f'checking line {index}')
        if index in skiplist:
            continue
    
        line = filerawlist[index]
        logger.debug(f'mapping line: {line}')
    
        
        if is_line_empty(line):
            logger.debug(f'skip empyt line {line}')
            skiplist.append(index)
            continue
        
        
        #check if the line is a groupkey
        if line.startswith('&'):
            groupname = line.replace('&', '')
            logger.debug(f'groupname: {groupname}')
            namedict[groupname] = {}
            #assing line
            skiplist.append(index)
            
            #read next line and look for settings
            for subidx in range(index+1,n_lines):
                subline = filerawlist[subidx]
                logger.debug('read subline: ', subline)
                
                if is_line_empty(subline):
                    logger.debug(f'  skip empyt subline {subline}')
                    skiplist.append(subidx)
                    continue
                #if new group detected, break the loop
                if subline.startswith('&'):  
                    break
                
                #catch setting_name
                if '=' in subline:
                    #setting name detecte
                    
                    settingname = subline.split('=')[0]
                    logger.debug(f'setting found: {settingname}')
                    
                    
                    
                    #situation 1: a single value for the setting
                    if ((subline.count(',') == 1) & #one value
                        ((filerawlist[subidx+1].startswith('&')) | #next line is new group OR
                         (filerawlist[subidx+1].count('=') == 1) | #next line is a new setting OR
                         (is_line_empty(filerawlist[subidx+1])))): #next line is empty
                        
                        value= subline.replace(',','').split('=')[1]
                        value = value_typecaster(value)
                        skiplist.append(subidx)
                        
                        namedict[groupname][settingname] = value
                        logger.debug(f'found pair: {settingname} : {value}')
                        continue
                        
                    #situation 2: multiple values (list) for one setting ON ONE LINE only
                    elif ((subline.count(',') > 1) & #multiple values on one line
                        (filerawlist[subidx+1].startswith('&') | #next line is new group OR
                         filerawlist[subidx+1].count('=') == 1 | #next line is a new setting OR
                         is_line_empty(filerawlist[subidx+1]))): #next line is empty
                    
                        
                        values = subline.split('=')[1].split(',') #split in values
                        values = [val for val in values if bool(val)] #remove empty values
                        values = [value_typecaster(val) for val in values] #typecast the elements
                        
                        skiplist.append(subidx)
                        
                        namedict[groupname][settingname] = values
                        logger.debug(f'found situation2: {settingname} : {values}')
                        continue
                    
                    #situation 3: multiple values (list) one multiple lines
                    elif ((subline.count(',') > 1) & #multiple values on one line
                        (not (filerawlist[subidx+1].startswith('&') | #next line is new group OR
                        filerawlist[subidx+1].count('=') == 1 | #next line is a new setting OR
                        is_line_empty(filerawlist[subidx+1])))): #next line is empty
                        
                        values =  subline.split('=')[1].split(',') #read right hand side string
                        skiplist.append(subidx)
                        
                        nextlines_values=[]
                        for subsubidx in range(subidx+1, n_lines):
                            subsubline = filerawlist[subsubidx]
                            
                            #skip empty rows
                            if is_line_empty(subsubline):
                                continue
                            
                            # if new group or settingname detected --> breake loop
                            if (subsubline.startswith('&') | subsubline.count('=') == 1):
                                break
                            
                            subsubvalues=subsubline.split(',')
                            values.extend(subsubvalues)
                            skiplist.append(subsubidx)
                            
                            subsubidx+=1
                            
                            
                        values = [val for val in values if bool(val)] #remove empty values
                        values = [value_typecaster(val) for val in values] #typecast the elements
                        namedict[groupname][settingname] = values
                        continue
                    
                    else:
                        sys.exit(f'unforseen situation: {subline}')
                subidx+=1
        
        index += 1
        
    return namedict

# =============================================================================
# Helpers
# =============================================================================
def is_line_empty(line):
    #skip rows without data
    if not line:
        return True
    if line == '/':
        return True
    return False
    

            

# =============================================================================
# Formatters
# =============================================================================
def value_typecaster(value):
    if ((value == '.FALSE.') | (value == '.F.')):
        return False
    if ((value == '.TRUE.') | (value == '.T.')):
        return True
    else:
        return value
        
def format_single_setting_per_row(rows):
    """ Check if there is one setting per row. Split rows if found. 
    
    Example: NFPMAX=287,NMFPMAX=287, --> NFPMAX=287,
                                         NMFPMAX=287,
    
    """
    nrows = len(rows)
    for idx in range(nrows):
        line = rows[idx]
        
        if line.count('=') >1:
            if (line.count('=') == line.count(',')):
                logger.debug(f'Format into multiple lines: {line}')
                lines = line.split(',')
                lines = [f'{subline},' for subline in lines if bool(subline)]
                
                #delete errornous line
                del rows[idx]
                #add at the correct index the splitted lines
                rows[idx:idx] = lines
                
                nrows += len(lines)-1
                
            else: 
                sys.exit('Multiple =-characters detected in one row, not equal to the numeber of ,-characters!')
        idx += 1
        
    return rows



def format_add_comma_to_end_of_line(rows):
    """ If there is no comma at the end of a row, then it is appended. 
        
    Example: CNMEXP='AR13' --> CNMEXP='AR13',
    
    """
    nrows = len(rows)
    for idx in range(nrows):
        line = rows[idx]
        
        if ((not ('&' in line)) & 
            (not (line.endswith(','))) &
            (not (is_line_empty(line)))):
            logger.debug(f'Add a comma to line: {line}')
            rows[idx] = f'{line},'
        idx+=1
    return rows


def format_indented_values(rows):
    """ Fix a line where the values are listed on the next line.
    
    
    FPVALH(0:87)=
      0.0000000000,    217.4625460000,    669.6928830000,   1316.411225000
    
    --> 
    FPVALH(0:87)=0.0000000000,    217.4625460000,    669.6928830000,   1316.411225000
    """
    nrows = len(rows)
    for idx in range(nrows):
        line = rows[idx]
        
        if line.endswith('='):
            logger.debug(f'Insert this line in front of the next occuring: {line}')
            
            #delete errornous line
            del rows[idx]
            #add the row in front of the next
            rows[idx:idx] = f'{line}{rows[idx]}'
            
            nrows -= 1
        elif line.endswith('=,'):
            logger.debug(f'Insert this line in front of the next occuring: {line}')
            
            #delete errornous line
            del rows[idx]
            #add the row in front of the next
            rows.insert(idx, f'{line[:-1]}{rows[idx]}')
            
            nrows -= 1
            
            
        idx += 1
    return rows
        