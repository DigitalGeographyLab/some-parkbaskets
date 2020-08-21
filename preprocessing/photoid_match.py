# -*- coding: utf-8 -*-
"""
Created on Mon Aug 12 10:05:14 2019

INFORMATION
===========

This script checks which images were succesfully retrieved from Flickr and
saves a geopackage that reflects the succesful retrievals.


USAGE
=====
Run the script by running the following command:
    
    python3 photoid_match.py -i yourdata.gpkg -o output/directory/ -gp yourdata2.gpkg


@author: tuomvais
"""

import glob
import geopandas as gpd
import argparse


# Set up the argument parser
ap = argparse.ArgumentParser()

# Define the path to input file
ap.add_argument("-i", "--input", required=True,
                help="Path to geopackage file")

# Define the path to output directory
ap.add_argument("-img", "--imgpath", required=True,
                help="Path to image root directory.")

# Define the preprocessing strategy
ap.add_argument("-gp", "--geopackage", required=True,
                help="Name of the geopackage file to be saved")

# Parse arguments
args = vars(ap.parse_args())

imgpath = args['imgpath']

# retrieve image paths to list
print('[INFO] - Retrieving all images in directory structure...')
imgfiles = glob.glob(imgpath + '\*\*.jpg')

# list of retrieved photoids
retphotos = []

# retrieve returned photoids
for imgpath in imgfiles:
    pid = imgpath.split('\\')[-1]
    pid = pid[:-6]
    retphotos.append(pid)

# read posts dataframe in
print('[INFO] - Reading geopackage in...')
df = gpd.read_file(args['input'])

# list for wrong image sizes
wsizes = ['_o.jpg', '_o.png', '_o.tif', '_m.jpg','_s.jpg','_q.jpg','_t.jpg','_n.jpg','_z.jpg','_c.jpg']

# empty list for all photo ids of downloaded images
pidlist = []

# loop over dataframe
print('[INFO] - Fetching photo ids')
for i, row in df.iterrows():
    pid = row['photo_url'].split('/')[-1]
    if any(imgsize in pid for imgsize in wsizes):
        pid = pid[:-6]
        pidlist.append(pid)
    else:
        pid = pid[:-4]
        pidlist.append(pid)
    
# create full photoid column
df['pid'] = pidlist

# remove posts with missing photos
print('[INFO] - Dropping images not present in the directories..')
df = df[df['pid'].isin(retphotos)]

# save trimmed df to file
print('[INFO] - Saving to geopackage...')
df.to_file(args['geopackage'], driver='GPKG')

print('[INFO] - ... done!')
