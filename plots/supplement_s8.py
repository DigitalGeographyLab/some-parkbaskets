#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 13 10:26:43 2020

INFORMATION
===========

This script plots supplementary figure S8 from the article.


USAGE
=====

Run the script by typing:
    python supplement_s8.py -i pickle.pkl -o supplementary8.png

@author: waeiski
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from collections import Counter
import argparse

# define arguments
ap = argparse.ArgumentParser()
ap.add_argument('-i','--input',required=True,
                help='path to input pickle')
ap.add_argument('-o','--output',required=True,
                help='path to output plot png')
args = vars(ap.parse_args())

# read data in
print("[INFO] - Reading pickle in...")
df = pd.read_pickle(args['input'])

# activities dataframe
print("[INFO] - Preparing data for plotting...")
adf = df[df['obj_count'] >= 1]

# landscapes list
toplands = sorted(Counter(df['scenecat'].values.tolist()).items(), key=lambda x: x[1], reverse=True)
lands = Counter(df['scenecat'].values.tolist())
landlist =['forest_path','forest/broadleaf','snowfield','tundra','ski_slope','lake/natural','creek','park']

# activity list
objs = adf['unique_objs'].values.tolist()
objs = Counter([o for ob in objs for o in ob])
topobjs = sorted(objs.items(), key=lambda x: x[1], reverse=True)
actlist = ['backpack','bird','boat', 'potted plant', 'dining table','bicycle','skis','dog']

# set font size
plt.rcParams.update({'font.size': 16})

# dual plot of landscapes and activities supplementary S8
print("[INFO] - Plotting...")
plt.figure(figsize=(20,8.5))
ax = plt.subplot(1,2,1)
colors = sns.color_palette('colorblind',len(landlist))
g = sns.scatterplot(data=df, x='umap-2d-one', y='umap-2d-two', alpha=0.1, color='grey', s=10, label='other pictures',ax=ax)
for i in range(len(landlist)):
    land = landlist[i]
    color = colors[i]
    plotmask = df['scenecat'].apply(lambda x: any(item for item in [land] if item in x))
    plotdf = df[plotmask]
    g2 = sns.kdeplot(data=plotdf['umap-2d-one'], data2=plotdf['umap-2d-two'], alpha=0.4, bw=0.12, n_levels=15,
                    shade=True, shade_lowest=False, color=color, ax=ax)
    g3 = sns.scatterplot(data=plotdf, x='umap-2d-one', y='umap-2d-two', alpha=0.9, color=color, s=19,
                        label=land.replace('_',' ') + ' (n=' + str(lands[land])+')', legend='brief',ax=ax).set_title('a. Top-8 categories for scene classification',fontsize=19)
plt.legend(markerscale=2.5, fontsize=18)
plt.tight_layout()

colors = sns.color_palette('colorblind',len(actlist))
ax2 = plt.subplot(1,2,2)
g4 = sns.scatterplot(data=df, x='umap-2d-one', y='umap-2d-two', alpha=0.1, color='grey', s=10, label='other pictures',ax=ax2)
for i in range(len(actlist)):
    act = actlist[i]
    color = colors[i]
    plotmask = adf['unique_objs'].apply(lambda x: any(item for item in [act] if item in x))
    plotdf = adf[plotmask]
    g5 = sns.kdeplot(data=plotdf['umap-2d-one'], data2=plotdf['umap-2d-two'], alpha=0.4, bw=0.12, n_levels=15,
                     shade=True, shade_lowest=False, color=color,ax=ax2)
    g6 = sns.scatterplot(data=plotdf, x='umap-2d-one', y='umap-2d-two', alpha=0.9, color=color, s=19,
                         label=act +' (n='+ str(objs[act])+')', legend='brief',ax=ax2).set_title('b. Objects associated with specific activities \ndetected using instance-level object detection',fontsize=19)
plt.legend(markerscale=2.5, fontsize=18)
plt.tight_layout()
plt.savefig(args['output'], dpi=500, bbox_inches='tight')

print("[INFO] - ... done!")