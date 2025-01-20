'''This file contains functions for rendering related purposes'''

from PIL import Image, ImageEnhance
import numpy, math

# Convert

def imageToArray(img:Image) -> numpy.ndarray:
    '''Converts an Image into a numpy array'''
    return numpy.array(img)

def arrayToImage(array:numpy.ndarray) -> Image:
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

def arrayPlaceOver(img1:numpy.ndarray, img2:numpy.ndarray, position:list|tuple, center = False):
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

def dArrayPlaceOver(img1:numpy.ndarray, img2: numpy.ndarray, position:list|tuple):
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

def placeOver(img1: Image, img2: Image, position:list|tuple, center = False):
    '''Modifies image 1 (background) as an array of image 2 (overlay) placed on top of image 1 (background), given as PIL images'''
    if center: X, Y = (position[0] - round(img2.width/2), position[1] - round(img2.height/2))
    else: X, Y = position
    if (X < img1.width) and (Y < img1.height) and (X + img2.width > 0) and (Y + img2.height > 0):
        if (X < 0) or (Y < 0) or (X + img2.width > img1.width) or (Y + img2.height > img1.height):
            SX = math.floor(max(X, 0))
            SY = math.floor(max(Y, 0))
            crop = img2.crop((
                max(-X, 0),
                max(-Y, 0),
                max(-X, 0) + (math.floor(min(X + img2.width, img1.width)) - SX),
                max(-Y, 0) + (math.floor(min(Y + img2.height, img1.height)) - SY)
            ))
            img1.paste(crop, (round(SX), round(SY)), crop)
        else:
            img1.paste(img2, (round(X), round(Y)), img2)
    return True

def rotateDeg(img: Image, degrees:float):
    '''Returns a copy of the Image as a rotated version of the given Image by (degrees) degrees, using the 0 up CCW rotation system'''
    return img.rotate(degrees,expand=True)

def rotateDegHundred(img: Image, cent:float):
    '''Returns a copy of the given Image as a rotated version of the given Image by (cent) cents, using the 0 up CCW rotation system. 100 cents = 360 degrees, 1 cent = 3.6 degrees'''
    return img.rotate(cent*3.6,expand=True)

def setSize(img: Image, size:float):
    '''Returns a copy of the given Image scaled by size, given the size change (given with 100 as normal, >100 scale up, <100 scale down)'''
    x, y = img.width, img.height
    return img.resize((max(1, (round(x*(size/100)))),max(1, round(y*(size/100)))),Image.Resampling.NEAREST)

def setSizeSize(img: Image, size:list|tuple):
    '''Returns a copy of the given Image with set size size, given the exact target sizes'''
    return img.resize((max(1,size[0]), max(1,size[1])), Image.Resampling.NEAREST)

def setSizeSizeBlur(img: Image, size:float):
    '''Returns a copy of the given Image with set size size, given the exact target sizes, resampling is hamming!'''
    return img.resize((size[0], size[1]), Image.Resampling.HAMMING)

def setColorEffect(img: Image, colorEffect:float):
    '''Returns a copy of the given Image with a color shift, given the shift value (given 0-100)'''
    imgc = imageToArray(img)
    imgc[:, :, 0:2] += numpy.uint8(colorEffect/100*255)
    return arrayToImage(imgc)

def setTransparency(img: Image, transparency:float):
    '''Returns a copy of the given Image with transparency multiplied, given the transparency value (given 0-100, 0 = clear, 100 = normal)'''
    if transparency == 100: return img
    imgc = imageToArray(img)
    imgMask = imgc[:, :, 3] * (transparency/100)
    imgc[:, :, 3] = imgMask
    return arrayToImage(imgc)

def setBrightnessEffect(img: Image, brightness:float):
    '''Returns a copy of the given Image with brightness changed, given the brightness value (<0 = darker, 0 = normal, >0 = brighter)'''
    return ImageEnhance.Brightness(img).enhance((brightness+100)/100)

def setBlur(img: Image, pixelation:float):
    '''Returns a copy of the given Image blured, given the blur value (given 0-100, 0 = normal, 100 = very pixelated)'''
    if pixelation <= 1: return img
    x, y = img.width, img.height
    imgc = img.resize((max(1, (round(x/pixelation*(x/100)))),max(1, round(y/pixelation*(y/100)))))
    return imgc.resize((round(x),round(y)))

def setLimitedSize(img: Image, size:int):
    '''Returns a copy of the given Image scaled to fix inside a (size x size) shape'''
    x, y = img.width, img.height
    scaleFactor = size/x if x>y else size/y
    return img.resize((max(1, (round(x*scaleFactor))),max(1, round(y*scaleFactor))))

def setLimitedSizeSize(img: Image, size:tuple|list):
    '''Returns a copy of the given Image scaled to fix inside a size shape'''
    x, y = img.width, img.height
    scaleFactor = size[0]/x
    if size[1]/y < scaleFactor: scaleFactor = size[1]/y
    return img.resize((max(1, (round(x*scaleFactor))),max(1, round(y*scaleFactor))), Image.Resampling.NEAREST)

def resizeImage(img: Image, size:tuple|list):
    '''Returns a copy of the given Image scaled to shape size'''
    return img.resize(size, Image.Resampling.NEAREST)