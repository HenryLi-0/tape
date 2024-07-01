'''This file contains functions for rendering related purposes'''

from PIL import ImageTk, Image, ImageEnhance
import numpy, math
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
    if center: position = (round(position[0]-img2.shape[1]*0.5),round(position[1]-img2.shape[0]*0.5))
    img1H = img1.shape[0] 
    img1W = img1.shape[1]
    img2H = img2.shape[0] 
    img2W = img2.shape[1]

    if position[1]>img1H or -position[1]>img2H: return False
    if position[0]>img1W or -position[0]>img2W: return False
    
    startX = math.floor(max(position[0], 0))
    startY = math.floor(max(position[1], 0))
    endX = math.floor(min(position[0]+img2W, img1W))
    endY = math.floor(min(position[1]+img2H, img1H))

    img2 = img2[round(max(-position[1], 0)):round((max(-position[1], 0)+(endY-startY))), round(max(-position[0], 0)):round((max(-position[0], 0)+(endX-startX)))]

    alpha_overlay = img2[:, :, 3] / 255.0
    overlayRGB = img2[:, :, :3]
    backgroundRGB = img1[startY:endY, startX:endX, :3]

    blendedRGB = (overlayRGB*alpha_overlay[:, :, None]+backgroundRGB*(1-alpha_overlay[:, :, None])).astype(numpy.uint8)    
    img1[startY:endY, startX:endX, :3] = blendedRGB
    return True

def dPlaceOver(img1:numpy.ndarray, img2: numpy.ndarray, position:list|tuple):
    '''Dangerously returns an overlayed version of image 1 (background) as an array of image 2 (overlay) placed on top of image 1 (background), given as numpy arrays, by directly adding it'''
    if img1.shape == img2.shape: img1 += img2
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

def rotateDeg(img: numpy.ndarray, degrees:float):
    '''Returns an array of a rotated version of the given image by (degrees) degrees, using the 0 up CCW rotation system'''
    return numpy.array(Image.fromarray(img).rotate(degrees,expand=True))

def setSize(img: numpy.ndarray, size):
    '''Returns a copy of the given image scaled by size, given the size change (given with 100 as normal, >100 scale up, <100 scale down)'''
    x, y, temp = img.shape
    return numpy.array(Image.fromarray(img).resize((round(x*size/100),round(y*size/100))))

def setColorEffect(img: numpy.ndarray, colorEffect):
    '''Returns a copy of the given image with a color shift, given the shift value (given 0-100)'''
    imgc = img.copy()
    imgc[:, :, 0:2] += numpy.uint8(colorEffect/100*255)
    return imgc

def setTransparency(img: numpy.ndarray, transparency):
    '''Returns a copy of the given image with transparency multiplied, given the transparency value (given 0-100, 0 = clear, 100 = normal)'''
    imgc = img.copy()
    imgMask = imgc[:, :, 3] * (transparency/100)
    imgc[:, :, 3] = imgMask
    return imgc

def setBrightness(img: numpy.ndarray, brightness):
    '''Returns a copy of the given image with brightness changed, given the brightness value (>0 = brighter, <0 = darker)'''
    imgc = ImageEnhance.Brightness(Image.fromarray(img))
    imgc = imgc.enhance((brightness+100)/100)
    return numpy.array(imgc)

def setPixelation(img: numpy.ndarray, pixelation):
    '''Returns a copy of the given image pixelated, given the pixelation value (given 0-100, 0 = normal, 100 = very pixelated)'''
    if pixelation <= 1: return img
    x, y, temp = img.shape
    imgc = numpy.array(Image.fromarray(img).resize((round(x/pixelation*(x/100)),round(y/pixelation*(x/100)))))
    return numpy.array(Image.fromarray(imgc).resize((round(x),round(y))))