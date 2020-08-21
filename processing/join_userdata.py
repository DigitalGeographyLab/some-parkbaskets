# -*- coding: utf-8 -*-
"""
Created on Wed Aug 21 10:31:46 2019

INFO
====

This script joins the dataframe containing feature vectors to the dataframe
containing post and user data. It results in a pickle containing all 2048
extracted features and the Flickr user data.

REQUIREMENTS
============
pickle file:
    image features
    unique photo ids

User data file:
    unique photo ids
    user home location
    locality
    datetimes

USAGE
=====
Run script in terminal/command prompt:
    python join_userdata.py -i features.pkl -ud users.gpkg -o output.pkl

@author: tuomvais
"""

from __future__ import print_function
import time
import numpy as np
import pandas as pd
import geopandas as gpd
import argparse

# define arguments
ap = argparse.ArgumentParser()
ap.add_argument('-i','--input',required=True,
                help='path to input feature vector dataset')
ap.add_argument('-ud','--userdata',required=True,
                help='path to user dataset geopackage')
ap.add_argument('-o','--output', default='/plot_outputs/',
                help='output directory for pickle')
args = vars(ap.parse_args())

# load pickle with extracted features in
print('[INFO] - Reading pickle in...')
df = pd.read_pickle(args['input'])

# load user data in
print('[INFO] - Reading geopackage in...')
userdf = gpd.read_file(args['userdata'])

# create columns for datetimes and seasons
print('[INFO] - Preparing user data for joining...')
userdf['date'] = pd.to_datetime(userdf['date_taken'], errors='coerce')
userdf['season'] = userdf['date'].apply(lambda dt: (dt.month%12 + 3)//3)

# get wanted user data columns
usercols = ['date', 'season','pid','user_id', 'country','gender','Local','Nimi']

# simplify userdata
userdf = userdf[usercols]

# rename columns
userdf = userdf.rename(columns={'Local':'local','Nimi':'parkname'})

# create string dicts for locals and seasons
locdict = {1:'National', 0:'International'}
seadict = {1:'Winter',2:'Spring',3:'Summer',4:'Autumn'}

# insert strings to user dataframe for better legibility
for i, row in userdf.iterrows():
    userdf.at[i, 'locstr'] = locdict[row['local']]
    userdf.at[i, 'seastr'] = seadict[row['season']]

# merge feature and user dataframes
print('[INFO] - Joining the dataframes...')
df = df.merge(userdf, left_on='photoid', right_on='pid')
print('[INFO] - Join complete! Size of the dataframe: {}'.format(df.shape))

# list parks in 4 landscape regions
laplist = ['Urho Kekkosen kansallispuisto', 'Pallas-Yllästunturin kansallispuisto', 'Pyhä-Luoston kansallispuisto']
eastlist = ['Oulangan kansallispuisto','Kolin kansallispuisto','Syötteen kansallispuisto','Hossan kansallispuisto', 'Riisitunturin kansallispuisto']
southlist = ['Nuuksion kansallispuisto', 'Sipoonkorven kansallispuisto', 'Helvetinjärven kansallispuisto','Seitsemisen kansallispuisto',
             'Repoveden kansallispuisto','Teijon kansallispuisto','Leivonmäen kansallispuisto','Hossan kansallispuisto','Liesjärven kansallispuisto']
archilist = ['Saaristomeren kansallispuisto','Selkämeren kansallispuisto','Tammisaaren saariston kansallispuisto']

# classify posts into landscape regions
for i, row in df.iterrows():
    if row['parkname'] in laplist:
        df.at[i, 'landscape_region'] = 'Lapland fells'
    elif row['parkname'] in eastlist:
        df.at[i, 'landscape_region'] = 'Eastern hills'
    elif row['parkname'] in southlist:
        df.at[i, 'landscape_region'] = 'Forests & lakes'
    elif row['parkname'] in archilist:
        df.at[i, 'landscape_region'] = 'Archipelago'

# save output
print('[INFO] - Saving results to pickle...')
df.to_pickle(args['output'])

print('[INFO] - ... done!')