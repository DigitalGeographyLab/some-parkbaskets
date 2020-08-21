# -*- coding: utf-8 -*-
"""
Created on Thu Sep 19 13:21:21 2019

INFORMATION
===========

This script classifies an image to a probable scene type using a VGG16 model
pre-trained on Places365-standard dataset. The script returns a pickle with
three most confidently identified scenes with confidence scores. The pre-trained
model is provided by Grigorios Kalliatakis at:
    https://github.com/GKalliatakis/Keras-VGG16-places365.

In order to run, the script requires the model available from repository
mentioned above and a pickle containing filepaths to image files.

USAGE
=====

Run script by typing:
    python predict_places365.py -i input.pkl -o output.pkl -b 32

@author: tuomvais
"""

import os
import progressbar
import pandas as pd
import numpy as np
from vgg16_places_365 import VGG16_Places365
from places_utils import preprocess_input
from keras.preprocessing.image import img_to_array 
from keras.preprocessing.image import load_img
import argparse

# define arguments
ap = argparse.ArgumentParser()
ap.add_argument('-i','--input',required=True,
                help='path to input pickle')
ap.add_argument('-o','--output',required=True,
                help='path to output pickle')
ap.add_argument('-b','--batchsize', type=int, default=32,
                help='batch size of images to be passed through network, default 32')
args = vars(ap.parse_args())

# read pickle in
print('[INFO] - Reading pickle in')
df = pd.read_pickle(args['input'])

# reset index from umap clustering
df = df.reset_index(drop=True)

# initialize model
model = VGG16_Places365(weights='places')

# grab list of imagepaths
print('[INFO] - Loading images..')
imagePaths = df['imagepath'].values.tolist()

# download classlabels if not present in directory
file_name = 'categories_places365.txt'
if not os.access(file_name, os.W_OK):
    print('[INFO] - Downloading class label file')
    synset_url = 'https://raw.githubusercontent.com/csailvision/places365/master/categories_places365.txt'
    os.system('wget ' + synset_url)

# empty list for classes
classes = list()

# open class label file and append to list
with open(file_name) as class_file:
    for line in class_file:
        classes.append(line.strip().split(' ')[0][3:])

# convert to tuple
classes = tuple(classes)

# define batch size
bs = args['batchsize']

#initialize progressbar
widgets = ['Predicting scene categories: ',
           progressbar.Percentage(),' ', progressbar.Bar(), ' ', progressbar.ETA()]

# start progressbar
pbar = progressbar.ProgressBar(maxval=len(df), widgets=widgets).start()

# empty list for predictions
predictions = []

# loop over images in batches
print('[INFO] - Starting scene prediction...')
for i in np.arange(0, len(imagePaths), bs):
    
    # extract batch of images and labels then initialize the list of actual images
    # that will be passed through the network for feature extraction
    batchPaths = df['imagepath'][i:i + bs].values.tolist()
    batchLabels = df['photoid'][i:i + bs].values.tolist()
    batchImages = []
    
    # loop over paths of images in batch
    for (j, imagePath) in enumerate(batchPaths):
        
        # load input image and resize to 224x224
        image = load_img(imagePath, target_size=(224,224))
        
        # convert to array
        image = img_to_array(image)
        
        # preprocess image by expanding dimensions and subtracting mean RGB pixel
        # intensity
        image = np.expand_dims(image, axis=0)
        image = preprocess_input(image)
        
        # add the image to the batch
        batchImages.append(image)
        
    # vertically stack images
    batchImages = np.vstack(batchImages)
    
    # pass the batch images through network and get predictions
    batchPredictions = model.predict(batchImages, batch_size=bs)
    
    # loop over predictions
    for preds in batchPredictions:
        
        # empty list to hold predictions
        predlist = []
        
        # get top 3 predictions
        top_preds = np.argsort(preds)[::-1][0:3]
        
        # loop over top 3 predictions
        for p in top_preds:
            
            # get classes
            imgclass = classes[p]
            
            # get confidences and round to 3 decimals
            prob = round(preds[p], 3)
            
            # convert to tuple of class and confidence
            predprob = (imgclass, prob)
            
            # append tuple to prediction list
            predlist.append(predprob)
            
        # append image predictions to list of all predictions
        predictions.append(predlist)
    
    # update progressbar
    pbar.update(i)

# save predictions to dataframe
df['scenepreds'] = predictions

# finish progressbar
pbar.finish()
print('[INFO] - Predictions saved to dataframe')

# get best predictions
for i in range(len(df)):
    df.at[i, 'scenecat'] = df.at[i, 'scenepreds'][0][0]
    df.at[i, 'sceneprob'] = df.at[i, 'scenepreds'][0][1]

# save dataframe
print('[INFO] - Saving results to pickle...')
df.to_pickle(args['output'])

print('[INFO] - ... done!')