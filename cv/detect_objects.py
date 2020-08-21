'''

INFORMATION
===========

This script detects objects in images using Mask r-CNN pre-trained on COCO
dataset. It requires that you have a pickled dataframe with paths to images
stored and installed Mask r-CNN (see below) with the appropriate weights and
labels files.

The script outputs a pickled dataframe containing object detections, confidences
unique objects and object counts.


USAGE
=====

Run this script by typing:
    python detect_objects.py -w file.h5 -l file.txt -i input.pkl -o output.pkl


NOTES
=====

This script is a lightly modified version of the Mask r-CNN scripts
from https://www.pyimagesearch.com/2019/06/10/keras-mask-r-cnn/ to better
suit the purposes of our article.

Running this script with a GPU is recommended as it speeds up the detection
considerably.


INSTALL MASK R-CNN
==================

To use this script you have to clone and install the Mask r-CNN repository
by typing:
    
    git clone https://github.com/matterport/Mask_RCNN.git
    cd Mask_RCNN
    python setup.py install

@author: Adrian Rosebrock of PyImageSearch, Tuomas Väisänen

'''

# import the necessary packages
from mrcnn.config import Config
from mrcnn import model as modellib
import pandas as pd
import progressbar
import colorsys
import argparse
import imutils
import random
import cv2
import os

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-w", "--weights", required=True,
	help="path to Mask R-CNN model weights pre-trained on COCO")
ap.add_argument("-l", "--labels", required=True,
	help="path to class labels file")
ap.add_argument("-i", "--input", required=True,
	help="path to input dataframe to apply Mask R-CNN to")
ap.add_argument("-o", "--output", required=True,
	help="path to output pickle")
args = vars(ap.parse_args())

# load the class label names from disk, one label per line
CLASS_NAMES = open(args['labels']).read().strip().split("\n")

# generate random (but visually distinct) colors for each class label
# (thanks to Matterport Mask R-CNN for the method!)
hsv = [(i / len(CLASS_NAMES), 1, 1.0) for i in range(len(CLASS_NAMES))]
COLORS = list(map(lambda c: colorsys.hsv_to_rgb(*c), hsv))
random.seed(42)
random.shuffle(COLORS)

# configuration of Mask r-CNN
class SimpleConfig(Config):
    
	# give the configuration a recognizable name
	NAME = "coco_inference"

	# set the number of GPUs to use along with the number of images
	# per GPU
	GPU_COUNT = 1
	IMAGES_PER_GPU = 1

	# number of classes (we would normally add +1 for the background
	# but the background class is *already* included in the class
	# names)
	NUM_CLASSES = len(CLASS_NAMES)

# initialize the inference configuration
config = SimpleConfig()

# initialize the Mask R-CNN model for inference and then load the weights
print("[INFO] - loading Mask R-CNN model...")
model = modellib.MaskRCNN(mode="inference", config=config,
	model_dir=os.getcwd())
model.load_weights(args['weights'], by_name=True)

# read pickle in
df = pd.read_pickle(args['input'])

# reset index from umap clustering
df = df.reset_index(drop=True)

# grab list of imagepaths
print('[INFO] - Loading image paths..')
imagePaths = df['imagepath'].values.tolist()

# initialize progressbar widgets
widgets = ['Predicting objects: ',
           progressbar.Percentage(),' ', progressbar.Bar(), ' ', progressbar.ETA()]

# start progressbar
pbar = progressbar.ProgressBar(maxval=len(df), widgets=widgets).start()

# empty list for predictions
predprobs = []

# loop over images in batches
for i in range(len(imagePaths)):
    # get path of image
    imagePath = df['imagepath'][i]
    
    # load input image
    image = cv2.imread(imagePath)
    
    # convert color scheme to RGB
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # resize to 512 x 512
    image = imutils.resize(image, width=512)
    
    # detect objects in image
    predictions = model.detect([image])
        
    # loop predictions
    for pred in predictions:
        
        # empty list for detected objects
        objects = []
        
        # get detected objects and append to list
        for c in pred['class_ids']:
            obj = CLASS_NAMES[c]
            objects.append(obj)
        
        # empty list for prediction confidences
        probs = []
        
        # get detection confidences and append to list
        for p in pred['scores']:
            probs.append(p)
        
        # combine detections with confidences and append to list
        preds = list(zip(objects, probs))
        predprobs.append(preds)
    
    # update progress
    pbar.update(i)

# save predictions to dataframe
df['obj_preds'] = predprobs

# finish progressbar
pbar.finish()
print("[INFO] - Object detection done!")

# count objects per picture
print("[INFO] - Saving detection results to dataframe...")
for i, row in df.iterrows():
    df.at[i, 'obj_count'] = len(row['obj_preds'])

# empty list for detected objects
detobjs = []

# get objects and append to list
for i, row in df.iterrows():
    objs = [x[0] for x in row['obj_preds']]
    detobjs.append(objs)

# save detected objects to dataframe
df['detected_objs'] = detobjs

# empty list for unique objects
uniqlist = []

# get unique objects and append to list
for i, row in df.iterrows():
    uniq = set(row['detected_objs'])
    uniqlist.append(uniq)

# save unique objects to dataframe
df['unique_objs'] = uniqlist

# count unique objects per picture
for i, row in df.iterrows():
    df.at[i, 'unique_obj_count'] = len(row['unique_objs'])

# save dataframe
df.to_pickle(args['output'])
print("[INFO] - ... done!")