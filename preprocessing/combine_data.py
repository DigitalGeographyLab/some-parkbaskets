# -*- coding: utf-8 -*-
"""
Created on Fri Jul 19 13:24:44 2019

INFORMATION
===========

This unifies data structures of flickr data collected in January 2019 and data
collected earlier and extracts the unique photoids from the resulting data.
Finally it drops duplicates.


USAGE
=====
Run the script by running the following command:
    
    python3 combine_data.py -df yourdata.gpkg -df2 yourdata2.gpkg -o path/to/file.gpkg


@author: tuomvais
"""

import geopandas as gpd
import pandas as pd
import argparse


# Set up the argument parser
ap = argparse.ArgumentParser()

# Define the path to input file
ap.add_argument("-df", "--dataframe", required=True,
                help="Path to new geopacakge")

# Define the path to output directory
ap.add_argument("-df2", "--dataframe2", required=True,
                help="Path to the old geopackage")

# Define the preprocessing strategy
ap.add_argument("-o", "--output", required=True,
                help="Path to output file.")

# Parse arguments
args = vars(ap.parse_args())

# read files in
print('[INFO] - Reading geopackages in...')
df = gpd.read_file(args['dataframe'])
df2 = gpd.read_file(args['dataframe2'])

# function to extract photoid from filename
def pid_extract(row):
    elements = row.split('_')
    photoid = elements[0]
    return photoid

# run function on dataframe with no photoid
print('[INFO] - Extracting photo ids..')
df['photoid'] = df['filename'].apply(pid_extract)

# convert photoid to numeric
df['photoid'] = pd.to_numeric(df['photoid'])

# unify dataframe structure
dflist = ['id','title','description','date_taken','photo_url','lat','lon','user_id','user_name','photoid','geometry']
df2list = ['id','text','photo_description','photoid','time_local','photourl','lat','lon','userid','username','geometry']

# establish renaming scheme
renamedict = {'text':'title',
              'photo_description':'description',
              'time_local':'date_taken',
              'photourl':'photo_url',
              'userid':'user_id',
              'username':'user_name'}

# simplify dataframes
print('[INFO] - Unifying the geodataframe column structure')
simp_df = df[dflist]
simp_df2 = df2[df2list]

# rename columns
simp_df2 = simp_df2.rename(columns=renamedict)

# join dataframes
ext_df = simp_df.append(simp_df2, ignore_index=True)

# drop duplicates
print('[INFO] - Dropping duplicate posts...')
ext_df = ext_df.drop_duplicates(subset='photoid')

# save output to file
print('[INFO] - Saving results to geopackage...')
ext_df.to_file(args['output'], driver='GPKG')

print('[INFO] - ... done!')