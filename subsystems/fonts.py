'''This file contains functions related to text rendering'''

from PIL import Image, ImageDraw, ImageFont
import numpy, os
from settings import *

def displayText(text: str, size, colorBG = (0,0,0,0), colorTXT = (255,255,255,255)):
    if size == "s":
        font = FONT_SMALL
    elif size == "m":
        font = FONT_MEDIUM
    else: 
        font = FONT_LARGE
    fsize = font.font.getsize(text)
    txtW = fsize[0][0]-fsize[1][0]
    txtH = fsize[0][1]-fsize[1][1]
    img = Image.new('RGBA', (txtW, round(txtH*2)), colorBG)
    ImageDraw.Draw(img).text((0, 0), text, font=font, fill=colorTXT)
    return numpy.array(img)


