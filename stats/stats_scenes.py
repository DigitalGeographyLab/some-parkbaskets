#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 12:55:53 2020

INFORMATION
===========

This script calculates Mann-Whitney U test between national and international
visitors based on the scenes detected in
their photographs.


USAGE
=====

Run this script by typing:
    python stats_scenes.py -i input.pkl -o output.csv

@author: waeiski
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
print("[INFO] - Preparing data...")
df = df[['pid', 'user_id','parkname', 'locstr', 'seastr', 'scenepreds', 'scenecat', 'sceneprob',
        'detected_objs', 'landscape_region']]

# interesting object
topscenes = ['forest_path', 'forest/broadleaf', 'snowfield', 'tundra', 'ski_slope',
             'lake/natural', 'creek', 'park', 'swamp', 'tree_farm']

# filter by top scenes
parkdf = df[df['scenecat'].isin(topscenes)]

# get user grouped dataframe
parkdf = parkdf.groupby(['locstr','user_id','scenecat'])['scenecat'].apply(len).rename('count').reset_index()

# divide into nationals and internationals
nationals = parkdf[parkdf['locstr'] == 'National']
internationals = parkdf[parkdf['locstr'] == 'International']

# pivot the visitor groups
nationals = nationals.pivot(index='user_id', columns='scenecat')['count'].reset_index().fillna(0)
internationals = internationals.pivot(index='user_id', columns='scenecat')['count'].reset_index().fillna(0)

# column list
cols = ['creek', 'forest/broadleaf', 'forest_path', 'lake/natural',
        'park', 'ski_slope', 'snowfield', 'swamp', 'tree_farm', 'tundra']

# create empty dataframe
scene_tests = pd.DataFrame(index=['creek', 'forest/broadleaf', 'forest_path', 'lake/natural',
                                  'park', 'ski_slope', 'snowfield', 'swamp', 'tree_farm', 'tundra'])

# calculate mann-whitney u
print("[INFO] - Calculating...")
for c in cols:
    mwu, mpval = mannwhitneyu(nationals[c].loc[lambda x: x >= 1], internationals[c].loc[lambda y: y >= 1], alternative='two-sided')
    name = c
    scene_tests.at[name, 'mwu'] = mwu
    scene_tests.at[name, 'mwu_p_value'] = mpval
    scene_tests.at[name, 'nat_samp'] = len(nationals[c].loc[lambda x: x >= 1]) # sample size for effect size calculation
    scene_tests.at[name, 'int_samp'] = len(internationals[c].loc[lambda x: x >= 1]) # sample size for effect size calculation

# save to file
print("[INFO] - Saving results to csv...")
scene_tests.to_csv(outfile, sep=',', encoding='utf-8')

print("[INFO] - ... done!")