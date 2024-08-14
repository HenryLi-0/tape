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

def clip(img:Image.Image|numpy.ndarray, cliplen: int, direction: str):
    '''Returns an image with clipped cliplen from a given direction'''
    img = numpy.array(img)
    cliplen = round(cliplen)
    if   direction == "N": return img[cliplen:, :, :]
    elif direction == "S": return img[:-cliplen, :, :]
    elif direction == "E": return img[:, cliplen:, :]
    elif direction == "W": return img[:, :-cliplen, :]
    else: return img

def addBlank(img:Image.Image|numpy.ndarray, add: int, direction: str, color = (0,0,0,0), thirdaxis = True):
    '''Returns the image with added add "empty" pixels in a given direction'''
    img = numpy.array(img)
    y, x = img.shape[:2]
    if direction == 'N': 
        temp = numpy.zeros((add, x, 4) if thirdaxis else (add, x), dtype=img.dtype)
        temp[:,:] = color
        return numpy.vstack((temp, img))
    elif direction == 'S': 
        temp = numpy.zeros((add, x, 4) if thirdaxis else (add, x), dtype=img.dtype)
        temp[:,:] = color
        return numpy.vstack((img, temp))
    elif direction == 'E': 
        temp = numpy.zeros((y, add, 4) if thirdaxis else (y, add), dtype=img.dtype)
        temp[:,:] = color
        return numpy.hstack((img, temp))
    elif direction == 'W': 
        temp = numpy.zeros((y, add, 4) if thirdaxis else (y, add), dtype=img.dtype)
        temp[:,:] = color
        return numpy.hstack((temp, img))
    else: return img

def getRegion(img:Image.Image|numpy.ndarray, cornerA:tuple|list, cornerB:tuple|list, exact = 2, color = (0,0,0,0), thirdaxis = True):
    '''Returns a region of an image, given two coordinates relative to (0,0) of the image'''
    imgC = img
    if thirdaxis: y, x, _ = img.shape
    else: y, x = img.shape
    pointA = [round(min(cornerA[0], cornerB[0])), round(min(cornerA[1], cornerB[1]))]
    pointB = [round(max(cornerA[0], cornerB[0])), round(max(cornerA[1], cornerB[1]))]
    if exact > 0:
        if pointA[0] < 0:
            add = abs(pointA[0])
            imgC = addBlank(imgC, add, "W", color, thirdaxis)
            pointA[0] += add 
            pointB[0] += add
        if pointA[1] < 0:
            add = abs(pointA[1])
            imgC = addBlank(imgC, add, "N", color, thirdaxis)
            pointA[1] += add 
            pointB[1] += add
        if exact > 1:
            if x < pointB[0]:
                add = abs(pointB[0]-x)
                imgC = addBlank(imgC, add, "E", color, thirdaxis)
                pointB[0] += add
            if y < pointB[1]:
                add = abs(pointB[1]-y)
                imgC = addBlank(imgC, add, "S", color, thirdaxis)
                pointB[1] += add
    area = imgC[round(pointA[1]):round(pointB[1]+1), round(pointA[0]):round(pointB[0]+1)]
    return area

def merge(img1:Image.Image|numpy.ndarray, img2:Image.Image|numpy.ndarray):
    '''Returns an array of the average of the values of two given images/numpy arrays as a numpy array'''
    img1 = numpy.array(img1)
    img2 = numpy.array(img2)
    return img1 // 2 + img2 // 2

def placeOver(img1:numpy.ndarray, img2:numpy.ndarray, position:list|tuple, center = False):
    '''Modifies image 1 (background) as an array of image 2 (overlay) placed on top of image 1 (background), given as numpy arrays'''
    if center: position = (round(position[0]-img2.shape[1]*0.5),round(position[1]-img2.shape[0]*0.5))
    img1H, img1W = img1.shape[:2] 
    img2H, img2W = img2.shape[:2]

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
    alpha_background = img1[startY:endY, startX:endX, 3] / 255.0

    if numpy.any(img2[:, :, 3] < 0):
        alpha_background = img1[startY:endY, startX:endX, 3].astype(numpy.float64)
        alpha_background += img2[:, :, 3].astype(numpy.float64)
        alpha_background[alpha_background < 0] = 0
        alpha_background[alpha_background > 255] = 255
        img1[startY:endY, startX:endX, 3] = alpha_background.astype(numpy.uint8)
    else:
        combined_alpha = alpha_overlay + alpha_background * (1 - alpha_overlay)
        blendedRGB = (overlayRGB*alpha_overlay[:, :, None]+backgroundRGB*(1-alpha_overlay[:, :, None])).astype(numpy.uint8)    
        img1[startY:endY, startX:endX, :3] = blendedRGB
        img1[startY:endY, startX:endX, 3] = (combined_alpha * 255).astype(numpy.uint8)
    
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

