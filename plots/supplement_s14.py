#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  3 10:07:54 2020

This script plots supplementary figure 14 of the article, depicting people
detections by Mask r-CNN. The figure is saved as a png in the user-defined
output location.

@author: tuomvais
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import argparse

# define arguments
ap = argparse.ArgumentParser()
ap.add_argument('-i','--input',required=True,
                help='path to input pickle')
ap.add_argument('-o','--orienteers',required=True,
                help='path to output plot png')
args = vars(ap.parse_args())

# read dataframe in
print("[INFO] - Reading data in...")
df = pd.read_pickle(args['input'])

# count number of people
print("[INFO] - Preparing data for plotting...")
df['people_count'] = df['detected_objs'].apply(lambda x: x.count('person'))

# select people detected by Mask r-CNN
peoplemask = df.detected_objs.apply(lambda x: any(item for item in ['person'] if item in x))

# get people pics
ppldf = df[peoplemask]

# divide into visitor groups
locppl = df[df['locstr'] == 'National']
intppl = df[df['locstr'] == 'International']

# process people dataframe for mean of people per landscape region
lpreg = locppl.groupby('landscape_region')['people_count'].mean().rename('National')
ipreg = intppl.groupby('landscape_region')['people_count'].mean().rename('International')

# process people dataframe for mean of people per season
lpsea = locppl.groupby('seastr')['people_count'].mean().rename('National')
ipsea = intppl.groupby('seastr')['people_count'].mean().rename('International')

# set index order of plots
regindex = ['Lapland fells', 'Eastern hills', 'Forests & lakes', 'Archipelago']
seaindex = ['winter', 'spring', 'summer', 'autumn']

# concatenate series to df
regdf = pd.concat([lpreg, ipreg], axis=1)
seadf = pd.concat([lpsea, ipsea], axis=1)

# simplify original dataframe
seldf = df[['locstr','people_count']]

# group people counts by visitor group
grouped = seldf.groupby(['locstr','people_count']).size().rename('photocount').reset_index()

# calculate frequency of people detections
for i, row in grouped.iterrows():
    if grouped.at[i, 'locstr'] == 'National':
        grouped.at[i, 'freq'] = grouped.at[i, 'photocount'] / 9979 # photocount of nationals
    elif grouped.at[i, 'locstr'] == 'International':
        grouped.at[i, 'freq'] = grouped.at[i, 'photocount'] / 2780 # photocount of internationals

# sort values by people count
grouped = grouped.sort_values('people_count').reset_index()

# select 10 most common values
grp = grouped.pivot(index='people_count', columns='locstr', values='freq')[:11]

# initialize the figure quad subplot for people detections
print("[INFO] - Plotting...")
plt.figure(figsize=(15,12))

# scatter plot of people detections
ax = plt.subplot(2,2, 1)
g1 = sns.scatterplot(data=df, x='umap-2d-one', y='umap-2d-two', alpha=0.1, s=4, color='grey',legend='brief', ax=ax)
g = sns.scatterplot(data=ppldf, x='umap-2d-one', y='umap-2d-two', hue='locstr',
                    alpha=0.9, s=9, ax=ax, palette=['darkorange', 'steelblue']).set_title('a. Person detections by Mask R-CNN')
handles, labels = ax.get_legend_handles_labels()
ax.legend(markerscale=1,handles=reversed(handles[1:]), labels=reversed(labels[1:]))

# bar plot of frequencies
ax1 = plt.subplot(2,2,2)
ax1 = grp.plot(ax=ax1, kind='bar', width=0.9, rot=0, color=['steelblue', 'darkorange'],
               title='b. Amount of people in images')
ax1.legend(title=None)
ax1.set_ylabel('Frequency')
ax1.set_xlabel('Amount of people in images')
ax1.grid(which='both')
handles1, labels1 = ax1.get_legend_handles_labels()
labels1 = ['National', 'International']
ax1.legend(handles1, labels1, loc='upper right',title=None)

# bar plot of average number of people per landscape region
ax2 = plt.subplot(2,2,3)
ax2 = regdf.reindex(regindex).plot(ax=ax2,kind='bar', width=0.8, rot=0, color=['steelblue', 'darkorange'],
                                  title='c. Average number of people in images per landscape region')
ax2.set_ylabel('Average number of people in images')
ax2.set_xlabel('')
ax2.grid(which='both')

# bar plot of average number of people per season
ax3 = plt.subplot(2,2,4)
ax3 = seadf.reindex(seaindex).plot(ax=ax3, kind='bar', width=0.8, rot=0, color=['steelblue', 'darkorange'],
                                   title='d. Average number of people in images per season')
ax3.set_ylabel('Average number of people in images')
ax3.set_xlabel('')
ax3.grid(which='both')

# save figure
plt.tight_layout()
plt.savefig(args['output'], dpi=500, bbox_inches='tight')

print("[INFO] - ... done!")