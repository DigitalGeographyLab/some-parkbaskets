#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 11:21:30 2020

@author: waeiski
"""

import shutil
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import argparse

# define arguments
ap = argparse.ArgumentParser()
ap.add_argument('-i','--input',required=True,
                help='path to input pickle')
ap.add_argument('-o','--output',required=True,
                help='path to output orienteers plot png')

args = vars(ap.parse_args())

# read data in
print("[INFO] - Reading data in...")
df = pd.read_pickle(args['input'])

# selected areas from scatterplot
print("[INFO] - Preparing data for plotting...")
orienteers = df[(df['umap-2d-one'] > 5) & (df['umap-2d-two'] > 0)]

# parse orienteers by months, landscaperegions and unique users
ordate = orienteers.groupby(['locstr','date_month']).size().rename('posts')
orspa = orienteers.groupby(['locstr','landscape_region',]).size().rename('posts')
orusers = orienteers.groupby('user_id').size().rename('posts').sort_values(ascending=False).reset_index()

# orienteers classification
df['Type'] = 'Other'
for i in orienteers.index:
    df.at[i, 'Type'] = 'Orienteer'

# plot orienteers
print("[INFO] - Plotting...")
plt.figure(figsize=(12,9))
ax = plt.subplot(2,2, 1)
g = sns.scatterplot(data=df, x='umap-2d-one', y='umap-2d-two', hue='Type', palette='gnuplot_r', alpha=0.7, s=6, ax=ax).set_title('a. Orienteering pictures')
ax2 = plt.subplot(2,2, 2)
ordate.unstack(level=0)[1:].plot(ax=ax2, kind='line', color=['darkorange','steelblue'],
                                      linewidth=1.8, title='b. Orienteering temporality')
ax2.legend(title=None)
ax2.set_ylabel('Post count')
ax2.set_xlabel('Time')
ax2.grid(which='both')
handles, labels = ax2.get_legend_handles_labels()
ax2.legend(reversed(handles), reversed(labels), loc='upper left',title=None)
ax3 = plt.subplot(2,2, 3)
orspa.unstack(level=0).plot(ax=ax3, kind='bar', width=0.8, color=['darkorange','steelblue'],
                                 title='c. Orienteering pictures per landscape region', rot=25)
ax3.set_ylabel('Post count')
ax3.set_xlabel('')
ax3.grid(which='both')
handles, labels = ax3.get_legend_handles_labels()
ax3.legend(reversed(handles), reversed(labels), loc='upper left',title=None)
ax4 = plt.subplot(2,2, 4)
orusers.plot(ax=ax4, kind='line', title='d. Orienteering posts by unique users')
ax4.set_ylabel('Post count')
ax4.set_xlabel('Unique users')
ax4.grid(which='both')
plt.tight_layout()
plt.savefig(args['output'], dpi=500)

print("[INFO] - ... done!")