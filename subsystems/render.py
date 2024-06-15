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
    '''Returns the average of the values of two given images/numpy arrays as a numpy array'''
    img1 = numpy.array(img1)
    img2 = numpy.array(img2)
    return img1 // 2 + img2 // 2

def placeOver(img1:Image.Image|numpy.ndarray, img2:Image.Image|numpy.ndarray, position:list|tuple):
    '''Returns an array of image 2 (overlay) placed on top of image 1 (background)'''
    img1 = numpy.array(img1)
    img2 = numpy.array(img2)
    x, y = position
    img1H, img1W, temp = img1.shape
    img2H, img2W, temp = img2.shape

    if position[1] > img1H or -position[1] > img2H:
        return img1
    if position[0] > img1W or -position[0] > img2W:
        return img1
    
    startX = max(x, 0)
    startY = max(y, 0)
    endX = min(x + img2W, img1W)
    endY = min(y + img2H, img1H)

    img2startX = max(-x, 0)
    img2startY = max(-y, 0)
    img2endX = img2startX + (endX - startX)
    img2endY = img2startY + (endY - startY)
    img2 = img2[img2startY:img2endY, img2startX:img2endX]

    alpha_overlay = img2[:, :, 3] / 255.0
    overlayRGB = img2[:, :, :3]
    backgroundRGB = img1[startY:endY, startX:endX, :3]

    blendedRGB = (overlayRGB * alpha_overlay[:, :, None] + backgroundRGB * (1 - alpha_overlay[:, :, None])).astype(numpy.uint8)    
    result = img1.copy()
    result[startY:endY, startX:endX, :3] = blendedRGB
    return result