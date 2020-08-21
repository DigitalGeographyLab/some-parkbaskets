# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 14:23:00 2019

INFORMATION
===========

This script reads a geopackage file containing links to Flickr images,
downloads the images at the highest standard resolution and divides
them into directories corresponding to Finnish national parks.

The script returns a directory with Flickr images and a geopackage containing
posts with available images. Images that have been removed, set to private or
are otherwise inaccessible are not included in the resulting geopackage.


USAGE
=====
Execute the script by running the following command:
    
    python3 image_download.py -i yourdata.gpkg -o output/directory/ -gp yourdata2.gpkg

NOTE
====

@author: tuomvais
"""

import geopandas as gpd
import urllib
import os
import time
import random
import argparse


# Set up the argument parser
ap = argparse.ArgumentParser()

# Define the path to input file
ap.add_argument("-i", "--input", required=True,
                help="Path to geopackage file")

# Define column with park names
ap.add_argument("-pn", "--parkname", required=True,
                help="Column containing parknames in geopackage")

# Define the path to output directory
ap.add_argument("-o", "--outpath", required=True,
                help="Path to the output directory.")

# Define the preprocessing strategy
ap.add_argument("-gp", "--geopackage", required=True,
                help="Name of the geopackage file to be saved")

# Parse arguments
args = vars(ap.parse_args())

# resulting file path
outgp = args['outpath'] + args['geopackage']

# read file in
print('[INFO] - Reading geopackage in...')
df = gpd.read_file(args['input'])

# make list of parknames and urls
imglist = list(zip(df[args['parkname']] ,df.photo_url))

# set up error journal to track lost posts/images
errorlist = []

# set up running progress indicator numbers
i = 1
imgcount = len(imglist) 

# list for wrong image sizes from flickr.photos.getSizes
wsizes = ['_o.jpg', '_o.png', '_o.tif', '_m.jpg','_s.jpg','_q.jpg','_t.jpg','_n.jpg','_z.jpg','_c.jpg']

# loop over parks and image urls
print('[INFO] - Starting image download...')
for park, imgurl in imglist:
    
    # generate random wait time to not get blocked by Flickr
    randwait = round(random.uniform(0.9, 1.8),1)
    
    # create directory structure and download images
    try:
        # first 6 chars of park name
        park = park[0:6]
        
        # create park specific directories
        if not os.path.exists(args['outpath'] + park):
            os.makedirs(args['outpath'] + park)
        
        # extract original filename
        fname = imgurl.split('/')[-1]
        
        # set filenames to match 1024 x 768 size images
        if any(imgsize in fname for imgsize in wsizes):
            fname = fname[:-6] + '_b.jpg'
        else:
            fname = fname[:-4] + '_b.jpg'
            
        # set flickr image urls to download 1024 x 768 size images
        if any(imgsize in imgurl for imgsize in wsizes):
            imgurl = imgurl[:-6] + '_b.jpg'
        else:
            imgurl = imgurl[:-4] + '_b.jpg'
        
        # download image to park specific directory
        file = urllib.request.urlretrieve(imgurl, args['outpath'] + '{0}\{1}'.format(park,fname))
        print('[INFO] - ' + str(i) + '/' + str(imgcount) +' image saved')
        
        # sleep to not get disconnected by Flickr
        time.sleep(randwait)
        
        # update progress indicator
        i += 1
        
        # check if errors have occurred
        if len(errorlist) > 0:
            
            # log errors into txt file
            with open(args['outpath'] + "flickr_errors.txt", "w") as output:
                output.write(str(errorlist))
    
    # catch errors and continue without waiting
    except urllib.error.HTTPError as e:
        
        # save error type and file name
        error_element = {"error": e, "file": fname}
        
        # append error to list
        errorlist.append(error_element)
        print('[INFO] - ' + str(e) + ' -- Total images lost: ' + str(len(errorlist)))
        
        # update progress indicator
        i += 1
        continue

# inform about ending of downloads
print('[INFO] - Available images downloaded!')

# create a list of photoids with error messages
epl = []

# loop over errors
print('[INFO] - Removing posts with errors in photo retrieval...')
for error in errorlist:
    
    # get photo id of error file
    photoid = error['file:'][:-6]
    
    # append error photo id to list
    epl.append(photoid)
    
# create empty photoid list
pidlist = []

# loop over parks and urls
for park, imgurl in imglist:
    
    # retrieve photo id
    pid = imgurl.split('/')[-1]
    
    # format photo id
    if any(imgsize in pid for imgsize in wsizes):
        pid = pid[:-6]
    else:
        pid = pid[:-4]
    
    # append photo id to list
    pidlist.append(pid)

# create full photoid column
df['pid'] = pidlist

# remove posts with missing photos
df = df[~df['pid'].isin(epl)]
print('[INFO] - Posts with missing photos removed!')

# save trimmed df to file
print('[INFO] - Saving to geopackage...')
df.to_file(outgp, driver='GPKG')

print('[INFO] - ... done!')