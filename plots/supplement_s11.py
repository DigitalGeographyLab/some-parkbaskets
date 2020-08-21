#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 15 20:08:21 2020

@author: waeiski
"""

import shutil
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
                help='path to output png')
args = vars(ap.parse_args())

# read data in
df = pd.read_pickle(args['input'])

# drop rows without detections
df = df[df['obj_count'] > 0]

# listify sets
df['unique_objs'] = df['unique_objs'].apply(lambda x: list(x))

# separate nationals and internationals
testdf = df.groupby('locstr')['unique_objs'].apply(list)
locdf = df[df['locstr'] == 'National']
intdf = df[df['locstr'] == 'International']

# empty lists for object detections
loclist = []
intlist = []

# append objs to lists
locdf['unique_objs'].apply(lambda x:  loclist.append(x))
intdf['unique_objs'].apply(lambda x:  intlist.append(x))

# flatten lists
loclist = [item for l in loclist for item in l]
intlist = [item for l in intlist for item in l]

# count occurrences and sort
loclist = sorted(Counter(loclist).items(), key=lambda x: x[1], reverse=True)
intlist = sorted(Counter(intlist).items(), key=lambda x: x[1], reverse=True)

# get top 10 objects except persons
loclist = loclist[1:11]
intlist = intlist[1:11]

# create dataframes
loc = pd.DataFrame(loclist, columns=['object', 'National'])
intn = pd.DataFrame(intlist, columns=['object', 'International'])

# join dataframes
joined = pd.merge(intn, loc, on='object')

# plot
ax = joined.sort_values('National', ascending=False).plot(kind='bar', stacked=True, x='object', figsize=(11,8), rot=7, width=0.9,
                 color=['darkorange','steelblue'])
handles, labels = ax.get_legend_handles_labels()
ax.legend(handles=reversed(handles), labels=reversed(labels))
#for p in ax.patches:
#    ax.annotate('n='+str(p.get_height()), (p.get_x() +0.03, p.get_height() * 0.80))
ax.set_xlabel('Objects detected by instance-level object detection')
ax.set_ylabel('Count of unique objects')
ax.grid(which='both')
plt.tight_layout()
plt.savefig(args['output'], bbox_inches='tight', dpi=500)
