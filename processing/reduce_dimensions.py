#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 10 09:51:16 2020

INFORMATION
===========

This script reduces the dimensions of the extracted image features to two, plots
a sanity check plot of the result and saves the output pickled dataframe.

It first randomizes the order of the posts to reduce any bias that could occur
from their order. Then reduces dimensions with UMAP to two, saves the UMAP
results to dataframe, plots a scatterplot of the results as a sanity check and
finally saves the resulting dataframe as a pickle.


USAGE
=====

Run this script with default values by typing:
    python reduce_dimensions.py -i input.pkl -o output.pkl
    
Run this script with modified values by typing e.g.:
    python reduce_dimensions.py -i input.pkl -c 2 -n 15 -d 0.5 -r 80 -v locstr -ov plot.png -o output.pkl


@author: tuomvais
"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import argparse
import umap

# define arguments
ap = argparse.ArgumentParser()
ap.add_argument('-i','--input',required=True,
                help='path to input pickled dataframe')
ap.add_argument('-c','--components', default=2,
                help='number of components to reduce dimenions to, e.g. set 3 '
                'for 3d plot. default= 2')
ap.add_argument('-n','--neighbors', default=80,
                help='number of neighbors to calculate UMAP with, default= 80')
ap.add_argument('-d','--distance', default=0,
                help='how tightly UMAP packs resulting points together. default= 0.0')
ap.add_argument('-r','--randomstate', default=42,
                help='random state initiation. default= 42')
ap.add_argument('-v','--visualization', default='season',
                help='column to visualize plot by, valid columns include: '
                'locstr, season, parkname')
ap.add_argument('-ov','--outviz',
                help='output directory for plot')
ap.add_argument('-o','--output', required=True,
                help='output pickle directory')
args = vars(ap.parse_args())

# load extracted features in
print('[INFO] - Reading dataframe in...')
df = pd.read_pickle(args['input'])

# retrieve featurecols
print('[INFO] - Preparing data for dimensionality reduction...')
featurecols = df.columns.tolist()[:2047]

# initiate a random seed and random permutation objects
np.random.seed(42)
rndperm = np.random.permutation(df.shape[0])

# get length of dataframe
N = len(df)

# get randomized order copy of the dataframe
df_rnd = df.loc[rndperm[:N],:].copy()

# get columns with extracted features
data = df_rnd[featurecols].values

# run UMAP
print('[INFO] - Running UMAP...')
umap_results = umap.UMAP(n_components=2, n_neighbors=80, min_dist=0.0,
                         random_state=42).fit_transform(data)

# save results to dataframe
print('[INFO] - Saving UMAP results...')
df_rnd['umap-2d-one'] = umap_results[:,0]
df_rnd['umap-2d-two'] = umap_results[:,1]

# plot UMAP scatterplot as sanity check
print('[INFO] - Plotting a sanity check plot...')
plt.figure(figsize=(15,12))
sns.scatterplot(
    x="umap-2d-one", y="umap-2d-two",
    hue=args['visualization'],
    palette='deep',
    data=df_rnd,
    legend="brief",
    alpha=0.6
)

# save figure to png
plt.savefig(args['outviz'], bbox_inches='tight')

# reset index after random permutation
df_rnd = df_rnd.reset_index(drop=True)

# save to pickle
print('[INFO] - Saving results to dataframe...')
df_rnd.to_pickle(args['output'])

print('[INFO] - ... done!')