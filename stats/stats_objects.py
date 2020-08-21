#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 12:55:53 2020

INFORMATION
===========

This script calculates Mann-Whitney U test between national and international
visitors based on the objects commonly associated with activities detected in
their photographs.


USAGE
=====

Run this script by typing:
    python stats_objects.py -i input.pkl -o output.csv

@author: Tuomas Väisänen
"""

import pandas as pd
from scipy.stats import mannwhitneyu
import argparse

# define arguments
ap = argparse.ArgumentParser()
ap.add_argument('-i','--input',required=True,
                help='path to input pickle')
ap.add_argument('-o','--output',required=True,
                help='path to output csv file')
args = vars(ap.parse_args())

# get input and output files
infile = args['input']
outfile = args['output']

# read pickle in
print("[INFO] - Reading data in...")
df = pd.read_pickle(infile)

# simplify data structure
print("[INFO] - Preparing data for Mann-Whitney U...")
df = df[['pid', 'user_id','parkname', 'locstr', 'seastr','scenecat', 'sceneprob',
        'detected_objs', 'landscape_region']]

# drop rows without detgections
df = df[df['detected_objs'].apply(lambda x: len(x) > 0)]

# interesting object
intobjs = ['person', 'dog', 'backpack', 'bicycle', 'skis', 'bench', 'dining table',
           'potted plant', 'bird']

# empty list for column names
cols = []

# count object occurrences
for obj in intobjs:
    obj2 = obj.replace(' ', '_')
    colname = obj2 + '_cnt'
    cols.append(colname)
    for i, row in df.iterrows():
        df.at[i, colname] = row['detected_objs'].count(obj)
        
# divide into nationals and internationals
nationals = df[df['locstr'] == 'National']
internationals = df[df['locstr'] == 'International']

# create empty dataframe
result = pd.DataFrame(index=['person', 'dog', 'backpack', 'bicycle', 'skis',
                             'bench', 'dining_table', 'potted_plant', 'bird'])

# calculate mann-whitney u
print("[INFO] - Calculating...")
for c in cols:
    mwu, mpval = mannwhitneyu(nationals[c].loc[lambda x: x >= 1], internationals[c].loc[lambda y: y >= 1], alternative='two-sided')
    name = c[:-4]
    result.at[name, 'mwu'] = mwu
    result.at[name, 'mwu_p_value'] = round(mpval, 7)
    result.at[name, 'nat_samp'] = len(nationals[c].loc[lambda x: x >= 1])
    result.at[name, 'int_samp'] = len(internationals[c].loc[lambda x: x >= 1])

# save to file
print("[INFO] - Saving results...")
result.to_csv(outfile, sep=',', encoding='utf-8')

print("[INFO] - ... done!")