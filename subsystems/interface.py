from settings import INTERFACE_FPS, PLACEHOLDER_IMAGE, PLACEHOLDER_IMAGE2
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
        img = placeOver(PLACEHOLDER_IMAGE, PLACEHOLDER_IMAGE2, (self.x+206,self.y+206))
        img = placeOver(img, PLACEHOLDER_IMAGE2, (self.x+206,-self.y+206))
        img = placeOver(img, PLACEHOLDER_IMAGE2, (-self.x+206,self.y+206))
        img = placeOver(img, PLACEHOLDER_IMAGE2, (-self.x+206,-self.y+206))
        img = placeOver(img, PLACEHOLDER_IMAGE2, (self.y+206,self.x+206))
        img = placeOver(img, PLACEHOLDER_IMAGE2, (self.y+206,-self.x+206))
        img = placeOver(img, PLACEHOLDER_IMAGE2, (-self.y+206,self.x+206))
        img = placeOver(img, PLACEHOLDER_IMAGE2, (-self.y+206,-self.x+206))
        return arrayToImage(img)
    def saveState(self):
        pass
    def close(self):
        pass