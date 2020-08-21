#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 12:50:40 2020

INFORMATION
===========

This script performs a PERMANOVA test between all UMAP coordinates between
national and international visitors. First, it calculates a distance matrix
between the coordinate points on which it performs the PERMANOVA with 999
permutations.


USAGE
=====

Run this script by typing:
    python stats_permanova.py -i input.pkl -o output.csv

@author: waeiski
"""

import pandas as pd
from scipy.spatial import distance
import skbio as sk
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
df = pd.read_pickle('scripts/natparks/top20parks_resnext101_datetimes.pkl')

# get coordinates
df_array = df[["umap-2d-one", "umap-2d-two"]].to_numpy()

# calculate distance matrix
print("[INFO] - Calculating distance matrix...")
distmat = distance.cdist(df_array, df_array)

# convert to scikit-bio distance matrix
dm = sk.stats.distance.DistanceMatrix(distmat, df['pid'].values.tolist())

# get permanova distance (999 permutations as default)
print("[INFO] - Running PERMANOVA...")
perm = sk.stats.distance.permanova(distance_matrix=dm, grouping=df['locstr'])

# save output
print("[INFO] - Saving results to csv...")
perm.to_csv(outfile, sep=',', encoding='utf-8')

print("[INFO] - ... done!")