'''This file is all about what the user sees'''

from settings import *
from PIL import ImageTk, Image
import time, numpy, random, os, subsystems.interface
from subsystems.pathing import bezierPathCoords, straightPathCoords
from subsystems.render import *

class Interface:
    def __init__(self):
        self.x = 0
        self.y = 0
        pass
    def tick(self):
        self.x += 1 #random.randrange(-3,3)
        self.y += 2 #random.randrange(-3,3)
    def getImage(self):
        img = LOADING_IMAGE_ARRAY.copy()
        placeOver(img, PLACEHOLDER_IMAGE_2_ARRAY, (self.x+206,self.y+206))
        placeOver(img, PLACEHOLDER_IMAGE_2_ARRAY, (self.x+206,-self.y+206))
        placeOver(img, PLACEHOLDER_IMAGE_2_ARRAY, (-self.x+206,self.y+206))
        placeOver(img, PLACEHOLDER_IMAGE_2_ARRAY, (-self.x+206,-self.y+206))
        placeOver(img, PLACEHOLDER_IMAGE_2_ARRAY, (self.y+206,self.x+206))
        placeOver(img, PLACEHOLDER_IMAGE_2_ARRAY, (self.y+206,-self.x+206))
        placeOver(img, PLACEHOLDER_IMAGE_2_ARRAY, (-self.y+206,self.x+206))
        placeOver(img, PLACEHOLDER_IMAGE_2_ARRAY, (-self.y+206,-self.x+206))
        return arrayToImage(PLACEHOLDER_IMAGE_5_ARRAY)
    def saveState(self):
        pass
    def close(self):
        pass