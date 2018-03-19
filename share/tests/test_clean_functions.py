#! usr/bin/env python3
#
# Author:   Roman Rivera (Invisible Institute)

'''pytest functions in clean_functions that require teardown/setup'''

import pytest
import pandas as pd
import numpy as np
import logging
import copy
from general_utils import *

from clean_functions import clean_data
log = logging.getLogger('test')

def test_clean_data():
    '''tests clean_data'''
    input_df = pd.DataFrame(
       {'first_name' : ['j edgar','Dylan ., JR', 'Mary sue E. M.', 'nAtAsha',''],
        'last_name' : ['Hoover., iii','Smith F', 'Jones V', "O.'brien-jenkins IV", np.nan],
        'middle_initial' : ['A', 'B', np.nan, 'C', 'D'],
        'incident_datetime' : ['9999-99-99 12:12', '2016-01-21', '2015-12-52 100:100', '2016-01-12 02:54', '07/21/16 10:59'],
        'trr_date' : ['200-12-12', '2000-12-12', '1921-01-01', '2016-12-01', '07/21/21'],
        'trr_time' : [1212, "00", 9876, "23:12", 109],
        'age' : [120, -999, 0, 21, "hi"],
        'race' : ['N', 'wbh', 'naTIVE AMericaN', 'black hispanic',  'I'],
        'gender' : ['mALE', 'm', 'NONE', 'FEMALE', np.nan]
        })
    orig_input_df = copy.deepcopy(input_df)
    output_df = pd.DataFrame(
       {'first_name' : ['J EDGAR','DYLAN', 'MARY SUE', 'NATASHA',np.nan],
        'last_name' : ['HOOVER','SMITH', 'JONES', "O'BRIEN-JENKINS", np.nan],
        'first_name_NS' : ['JEDGAR','DYLAN', 'MARYSUE', 'NATASHA',np.nan],
        'last_name_NS' : ['HOOVER','SMITH', 'JONES', 'OBRIENJENKINS', np.nan],
        'middle_initial' : ['A', 'B', 'E', 'C', 'D'],
        'middle_initial2' : [np.nan, 'F', 'M', np.nan, np.nan],
        'suffix_name' : ['III', 'JR', 'V', 'IV', np.nan],
        'incident_date' : pd.to_datetime(pd.Series([np.nan, '2016-01-21', np.nan, '2016-01-12', '2016-07-21'])).dt.date,
        'incident_time' : pd.to_datetime(pd.Series(['12:12:00', '00:00:00', np.nan, '02:54:00', '10:59:00'])).dt.time,
        'trr_date' : pd.to_datetime(pd.Series([np.nan, '2000-12-12', '1921-01-01', '2016-12-01', '1921-07-21'])).dt.date,
        'trr_time' : pd.to_datetime(pd.Series(['12:12:00', '00:00:00', np.nan, '23:12:00', '01:09:00'])).dt.time,
        'age' : [np.nan, np.nan, np.nan, 21, np.nan],
        'race' : ['BLACK', 'HISPANIC', 'NATIVE AMERICAN/ALASKAN NATIVE', 'BLACK',  'WHITE'],
        'gender' : ['MALE', 'MALE', '', 'FEMALE', '']
        })
    results = clean_data(input_df, log)
    assert set(results.columns) == set(output_df.columns)
    assert results.equals(output_df[results.columns])
    assert orig_input_df.equals(input_df)


def test_clean_data_dict():
    '''tests clean_data with dict_cols'''
    input_df = pd.DataFrame(
       {'race' : ['N', 'wbh', 'naTIVE AMericaN', 'black hispanic',  'I'],
        'gender' : ['mALE', 'm', 'NONE', 'FEMALE', np.nan]
        })
    orig_input_df = copy.deepcopy(input_df)
    output_df = pd.DataFrame(
       {'race' : ['BLACK', 'HISPANIC', 'NATIVE AMERICAN/ALASKAN NATIVE', 'BLACK',  'WHITE'],
        'gender' : ['', 'MALE', '', 'FEMALE', '']
        })
    input_dict_cols = {'gender' : {'mALE' : '', 'm' : 'MALE', 'FEMALE': 'FEMALE'}}
    results = clean_data(input_df, log,
                         dict_cols = input_dict_cols)

    assert set(results.columns) == set(output_df.columns)
    assert results.equals(output_df[results.columns])
    assert orig_input_df.equals(input_df)

