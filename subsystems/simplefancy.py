'''This file contains functions related to fancy rendering, but does not import from setting'''

from PIL import Image, ImageDraw
import numpy, random, colorsys

def generateColorBox(size:list|tuple = (25,25),color:list|tuple = (255,255,255,255)):
    '''Generates a box of (size) size of (color) color'''
    array = numpy.empty((size[1], size[0], 4), dtype=numpy.uint8)
    array[:, :] = color
    return array

def generateUnrestrictedColorBox(size:list|tuple = (25,25),color:list|tuple = (255,255,255,255)):
    '''Generates a box of (size) size of (color) color without restrictions'''
    array = numpy.empty((size[1], size[0], 4))
    array[:, :] = color
    return array

def generateBorderBox(size:list|tuple = (25,25), outlineW:int = 1, color:list|tuple = (255,255,255,255)):
    '''Generates a bordered box with a transparent inside, with transparent space of (size), and an (outlineW) px thick outline of (color) color surrounding it'''
    array = numpy.zeros((size[1]+2*outlineW, size[0]+2*outlineW, 4), dtype=numpy.uint8)
    array[:outlineW, :, :] = color
    array[-outlineW:, :, :] = color
    array[:, :outlineW, :] = color
    array[:, -outlineW:, :] = color
    return array

def generateInwardsBorderBox(size:list|tuple = (25,25), outlineW:int = 1, color:list|tuple = (255,255,255,255)):
    '''Generates a inwards bordered box with a transparent inside, with transparent space of (size - outline), and an (outlineW) px thick outline of (color) color surrounding it'''
    array = numpy.zeros((size[1], size[0], 4), dtype=numpy.uint8)
    array[:outlineW, :, :] = color
    array[-outlineW:, :, :] = color
    array[:, :outlineW, :] = color
    array[:, -outlineW:, :] = color
    return array

def generatePastelDark():
    '''Randomly generates a dark pastel color'''
    color = [100]
    color.insert(random.randrange(0,len(color)), random.randrange(100,200))
    color.insert(random.randrange(0,len(color)), random.randrange(100,200))
    color.append(255)
    return color

def translatePastelLight(color):
    '''Translate a dark pastel color to a light pastel color, given the color in RGBA form'''
    colorC = color[0:3]
    colorC = list(colorsys.rgb_to_hsv(colorC[0]/255,colorC[1]/255,colorC[2]/255))
    colorC[2] = 0.9
    colorC = colorsys.hsv_to_rgb(colorC[0],colorC[1],colorC[2])
    return [round(colorC[0]*255), round(colorC[1]*255), round(colorC[2]*255), color[3]]

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
    return array

def generateThemedBorderRectangleInstructions(size:list|tuple = (25,25),borderColor:list|tuple = (255,255,255,255)):
    '''Generates Instructions for a Themed Border Rectangle'''
    instructions = []
    row = generateColorBox((size[0],3), borderColor)
    col = generateColorBox((3,size[1]), borderColor)
    instructions.append([row, (0,0)])
    instructions.append([col, (0,0)])
    instructions.append([row, (0,size[1]-3)])
    instructions.append([col, (size[0]-3,0)])
    return instructions

def genereateSpecificThemedBorderRectangleInstructions(section, borderColor:list|tuple = (255,255,255,255)):
    '''Generates Instructions for a specific section's Themed Border Rectangle'''
    if section == "editor":
        "???"
    elif section == "options":
        instructions = []
        longrow = generateColorBox((309,3), borderColor)
        shortrow = generateColorBox((120,3), borderColor)
        shorterrow = generateColorBox((58,3), borderColor)
        col = generateColorBox((3,58), borderColor)
        instructions.append([shortrow, (  7, 0)])
        instructions.append([col,      (  7, 0)])
        instructions.append([shortrow, (  7,55)])
        instructions.append([col,      (124, 0)])
        instructions.append([shortrow, (134, 0)])
        instructions.append([col,      (134, 0)])
        instructions.append([shortrow, (134,55)])
        instructions.append([col,      (251, 0)])
        instructions.append([shortrow, (261, 0)])
        instructions.append([col,      (261, 0)])
        instructions.append([shortrow, (261,55)])
        instructions.append([col,      (378, 0)])

        instructions.append([longrow, (  7, 65)])
        instructions.append([    col, (  7, 65)])
        instructions.append([longrow, (  7,120)])
        instructions.append([    col, (313, 65)])

        instructions.append([shorterrow, (323, 65)])
        instructions.append([col,        (323, 65)])
        instructions.append([shorterrow, (323,120)])
        instructions.append([col,        (378, 65)])
        return instructions
    else:
        "???"