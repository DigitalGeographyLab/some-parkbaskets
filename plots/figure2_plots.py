# -*- coding: utf-8 -*-
"""
Created on Wed Feb 12 12:21:34 2020

INFORMATION
===========

This script plots two figures that comprise Figure 2 of the article:
    - scatterplot of UMAP results across landscape regions
    - minithumbnail scatterplot of the images

USAGE
=====

Run the script by typing:
    python figure2_plots.py -i pickle.pkl -o fig2.png -ot fig2_thumb.png

NOTE
====

This script does not replicate Figure 2 from article, but its parts. To replicate
Figure 2 you have to copy the thumbnail image onto the landscape scatterplot
using Photoshop, GIMP or similar software.

@author: Tuomas Väisänen
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import cv2
import numpy as np
import argparse

# define arguments
ap = argparse.ArgumentParser()
ap.add_argument('-i','--input',required=True,
                help='path to input pickle')
ap.add_argument('-o','--output',required=True,
                help='path to output png')
ap.add_argument('-ot','--outthumb',required=True,
                help='path to output thumbnail png')

args = vars(ap.parse_args())

# read pickle in
print("[INFO] - Reading data in...")
df = pd.read_pickle(args['input'])

# plot UMAP points by landscape regions
print("[INFO] - Plotting scatterplot...")
plt.figure(figsize=(15,12))
sns.set(font_scale=1.4)
sns.set_style('white')
ax = sns.scatterplot(
        x="umap-2d-one", y="umap-2d-two",
        hue="landscape_region",
        hue_order=['Lapland fells', 'Eastern hills', 'Forests & lakes', 'Archipelago'],
        palette=['grey', 'orange', 'green', 'blue'],
        data=df,
        legend="brief",
        alpha=0.6)
handles,labels = ax.get_legend_handles_labels()
ax.legend(handles[1:],labels[1:],loc=2, title='Landscape region')
plt.tight_layout()
plt.savefig(args['output'], bbox_inches='tight')

# function for thumbnail scatterplot
def visualize_scatter_with_images(dataframe, x, y, figsize=(55,50), image_zoom=1):
    
    # initialize the subplot
    fig, ax = plt.subplots(figsize=figsize)
    
    # empty list for artists
    artists = []
    
    # loop over the UMAP coordinates and imagepaths
    for x0, y0, path in zip(dataframe[x].values, dataframe[y].values, dataframe['imagepath']):
        
        # read image
        img = cv2.imread(path, cv2.IMREAD_COLOR)
        
        # convert to RGBA color space
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)
        
        # resize to small size
        img = cv2.resize(img, (35,35))
        
        # uncomment to make image transparent 
        #img[:,:,3] = 185
        
        # convert to offsetimage
        img = OffsetImage(img, zoom=image_zoom)
        
        # store image and location information
        ab = AnnotationBbox(img, (x0, y0), xycoords='data', frameon=False)
        
        # append image and location information to list
        artists.append(ax.add_artist(ab))
    
    # set xy limits for plot
    ax.update_datalim(np.column_stack((dataframe[x].values, dataframe[y].values)))
    
    # autoscale the axis
    ax.autoscale()
    
    # show figure
    plt.show()
    
    # save figure
    plt.savefig(args['outthumb'], bbox_inches='tight')

# run thumbnail plot
print("[INFO] - Plotting thumbnail scatterplot...")
visualize_scatter_with_images(df, x='umap-2d-one', y='umap-2d-two')

print("[INFO] - ... done!")