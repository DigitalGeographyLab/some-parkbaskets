# -*- coding: utf-8 -*-
"""
Created on Fri Aug 16 15:07:45 2019

INFORMATION
===========

This script extracts features from Flickr images with ResNeXt101 pretrained with
ImageNet and saves results into a pickled dataframe. The dataframe will also
contain the file paths to the images.


USAGE
=====

Run script by typing
    python extract_features.py -i path/to/image/directory/ -o outputfile.pkl -b 32


@author: Tuomas Väisänen
"""

from keras.preprocessing.image import img_to_array 
from keras.preprocessing.image import load_img
from keras.layers import Input
from imutils import paths
import numpy as np
import pandas as pd
import progressbar
import argparse
import os
import keras
from keras_applications.resnext import ResNeXt101, preprocess_input

# define arguments
ap = argparse.ArgumentParser()
ap.add_argument('-i','--input',required=True,
                help='path to input image directory')
ap.add_argument('-o','--output',required=True,
                help='path to output pickled dataframe')
ap.add_argument('-b','--batchsize', type=int, default=32,
                help='batch size of images to be passed through network, default 32')
args = vars(ap.parse_args())

# store the batch size in a convenience variable
bs = args['batchsize']

# input shape for resnext models
inp = Input(shape=(224,224,3))

# load model
model = ResNeXt101(input_tensor=inp, include_top=False, weights='imagenet',
                   backend=keras.backend, layers=keras.layers,
                   models=keras.models, utils=keras.utils, pooling='max')
print('[INFO] - ResNeXt101 trained on ImageNet loaded!')

# grab list of image paths
print('[INFO] - Loading images..')
imagePaths = list(paths.list_images(args['input']))

# message about defining the result dataframe
print('[INFO] - Defining dataframe..')

# create column names according to output dimensionality
featurecols = ['feature'+str(i) for i in range(model.output.shape[1].value)]

# create empty dataframe
df = pd.DataFrame(None, columns=featurecols)

# add image paths to dataframe
df['imagepath'] = imagePaths

# extract the filenames and photo ids from the image paths
print('[INFO] - Extracting unique photo ids..')
fnames = [p.split(os.path.sep)[-1] for p in imagePaths]

# empty list to append photo ids to
pids = []

# loop over image paths to extract photoids
for f in fnames:
    
    # remove trailing size and format strings
    f = f[:-6] 
    
    # append the photo id to list
    pids.append(f)

# add file names and photo ids to dataframe
df['filename'] = fnames
df['photoid'] = pids

# initialize progressbar
widgets = ['Extracting features with ImageNet pre-trained model: ',
           progressbar.Percentage(),' ', progressbar.Bar(), ' ', progressbar.ETA()]

# start progressbar
pbar = progressbar.ProgressBar(maxval=len(imagePaths), widgets=widgets).start()

# empty feature feature list
features = []

# loop over images in batches
for i in np.arange(0, len(imagePaths), bs):
    
    # extract batch of images and labels then initialize the list of actual images
    # that will be passed through the network for feature extraction
    batchPaths = df['imagepath'][i:i + bs].values.tolist()
    batchLabels = df['photoid'][i:i + bs].values.tolist()
    batchImages = []
    
    for (j, imagePath) in enumerate(batchPaths):
        
        # load input image and resize to 224x224
        image = load_img(imagePath, target_size=(224,224))
        
        # convert to array
        image = img_to_array(image)
        
        # preprocess image by expanding dimensions and subtracting mean RGB pixel
        # intensity from ImageNet
        image = np.expand_dims(image, axis=0)
        image = preprocess_input(image, data_format='channels_last')
        
        # add the image to the batch
        batchImages.append(image)
        
    # vertically stack the batch images
    batchImages = np.vstack(batchImages)
    
    # pass the batch images through network to get image features
    batchFeatures = model.predict(batchImages, batch_size=bs)
    
    # add features and labels to dataset
    features.extend(batchFeatures)
    
    # update progressbar
    pbar.update(i)

# finish progressbar
pbar.finish()

# add extracted features to dataframe
print('[INFO] - Updating dataframe with extracted features')
df[featurecols] = features

# Save dataframe to pickle
df.to_pickle(args['output'])

print('[INFO] - .. done!')