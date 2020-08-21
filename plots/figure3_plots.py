#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  6 15:04:23 2020

INFORMATION
===========

This script plots the components of Figure 3 from the article. You have to
join them in Photoshop, GIMP or similar software if you want to have the exact
same image.


USAGE
=====

Run this script by typing:
    python figure3_plots.py -i input.pkl -o output1.png -in inset.png

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
ap.add_argument('-in','--inset',required=True,
                help='path to output inset png')
args = vars(ap.parse_args())

# read pickle in
print("[INFO] - Reading data in...")
df = pd.read_pickle(args['input'])

# empty lists for landscape region UMAP coordinates
print("[INFO] - Preparing data for plotting...")
laplist = []
eastlist = []
forlist = []
archilist = []

# loop over dataframe to populate landscape region lists
for i, row in df.iterrows():
    if row['landscape_region'] == 'Lapland fells':
        datapoint = [row['umap-2d-one'], row['umap-2d-two']]
        laplist.append(datapoint)
    elif row['landscape_region'] == 'Eastern hills':
        datapoint = [row['umap-2d-one'], row['umap-2d-two']]
        eastlist.append(datapoint)
    elif row['landscape_region'] == 'Forests & lakes':
        datapoint = [row['umap-2d-one'], row['umap-2d-two']]
        forlist.append(datapoint)
    elif row['landscape_region'] == 'Archipelago':
        datapoint = [row['umap-2d-one'], row['umap-2d-two']]
        archilist.append(datapoint)

# convert lists to arrays
lapX = np.array(laplist)
eastX = np.array(eastlist)
forX = np.array(forlist)
archiX = np.array(archilist)
    
# empty list for every UMAP coordinate pair
umaplist = []

# loop over dataframe to populate umap list
for i, row in df.iterrows():
    dp = [row['umap-2d-one'], row['umap-2d-two']]
    umaplist.append(dp)

# convert list to array
X = np.array(umaplist)

# Figure 3 main plot without inset
loclist = []
noloclist = []
for i, row in df.iterrows():
    if row['locstr'] == 'National':
        datapoint = [row['umap-2d-one'], row['umap-2d-two']]
        loclist.append(datapoint)
    elif row['locstr'] == 'International':
        datapoint = [row['umap-2d-one'], row['umap-2d-two']]
        noloclist.append(datapoint)

# lists to array
loc = np.array(loclist)
noloc = np.array(noloclist)

# colorbar keywords
ckws = {'shrink': 0.65, 'pad' : 0.008, 'fraction':0.06, 'ticks':[]}

# density map
print("[INFO] - Plotting first figure...")
plt.figure(figsize=(16,11))
#sns.set_style('white')
ax = sns.kdeplot(loc[:,0],loc[:,1], shade=True, cmap='Blues',
                 shade_lowest=False, cbar=True, cbar_kws=ckws, legend=True,
                 alpha=0.6)
ax = sns.kdeplot(noloc[:,0],noloc[:,1], shade=True, cmap='Reds',
                 shade_lowest=False, cbar=True,cbar_kws=ckws, legend=True, 
                 alpha=0.5)
ax.set_title('a.', loc='left', fontsize=18)
plt.xticks([])
plt.yticks([])
plt.tight_layout()
plt.savefig(args['output'], dpi=500)


# Figure 3 inset plot per landscape regions
print("[INFO] - Plotting inset figure...")
plt.figure(figsize=(16,13))
ax1 = plt.subplot(2, 2, 1)
ax1.set_title('b.', loc='left', fontsize=42)
sns.kdeplot(X[:,0],X[:,1],
            shade=True,
            cmap='Greys',
            shade_lowest=False,
            alpha=0.4)
sns.kdeplot(lapX[:,0],lapX[:,1],
            shade=True,
            cmap='bone_r',
            shade_lowest=False,
            alpha=0.9)
plt.xticks([])
plt.yticks([])
ax2 = plt.subplot(2, 2, 2)
ax2.set_title('c.', loc='left', fontsize=42)
sns.kdeplot(X[:,0],X[:,1],
            shade=True,
            cmap='Greys',
            shade_lowest=False,
            alpha=0.4)
sns.kdeplot(eastX[:,0],eastX[:,1],
            shade=True,
            cmap='YlOrBr',
            shade_lowest=False,
            alpha=0.9)
plt.xticks([])
plt.yticks([])
ax3 = plt.subplot(2, 2, 3)
ax3.set_title('d.', loc='left', fontsize=42)
sns.kdeplot(X[:,0],X[:,1],
            shade=True,
            cmap='Greys',
            shade_lowest=False,
            alpha=0.4)
sns.kdeplot(forX[:,0],forX[:,1],
            shade=True,
            cmap='Greens',
            shade_lowest=False,
            alpha=0.9)
plt.xticks([])
plt.yticks([])
ax4 = plt.subplot(2, 2, 4)
ax4.set_title('e.', loc='left', fontsize=42)
sns.kdeplot(X[:,0],X[:,1],
            shade=True,
            cmap='Greys',
            shade_lowest=False,
            alpha=0.4)
sns.kdeplot(archiX[:,0],archiX[:,1],
            shade=True,
            cmap='Blues',
            shade_lowest=False,
            alpha=1)
plt.xticks([])
plt.yticks([])
plt.tight_layout()
plt.savefig(args['inset'], dpi=500)

print("[INFO] - ... done!")