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

def generateInwardsBorderBox(size:list|tuple = (25,25), outlineW:int = 1, color:list|tuple = (255,255,255,255), fill: list|tuple = (0,0,0,0)):
    '''Generates a inwards bordered box with a transparent or given color inside, with inside space of (size - outline), and an (outlineW) px thick outline of (color) color surrounding it'''
    array = numpy.zeros((size[1], size[0], 4), dtype=numpy.uint8)
    array[:, :] = fill
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
    if section == "timeline":
        instructions = []
        instructions.append([generateInwardsBorderBox(( 43, 43), 3, borderColor), (  0,  0)])
        instructions.append([generateInwardsBorderBox(( 43, 43), 3, borderColor), (  0, 40)])
        instructions.append([generateInwardsBorderBox(( 43, 43), 3, borderColor), (  0, 80)])
        instructions.append([generateInwardsBorderBox((855,123), 3, borderColor), ( 48,  0)])
        return instructions
    elif section == "editor":
        instructions = []
        instructions.append([generateInwardsBorderBox((189, 95), 3, borderColor), (  0,  0)])
        instructions.append([generateInwardsBorderBox((189, 48), 3, borderColor), (  0,104)])
        instructions.append([generateInwardsBorderBox((189, 48), 3, borderColor), (  0,162)])
        instructions.append([generateInwardsBorderBox((388,288), 3, borderColor), (  0,219)])
        instructions.append([generateInwardsBorderBox((189,210), 3, borderColor), (199,  0)])
        return instructions
    elif section == "options":
        instructions = []
        instructions.append([generateInwardsBorderBox((120, 58), 3, borderColor), (  7, 0)])
        instructions.append([generateInwardsBorderBox((120, 58), 3, borderColor), (134, 0)])
        instructions.append([generateInwardsBorderBox((120, 58), 3, borderColor), (261, 0)])
        instructions.append([generateInwardsBorderBox((309, 58), 3, borderColor), (  7,65)])
        instructions.append([generateInwardsBorderBox(( 58, 58), 3, borderColor), (323,65)])
        return instructions
    elif section == "graph":
        from subsystems.render import placeOver
        temp = generateColorBox((388,288), (0,0,0,0))
        placeOver(temp, generateColorBox((  3,236), borderColor), ( 29, 23))
        placeOver(temp, generateColorBox((336,  3), borderColor), ( 29,256))
        return temp
    else:
        return []