def rotateDegHundred(img: numpy.ndarray, cent:float):
    '''Returns an array of a rotated version of the given image by (cent) cents, using the 0 up CCW rotation system. 100 cents = 360 degrees, 1 cent = 3.6 degrees'''
    return numpy.array(Image.fromarray(img).rotate(cent*3.6,expand=True))

def setSize(img: numpy.ndarray, size):
    '''Returns a copy of the given image scaled by size, given the size change (given with 50 as normal, >50 scale up, <50 scale down)'''
    y, x = img.shape[:2]
    return numpy.array(Image.fromarray(img).resize((max(1, (round(x*(size/50)**2))),max(1, round(y*(size/50)**2)))))

def setSizeSize(img: numpy.ndarray, size):
    '''Returns a copy of the given image with set size size, given the exact target sizes'''
    return numpy.array(Image.fromarray(img).resize((max(1,size[0]), max(1,size[1])), Image.Resampling.NEAREST))

def setSizeSizeBlur(img: numpy.ndarray, size):
    '''Returns a copy of the given image with set size size, given the exact target sizes, resampling is hamming!'''
    return numpy.array(Image.fromarray(img).resize((size[0], size[1]), Image.Resampling.HAMMING))

def setColorEffect(img: numpy.ndarray, colorEffect):
    '''Returns a copy of the given image with a color shift, given the shift value (given 0-100)'''
    imgc = img.copy()
    imgc[:, :, 0:2] += numpy.uint8(colorEffect/100*255)
    return imgc

def setTransparency(img: numpy.ndarray, transparency):
    '''Returns a copy of the given image with transparency multiplied, given the transparency value (given 0-100, 0 = clear, 100 = normal)'''
    if transparency == 100: return img
    imgc = img.copy()
    imgMask = imgc[:, :, 3] * (transparency/100)
    imgc[:, :, 3] = imgMask
    return imgc

def setBrightness(img: numpy.ndarray, brightness):
    '''Returns a copy of the given image with brightness changed, given the brightness value (>50 = brighter, <50 = darker)'''
    imgc = ImageEnhance.Brightness(Image.fromarray(img))
    imgc = imgc.enhance((brightness+50)/100)
    return numpy.array(imgc)

def setBlur(img: numpy.ndarray, pixelation):
    '''Returns a copy of the given image blured, given the blur value (given 0-100, 0 = normal, 100 = very pixelated)'''
    if pixelation <= 1: return img
    y, x = img.shape[:2]
    imgc = numpy.array(Image.fromarray(img).resize((max(1, (round(x/pixelation*(x/100)))),max(1, round(y/pixelation*(y/100))))))
    return numpy.array(Image.fromarray(imgc).resize((round(x),round(y))))

def setLimitedSize(img: numpy.ndarray, size):
    '''Returns the a copy of the image scaled to fix inside a (size x size) shape'''
    y, x, = img.shape[:2]
    scaleFactor = size/x if x>y else size/y
    return numpy.array(Image.fromarray(img).resize((max(1, (round(x*scaleFactor))),max(1, round(y*scaleFactor)))))

def setLimitedSizeSize(img: numpy.ndarray, size:tuple|list):
    '''Returns the a copy of the image scaled to fix inside a size shape'''
    y, x = img.shape[:2]
    scaleFactor = size[0]/x
    if size[1]/y < scaleFactor: scaleFactor = size[1]/y
    return numpy.array(Image.fromarray(img).resize((max(1, (round(x*scaleFactor))),max(1, round(y*scaleFactor))), Image.Resampling.NEAREST))

def resizeImage(img: numpy.ndarray, size:tuple|list):
    '''Returns the a copy of the image scaled to shape size'''
    return numpy.array(Image.fromarray(img).resize(size, Image.Resampling.NEAREST))