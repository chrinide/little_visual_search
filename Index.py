# -*- coding: utf-8 -*-
"""
Created on Sun Nov  1 10:29:47 2015

@author: sl001093
"""

#Import the necessary packages
import RGBHistogram
import argparse
import cPickle #For dumping our index to disk
import glob #Get the paths of the images we are going to index
import cv2

#Construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-d","--dataset",required = True,help="Path to the directory that contains the images to be indexed")
ap.add_argument("-i","--index",required=True,help = "Path to where the computed index will be stored")
args=vars(ap.parse_args())

# initialize the index dictionary to store our our quantifed
# images, with the 'key' of the dictionary being the image
# filename and the 'value' our computed features
index = {}

# initialize our image descriptor -- a 3D RGB histogram with
# 8 bins per channel
desc=RGBHistogram.RGBHistogram([8,8,8]) #USe 8 bins for each RGB channel

#Use glob to grab the image paths and loop over them
for imagePath in glob.glob(args["dataset"] + "/*.png"):
    #extract our inique image ID (i.e the filename)
    k = imagePath[imagePath.rfind("/")+ 1:] #We extract the “key” for our dictionary. 
    #All filenames are unique in this sample dataset, so the filename itself will be enough to serve as the key.
    
    #Load the image, describe it using our RGB histogram
    #descriptor, and update the index
    image=cv2.imread(imagePath)
    features=desc.describe(image)
    index[k]=features
    
# we are now done indexing our image -- now we can write our
# index to disk
f=open(args["index"],"w")
f.write(cPickle.dumps(index))
f.close()