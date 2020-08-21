#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 14:40:19 2020


INFORMATION
===========

This script plots the supplementary figure S12 from the article


USAGE
=====

Run this script by typing:
    python supplementary_s12.py -i input.pkl -o supplementary_s12.png
    
@author: Tuomas Väisänen
"""

import shutil
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import argparse

# define arguments
ap = argparse.ArgumentParser()
ap.add_argument('-i','--input',required=True,
                help='path to input pickle')
ap.add_argument('-o','--output',required=True,
                help='path to output plot png')
args = vars(ap.parse_args())

# read df in
print("[INFO] - Reading pickle in...")
df = pd.read_pickle(args['input'])

# create mask for doggy pics
print("[INFO] - Preparing data for plotting...")
mask = df.detected_objs.apply(lambda x: any(item for item in ['dog'] if item in x))

# get pics with dogs
doggydf = df[mask]

# get pics without dogs
nodog = df[~mask]

# separate dog pics from nationals and internationals
locdog = doggydf[doggydf['locstr'] == 'National']
intdog = doggydf[doggydf['locstr'] == 'International']

# divide into landscape regions and seasons
locreg = locdog['landscape_region'].value_counts().rename('National')
intreg = intdog['landscape_region'].value_counts().rename('International')
locsea = locdog['seastr'].value_counts().rename('National')
intsea = intdog['seastr'].value_counts().rename('International')

# set order of plots
regindex = ['Lapland fells', 'Eastern hills', 'Forests & lakes', 'Archipelago']
seaindex = ['winter', 'spring', 'summer', 'autumn']

# concatenate series to df
regdf = pd.concat([locreg, intreg], axis=1)
seadf = pd.concat([locsea, intsea], axis=1)

# dataframe for manually checked results of dog pictures
dogtype = pd.DataFrame({'National':[6,82,10,27],'International':[48,16,19,17],},
                       index=['Dog sleigh','Other dog', 'Other animal', 'Misdetection'])

# plot dog subplot
print("[INFO] - Plotting...")
plt.figure(figsize=(14,11))
ax = plt.subplot(2,2,1)
g2 = sns.scatterplot(data=nodog, x='umap-2d-one', y='umap-2d-two', color='grey', ax=ax, alpha=0.3, s=3)
g = sns.scatterplot(data=doggydf, x='umap-2d-one', y='umap-2d-two',
                    hue='locstr', palette=['darkorange', 'steelblue'],
                    ax=ax, s=20).set_title('a. Dog detections by Mask R-CNN')
handles, labels = ax.get_legend_handles_labels()
ax.legend(markerscale=1,handles=reversed(handles[1:]), labels=reversed(labels[1:]))
#ax.legend(handles=handles[1:], labels=labels[1:])
ax2 = plt.subplot(2,2,2)
ax2 = regdf.reindex(regindex).plot(ax=ax2,kind='bar', width=0.8, rot=0, color=['steelblue','darkorange'],
                                  title='b. Dog picture spatiality (Mask R-CNN)')
plt.grid(which='both')
ax3 = plt.subplot(2,2,3)
ax3 = seadf.reindex(seaindex).plot(ax=ax3, kind='bar', width=0.8, rot=0, color=['steelblue','darkorange'],
                                   title='c. Dog picture seasonality (Mask R-CNN)')
plt.grid(which='both')
ax4 = plt.subplot(2,2,4)
ax4 = dogtype.plot(ax=ax4, kind='bar', width=0.8, rot=0, color=['steelblue','darkorange'],
                   title='d. Dog picture content type (Manually classified)')
plt.tight_layout()
plt.grid(which='both')
plt.savefig(args['output'], dpi=500)

print("[INFO] - ... done!")