[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.4282145.svg)](https://doi.org/10.5281/zenodo.4282145)

# Exploring human-nature interactions in national parks using social media photographs and computer vision
This repository contains Python scripts for the article *Exploring human-nature interactions in national parks using social media photographs and computer vision* published in Conservation Biology. The scripts use off-the-shelf computer vision models detect objects, extract features and classify scenes from social media photographs taken in Finnish national parks.

Follow the steps below to reproduce the results from the article or to adapt them to your own data. 

### Prerequisites
* A geopackage containing Flickr image URLs, e.g. from database which contains data collected from Flickr API using your own API credentials
* A computer with an NVIDIA GPU or access to one (you *can* run the scripts on a CPU, but it's **considerably slower**)
* Python 3: we recommend creating a virtual environment for installing the libraries required to run the scripts

### Directory contents
| Directory | Description |
| :-------- | :---------- |
| [preprocessing](preprocessing)   | Scripts for preprocessing of Flickr image data |
| [cv](cv) | Computer vision scripts |
| [processing](processing) | Processing scripts for the data |
| [plots](plots) | Scripts for plotting feature extraction results |
| [stats](stats) | Scripts for statistical analyses |

### Recommended running order of scripts
| Step | Script | Description | Input | Output |
| ---- | :----- | :---------- | :---- | :----- |
| 0 | [combine_data.py](preprocessing/combine_data.py) | Combines two existing datasets (not necessary if only one exists) | 2 geopackages | Combined geopackage without duplicates |
| 1 | [image_download.py](preprocessing/image_download.py) | Downloads images and removes posts with unavailable images | Geopackage with URLs | Image directory & geopackage without download errors |
| 2 | [photoid_match.py](preprocessing/photoid_match.py) | Double-checks geopackage reflects downloaded images | Geopackage | Geopackage |
| 3 | [resize_images.py](preprocessing/resize_images.py) | Resizes and center-crops images for computer vision | Image directory | Resized image directory |
| 4 | [extract_features.py](processing/extract_features.py) | Extracts high-dimensional semantic feature vectors from images with ResNeXt101 pre-trained with ImageNet | Resized image directory | Pickled dataframe |
| 5 | [join_userdata.py](pprocessing/join_userdata.py) | Joins manually annotated user data to photo id matched geopackage | User data CSV & output geopackage from step 2 | Pickled dataframe |
| 6 | [reduce_dimensions.py](processing/reduce_dimensions.py) | Performs semantic clustering of the data based on feature vectors | Output pickled dataframe from step 5 | Pickled dataframe, a sanity check plot |
| 7 | [predict_places365.py](cv/predict_places365.py) | Classifies image to a scene using VGG16-Places365 | Output pickled dataframe from step 6 | Pickled dataframe |
| 8 | [detect_objects.py](cv/detect_objects.py) | Detects objects in images with Mask r-CNN pre-trained with MS COCO | Output pickled dataframe from step 7 | Pickled dataframe |
| 9 | [plot scripts](plots) | Plot scripts for the plots used in the article | Output pickled dataframe from step 8 | Image files |
| 10 | [stats scripts](stats) | Statistical tests used in the article | Output pickled dataframe from step 8 | CSV results files |
