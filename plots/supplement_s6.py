#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  6 14:58:14 2020

INFORMATION
===========

This script plots the supplementary figure S6 from the article

USAGE
=====

Run the script by typing:
    python supplement_s6.py -i input.pkl -o output.png

@author: tuomvais
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import argparse

# define arguments
ap = argparse.ArgumentParser()
ap.add_argument('-i','--input',required=True,
                help='path to input pickle')
ap.add_argument('-o','--output',required=True,
                help='path to output png')
args = vars(ap.parse_args())

# read pickle in
print("[INFO] - Reading data in...")
df = pd.read_pickle(args['input'])

# empty lists for season UMAP coordinates
print("[INFO] - Preparing data for plotting...")
wilist = []
splist = []
sulist = []
aulist = []

# loop over dataframe to populate empty season lists
for i, row in df.iterrows():
    if row['seastr'] == 'winter':
        datapoint = [row['umap-2d-one'], row['umap-2d-two']]
        wilist.append(datapoint)
    elif row['seastr'] == 'spring':
        datapoint = [row['umap-2d-one'], row['umap-2d-two']]
        splist.append(datapoint)
    elif row['seastr'] == 'summer':
        datapoint = [row['umap-2d-one'], row['umap-2d-two']]
        sulist.append(datapoint)
    elif row['seastr'] == 'autumn':
        datapoint = [row['umap-2d-one'], row['umap-2d-two']]
        aulist.append(datapoint)

# convert lists to array
wiX = np.array(wilist)
spX = np.array(splist)
suX = np.array(sulist)
auX = np.array(aulist)

# empty list for all UMAP coordinates
umaplist = []

# populate list of all UMAP coordinates
for i, row in df.iterrows():
    dp = [row['umap-2d-one'], row['umap-2d-two']]
    umaplist.append(dp)

# convert list to array
X = np.array(umaplist)

# Plot seasonal subplot
print("[INFO] - Plotting...")
plt.figure(figsize=(14,13),edgecolor='black', linewidth=8)
ax1 = plt.subplot(2, 2, 1)
ax1.set_title('Winter', size=22)
sns.kdeplot(X[:,0],X[:,1],
            shade=True,
            cmap='Greys',
            shade_lowest=False,
            alpha=0.2)
sns.kdeplot(wiX[:,0],wiX[:,1],
            shade=True,
            cmap='Blues',
            shade_lowest=False,
            alpha=1)

ax2 = plt.subplot(2, 2, 2)
ax2.set_title('Spring', size=22)
sns.kdeplot(X[:,0],X[:,1],
            shade=True,
            cmap='Greys',
            shade_lowest=False,
            alpha=0.2)
sns.kdeplot(spX[:,0],spX[:,1],
            shade=True,
            cmap='RdPu',
            shade_lowest=False,
            alpha=0.9)
ax3 = plt.subplot(2, 2, 3)
ax3.set_title('Summer', size=22)
sns.kdeplot(X[:,0],X[:,1],
            shade=True,
            cmap='Greys',
            shade_lowest=False,
            alpha=0.2)
sns.kdeplot(suX[:,0],suX[:,1],
            shade=True,
            cmap='BuGn',
            shade_lowest=False,
            alpha=0.9)
ax4 = plt.subplot(2, 2, 4)
ax4.set_title('Autumn', size=22)
sns.kdeplot(X[:,0],X[:,1],
            shade=True,
            cmap='Greys',
            shade_lowest=False,
            alpha=0.2)
sns.kdeplot(auX[:,0],auX[:,1],
            shade=True,
            cmap='OrRd',
            shade_lowest=False,
            alpha=0.8)
plt.tight_layout()
plt.savefig(args['output'], dpi=500)

print("[INFO] - ... done!")