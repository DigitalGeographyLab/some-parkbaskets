# -*- coding: utf-8 -*-
"""
Created on Thu Aug 29 10:25:00 2019

INFORMATION
===========
This script resizes the downloaded Flickr images and center crops them for
computer vision models. It returns an output directory structure and places
the center-cropped and resized images therein.

USAGE
=====
Run the script by running the following command:
    
    python3 resize_photos.py -i path/to/image/directory -o output/directory


@author: tuomvais
"""

from PIL import Image
from imutils import paths
import os
import numpy as np
import argparse 

# define arguments
ap = argparse.ArgumentParser()
ap.add_argument('-i','--input',required=True,
                help='path to input image directory')
ap.add_argument('-o','--output',required=True,
                help='path to output resized image directory')
args = vars(ap.parse_args())

# define function to crop image
def center_crop(img, new_width=None, new_height=None):        

    width = img.shape[1]
    height = img.shape[0]
    
    # if no desired width set the smaller value of initial size chosen
    if new_width is None:
        new_width = min(width, height)
    
    # if no desired heigth set the smaller value of initial size chosen
    if new_height is None:
        new_height = min(width, height)
    
    # set new sizes for left and right sides of image
    left = int(np.ceil((width - new_width) / 2))
    right = width - int(np.floor((width - new_width) / 2))
    
    # set new sizes for top and bottom sides of image
    top = int(np.ceil((height - new_height) / 2))
    bottom = height - int(np.floor((height - new_height) / 2))
    
    # center crop image
    if len(img.shape) == 2:
        center_cropped_img = img[top:bottom, left:right]
    else:
        center_cropped_img = img[top:bottom, left:right, ...]

    return center_cropped_img

# retrieve image paths
print('[INFO] - Retrieving all image paths in directory structure...')
imagePaths = list(paths.list_images(args['input']))

# extract park names for directory creation
print('[INFO] - Retrieving park names...')
parknames = []
for path in imagePaths:
    park = path.split(os.path.sep)[-2]
    parknames.append(park)

# create dirs for resized images
print('[INFO] - Creating directories for resized images...')
for park in parknames:
    target_path = os.path.join(args['output'], park)
    os.makedirs(target_path, exist_ok=True)

# initialize progress indicator
i = 1

# resize and keep aspect ration
print('[INFO] - Resizing and saving resized images...')
for path in imagePaths:
    
    print('[INFO] - Resizing ' + str(i) + '/' + str(len(imagePaths)) + ' image')
    # fetch park and file names
    park, fname = path.split(os.path.sep)[-2:]
    
    # open image
    img = Image.open(path)
    
    # resize and keep aspect ratio
    img.thumbnail((900,900),Image.ANTIALIAS)
    
    # convert to array
    img = np.array(img)
    
    # center crop the array
    img = center_crop(img)
    
    # convert back to image
    img = Image.fromarray(np.uint8(img))
    
    # save to file
    img.save(os.path.join(args['output'], park, fname))
    i += 1

print('[INFO] - ... done!')