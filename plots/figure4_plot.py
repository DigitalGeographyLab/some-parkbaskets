#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  6 15:11:59 2020


INFORMATION
===========

This script plots the components of Figure 4 from the article. 


USAGE
=====

Run this script by typing:
    python figure4_plot.py -i input.pkl -o output1.png 

@author: tuomvais
"""

import pandas as pd
import matplotlib.pyplot as plt
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

# simplify dataframe for faster operations
print("[INFO] - Preparing data for plotting...")
selected = df[['scenecat','locstr']]

# crosstabulate by scenes and visitor group
grouped = pd.crosstab(selected.scenecat, selected.locstr).reset_index()

# count scene counts
for i, row in grouped.iterrows():
    grouped.at[i, 'scenecount'] = int(row['International']) + int(row['National'])

# sort dataframe by scene counts
grouped = grouped.sort_values(by='scenecount', ascending=False)

# get top 15 scene categories
top10 = grouped[:10]
top10list = top10['scenecat'].values.tolist()

# get df of top 15 scenes
top10df = df[df['scenecat'].isin(top10list)]

# initialize the figure
print("[INFO] - Plotting...")
plt.figure(figsize=(15,20))
sns.set(font_scale=1.2)
sns.set_style('white')

# plot the scene categories with swarm plot
ax2 = plt.subplot(2,1,1)
ax2 = sns.swarmplot(
        x="scenecat", y="sceneprob",
        hue="locstr",
        palette="colorblind",
        data=top10df, ax=ax2)
handles, labels = ax2.get_legend_handles_labels()
ax2.legend(handles,labels).set_title('User group')
ax2.set_title('a.', loc='left', fontdict={'fontsize':22})
ax2.set_xlabel('')
ax2.set_ylabel('Confidence of scene identification')
ax = plt.subplot(2,1,2)
ax = sns.swarmplot(
        x="scenecat", y="sceneprob",
        hue="landscape_region",
        hue_order=['Lapland fells','Eastern hills','Forests & lakes','Archipelago'],
        palette=['grey','orange','green','blue'],
        data=top10df, ax=ax)
handles, labels = ax.get_legend_handles_labels()
ax.legend(handles,labels).set_title('Landscape Region')
ax.set_title('b.', loc='left', fontdict={'fontsize':22})
ax.set_xlabel('')
ax.set_ylabel('Confidence of scene identification')
plt.tight_layout()
plt.savefig(args['output'], dpi=500, bbox_inches='tight')

print("[INFO] - ... done!")