'''This file contains functions for rendering related purposes'''

from PIL import ImageTk, Image
import time, numpy, os
from settings import *

#Convert

def imageToArray(img:Image):
    '''Converts an Image into a numpy array'''
    return numpy.array(img)

def arrayToImage(array:numpy.ndarray):
    '''Converts a numpy array to an Image'''
    return Image.fromarray(array.astype("uint8"), "RGBA")

def saveImage(array:numpy.ndarray, output_path):
    img = Image.fromarray(array)
    img.save(output_path)

# Image

def merge(img1:Image.Image|numpy.ndarray, img2:Image.Image|numpy.ndarray):
    '''Returns an array of the average of the values of two given images/numpy arrays as a numpy array'''
    img1 = numpy.array(img1)
    img2 = numpy.array(img2)
    return img1 // 2 + img2 // 2

def placeOver(img1:numpy.ndarray, img2:numpy.ndarray, position:list|tuple, center = False):
    '''Modifies image 1 (background) as an array of image 2 (overlay) placed on top of image 1 (background), given as numpy arrays'''
    if center:
        position = (round(position[0]-img2.shape[1]*0.5),round(position[1]-img2.shape[0]*0.5))
    img1H = img1.shape[0] 
    img1W = img1.shape[1]
    img2H = img2.shape[0] 
    img2W = img2.shape[1]

    if position[1]>img1H or -position[1]>img2H:
        return False
    if position[0]>img1W or -position[0]>img2W:
        return False
    
    startX = max(position[0], 0)
    startY = max(position[1], 0)
    endX = min(position[0]+img2W, img1W)
    endY = min(position[1]+img2H, img1H)

    img2 = img2[max(-position[1], 0):(max(-position[1], 0)+(endY-startY)), max(-position[0], 0):(max(-position[0], 0)+(endX-startX))]

    alpha_overlay = img2[:, :, 3] / 255.0
    overlayRGB = img2[:, :, :3]
    backgroundRGB = img1[startY:endY, startX:endX, :3]

    blendedRGB = (overlayRGB*alpha_overlay[:, :, None]+backgroundRGB*(1-alpha_overlay[:, :, None])).astype(numpy.uint8)    
    img1[startY:endY, startX:endX, :3] = blendedRGB
    return True

def dPlaceOver(img1:numpy.ndarray, img2: numpy.ndarray, position:list|tuple):
    '''Dangerously returns an overlayed version of image 1 (background) as an array of image 2 (overlay) placed on top of image 1 (background), given as numpy arrays, by directly adding it'''
    if img1.shape == img2.shape:
        img1 += img2
    else:
        try:
            img2 = numpy.hstack([numpy.zeros((img2.shape[0],position[0],4),numpy.uint8),img2])
            img2 = numpy.hstack([img2, numpy.zeros((img2.shape[0],img1.shape[1]-img2.shape[1],4),numpy.uint8)])
            img2 = numpy.vstack([numpy.zeros((position[1],img2.shape[1],4),numpy.uint8),img2])
            img2 = numpy.vstack([img2, numpy.zeros((img1.shape[0]-img2.shape[0],img2.shape[1],4),numpy.uint8)])
            img1 += img2
        except:
            '''So, you really messed up... told you it was dangerous...'''
            pass