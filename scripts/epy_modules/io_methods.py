#!/usr/bin/env python3

""" A collection of methods for converting epygram formats, reading and writing """
import os
import sys
import epygram



def construct_filepath(file_indic):
    """ Checks if the file is relative defined and if so add the pwd. """
    if str('/') not in file_indic:
        #relative path
        fullpath = os.path.join(os.getcwd(), file_indic)
    else:
        fullpath = file_indic
    assert os.path.isfile(fullpath), f'{fullpath} not a file.'
    return fullpath



def read_file(filepath):
    return epygram.formats.resource(filepath, 'r')

def read_2d_field(resource,fieldname, level=None):
    #construct fieldname
    if level is None:
        trg_fieldname = f'{str(fieldname).upper()}'
    else:
        trg_fieldname = f'S{str(level).zfill(3)}{str(fieldname).upper()}'
    
    #Check if the fieldname is present and unique defined
    field_candidates = resource.find_fields_in_resource(trg_fieldname)
    assert bool(field_candidates), f'{trg_fieldname} is not a knonw fieldname.'
    assert len(field_candidates) == 1, f'{trg_fieldname} as fieldname does not result in a unique field, specify the fieldname to destinguish: \n {field_candidates}'

    
    #Read the field
    trg_field = field_candidates[0]
    f = resource.readfield(trg_field)
    assert isinstance(f, epygram.fields.H2DField), f'The field is not a H2D field but a {type(f)}.'

    return f

     
