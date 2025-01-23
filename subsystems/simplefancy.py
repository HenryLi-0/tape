'''This file contains functions related to fancy rendering, but does not import from setting'''

from PIL import Image
import numpy, random, colorsys
from subsystems.render import *

def getArrayImageRGBAFromPath(path):
    '''Given a path, opens the image, converts it to RGBA, and returns it as a numpy array.'''
    return numpy.array(Image.open(path).convert("RGBA"))

def getImageRGBAFromPath(path):
    '''Given a path, opens the image, converts it to RGBA, and returns the Image.'''
    return Image.open(path).convert("RGBA")

def generateColorBox(size:list|tuple = (25,25),color:list|tuple = (255,255,255,255)):
    '''Generates a box of (size) size of (color) color'''
    array = numpy.empty((size[1], size[0], 4), dtype=numpy.uint8)
    array[:, :] = color
    return arrayToImage(array)

def generateUnrestrictedColorBox(size:list|tuple = (25,25),color:list|tuple = (255,255,255,255)):
    '''Generates a box of (size) size of (color) color without restrictions'''
    array = numpy.empty((size[1], size[0], 4))
    array[:, :] = color
    return array

def generateBorderBox(size:list|tuple = (25,25), outlineW:int = 1, outerFill:list|tuple = (255,255,255,255), innerFill: list|tuple = (0,0,0,0)):
    '''Generates a bordered box with an inside with (innerFill) fill with space of (size), and an (outlineW) px thick outline of (outerFill) color surrounding it'''
    array = numpy.zeros((size[1]+2*outlineW, size[0]+2*outlineW, 4), dtype=numpy.uint8)
    array[:,:,:] = innerFill
    array[:outlineW, :, :] = outerFill
    array[-outlineW:, :, :] = outerFill
    array[:, :outlineW, :] = outerFill
    array[:, -outlineW:, :] = outerFill
    return arrayToImage(array)

def generateInwardsBorderBox(size:list|tuple = (25,25), outlineW:int = 1, color:list|tuple = (255,255,255,255), fill:list|tuple = (0,0,0,0)):
    '''Generates a inwards bordered box with a transparent inside, with transparent space of (size - outline), and an (outlineW) px thick outline of (color) color surrounding it'''
    array = numpy.zeros((size[1], size[0], 4), dtype=numpy.uint8)
    array[:,:,:] = fill
    array[:outlineW, :, :] = color
    array[-outlineW:, :, :] = color
    array[:, :outlineW, :] = color
    array[:, -outlineW:, :] = color
    return arrayToImage(array)

def generatePastelDark():
    '''Randomly generates a dark pastel color'''
    color = [100]
    color.insert(random.randrange(0,len(color)), random.randrange(100,200))
    color.insert(random.randrange(0,len(color)), random.randrange(100,200))
    color.append(255)
    return color

def translatePastel(color, value = 0.9):
    '''Translate a color based on the value of Value is HSV, given the color in RGBA form and the target Value'''
    colorC = color[0:3]
    colorC = list(colorsys.rgb_to_hsv(colorC[0]/255,colorC[1]/255,colorC[2]/255))
    colorC[2] = value
    colorC = colorsys.hsv_to_rgb(colorC[0],colorC[1],colorC[2])
    return [round(colorC[0]*255), round(colorC[1]*255), round(colorC[2]*255), color[3]]

def generateHoverIcon(img, active = False, color = ""):
    '''Generates an icon image given an image, inactive color, active color, and an optional overriding color, which replacing all non empty pixels with that color.'''
    from subsystems.render import imageToArray, arrayToImage
    icon = imageToArray(img)
    icon[(icon[...] != [0,0,0,0]).any(axis=-1)] = color if (color!= "") else ([250,250,250,255] if active else [175,175,175,255])
    icon = arrayToImage(icon)
    return icon

def fill(img, targetColor = (0,0,0,255), fillColor = (255,255,255,255)):
    '''Generates an icon image given an image, inactive color, active color, and an optional overriding color, which replacing all non empty pixels with that color.'''
    from subsystems.render import imageToArray, arrayToImage
    icon = imageToArray(img)
    icon[(icon[...] == targetColor).any(axis=-1)] = fillColor
    icon = arrayToImage(icon)
    return icon

def generateCircle(radius, color):
    '''Generates a circle with given radius (radius) and color (RGBA)'''
    diameter = radius * 2
    array = numpy.empty((diameter, diameter, 4), dtype=numpy.uint8)
    center = radius
    for y in range(diameter):
        for x in range(diameter):
            distance = numpy.sqrt((x-center)**2+(y-center)**2)
            if distance <= radius:
                array[y,x] = color
            else:
                array[y,x] = (0,0,0,0)
    return arrayToImage(array)

def generateThemedBorderRectangleInstructions(size:list|tuple = (25,25),borderColor:list|tuple = (255,255,255,255), background:Image = None, backgroundOffset:list|tuple = (0,0)):
    '''Generates Instructions for a Themed Border Rectangle'''
    instructions = []
    if background != None: instructions.append([background, backgroundOffset])
    row = generateColorBox((size[0],3), borderColor)
    col = generateColorBox((3,size[1]), borderColor)
    instructions.append([row, (0,0)])
    instructions.append([col, (0,0)])
    instructions.append([row, (0,size[1]-3)])
    instructions.append([col, (size[0]-3,0)])
    return instructions

def generateSpecificThemedBorderRectangleInstructions(section, borderColor:list|tuple = (255,255,255,255)):
    '''Generates Instructions for a specific section's Themed Border Rectangle'''
    return None
    