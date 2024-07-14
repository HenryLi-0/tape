'''This file contains functions related to fancy rendering'''

from PIL import Image, ImageDraw
import numpy
from settings import *

def displayText(text: str, size, colorBG:tuple|list = (0,0,0,0), colorTXT:tuple|list = (255,255,255,255), bold = False):
    '''Returns a numpy array for text, give the text (str), size (s, m, or l for small, medium, large, respectively), and optional background and text color given as (r,g,b,a)'''
    if size == "s":
        font = FONT_SMALL
    elif size == "m":
        font = FONT_MEDIUM
    else: 
        font = FONT_LARGE
    fsize = font.font.getsize(text)
    txtW = fsize[0][0]-fsize[1][0]
    txtH = fsize[0][1] #-fsize[1][1]
    img = Image.new('RGBA', (txtW, round(txtH*1.5)), colorBG)
    ImageDraw.Draw(img).text((0, 0), text, font=font, fill=colorTXT, stroke_width=(1 if bold else 0))
    return numpy.array(img)


def generateColorBox(size:list|tuple = (25,25),color:list|tuple = (255,255,255,255)):
    '''Generates a box of (size) size of (color) color'''
    array = numpy.empty((size[1], size[0], 4), dtype=numpy.uint8)
    array[:, :, 0] = color[0]
    array[:, :, 1] = color[1]
    array[:, :, 2] = color[2]
    array[:, :, 3] = color[3]
    return array

def generateBorderBox(size:list|tuple = (25,25), outlineW:int = 1, color:list|tuple = (255,255,255,255)):
    '''Generates a bordered box with a transparent inside, with transparent space of (size), and an (outlineW) px thick outline of (color) color surrounding it'''
    array = numpy.zeros((size[1]+2*outlineW, size[0]+2*outlineW, 4), dtype=numpy.uint8)
    array[:outlineW, :, :] = color
    array[-outlineW:, :, :] = color
    array[:, :outlineW, :] = color
    array[:, -outlineW:, :] = color
    return array

def generateIcon(img, active = False, size = (29,29)):
    from subsystems.visuals import placeOver
    icon = generateColorBox((size[0]+6,size[1]+6),hexColorToRGBA(BACKGROUND_COLOR))
    placeOver(icon, generateBorderBox(size,3, hexColorToRGBA(SELECTED_COLOR if active else FRAME_COLOR)), (0,0))
    placeOver(icon, img, (round((size[0]+6)/2),round((size[1]+6)/2)), True)
    return icon