def test_clean_data_skip():
    '''tests clean_data with skip_cols'''
    input_df = pd.DataFrame(
       {'race' : ['N', 'wbh', 'naTIVE AMericaN', 'black hispanic',  'I'],
        'gender' : ['mALE', 'm', 'NONE', 'FEMALE', np.nan]
        })
    orig_input_df = copy.deepcopy(input_df)
    output_df = pd.DataFrame(
       {'race' : ['BLACK', 'HISPANIC', 'NATIVE AMERICAN/ALASKAN NATIVE', 'BLACK',  'WHITE'],
        'gender': ['mALE', 'm', 'NONE', 'FEMALE', np.nan]
        })
    input_skip_cols = ['gender']
    results = clean_data(input_df, log, skip_cols=input_skip_cols)

    assert set(results.columns) == set(output_df.columns)
    assert results.equals(output_df[results.columns])
    assert orig_input_df.equals(input_df)


def test_clean_data_type_dict():
    '''tests clean_data with type_dict'''
    input_df = pd.DataFrame(
       {'first_name' : ['j edgar','Dylan ., JR', 'Mary sue E. M.', 'nAtAsha',''],
        'last_name' : ['Hoover., iii','Smith F', 'Jones V', "O.'brien-jenkins IV", np.nan],
        'middle_initial' : ['A', 'B', np.nan, 'C', 'D'],
        'incident_datetime' : ['9999-99-99 12:12', '2016-01-21', '2015-12-52 100:100', '2016-01-12 02:54', '07/21/16 10:59'],
        'trr_date' : ['200-12-12', '2000-12-12', '1921-01-01', '2016-12-01', '07/21/21'],
        'trr_time' : [1212, "00", 9876, "23:12", 109],
        'age' : [120, -999, 0, 21, "hi"],
        'race' : ['N', 'wbh', 'naTIVE AMericaN', 'black hispanic',  'I'],
        'gender' : ['mALE', 'm', 'NONE', 'FEMALE', np.nan]
        })
    input_types_dict = {
        'first_name': 'name', 'last_name':'name', 'middle_initial': 'name',
        'incident_datetime' : 'date', # notice should be datetime in yaml file
        'trr_date' : 'date', 'trr_time' : 'time',
        'age' : 'age', 'race' : 'race', 'gender' : 'gender'}
    orig_input_df = copy.deepcopy(input_df)
    output_df = pd.DataFrame(
       {'first_name' : ['J EDGAR','DYLAN', 'MARY SUE', 'NATASHA',np.nan],
        'last_name' : ['HOOVER','SMITH', 'JONES', "O'BRIEN-JENKINS", np.nan],
        'first_name_NS' : ['JEDGAR','DYLAN', 'MARYSUE', 'NATASHA',np.nan],
        'last_name_NS' : ['HOOVER','SMITH', 'JONES', 'OBRIENJENKINS', np.nan],
        'middle_initial' : ['A', 'B', 'E', 'C', 'D'],
        'middle_initial2' : [np.nan, 'F', 'M', np.nan, np.nan],
        'suffix_name' : ['III', 'JR', 'V', 'IV', np.nan],
        'incident_date' : pd.to_datetime(pd.Series([np.nan, '2016-01-21', np.nan, '2016-01-12', '2016-07-21'])).dt.date,
        'trr_date' : pd.to_datetime(pd.Series([np.nan, '2000-12-12', '1921-01-01', '2016-12-01', '1921-07-21'])).dt.date,
        'trr_time' : pd.to_datetime(pd.Series(['12:12:00', '00:00:00', np.nan, '23:12:00', '01:09:00'])).dt.time,
        'age' : [np.nan, np.nan, np.nan, 21, np.nan],
        'race' : ['BLACK', 'HISPANIC', 'NATIVE AMERICAN/ALASKAN NATIVE', 'BLACK',  'WHITE'],
        'gender' : ['MALE', 'MALE', '', 'FEMALE', '']
        })
    results = clean_data(input_df, log, types_dict=input_types_dict)
    assert set(results.columns) == set(output_df.columns)
    assert results.equals(output_df[results.columns])
    assert orig_input_df.equals(input_df)
