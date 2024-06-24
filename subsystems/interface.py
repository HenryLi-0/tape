'''This file is all about managing what the user sees'''

from settings import *
from PIL import ImageTk, Image
import time, numpy, random, os, subsystems.interface
from subsystems.pathing import bezierPathCoords, straightPathCoords
from subsystems.render import *
from subsystems.fonts import displayText

class Interface:
    def __init__(self):
        self.mx = 0
        self.my = 0
        self.fps = 0
        pass

    def tick(self,mx,my,fps):
        '''Entire Screen: `(0,0) to (1365,697)`: size `(1366,698)`'''
        self.mx = mx if (0<=mx and mx<=1365) and (0<=my and my<=697) else self.mx 
        self.my = my if (0<=mx and mx<=1365) and (0<=my and my<=697) else self.my
        self.fps = fps
        pass

    def getImageAnimation(self):
        '''Animation Interface: `(23,36) to (925,542)`: size `(903,507)`'''
        img = FRAME_ANIMATION_ARRAY.copy()
        placeOver(img, displayText(f"mouse is at ({self.mx}, {self.my})", "m"), (50,50))
        placeOver(img, displayText("".join([x for x in [("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-_=+")[random.randrange(0,75)] for x in range(50)]]), "m", colorTXT=(0,255,0,255)),(50,100))
        placeOver(img, displayText(f"FPS: {self.fps}", "m"), (50,150))
        placeOver(img, CURSOR_ARRAY, (self.mx-23-13,self.my-36-13))
        for i in range(100):
            placeOver(img, PLACEHOLDER_IMAGE_5_ARRAY, (random.randrange(0,902),random.randrange(0,506)))
        return arrayToImage(img)
    
    def getImageTimeline(self):
        '''Timeline Interface: `(23,558) to (925,680)`: size `(903,123)`'''
        return arrayToImage(FRAME_TIMELINE_ARRAY)
    
    def getImageEditor(self):
        '''Editor Interface: `(953,36) to (1340,542)`: size `(388,507)`'''
        return arrayToImage(FRAME_EDITOR_ARRAY)
    
    def getImageOptions(self):
        '''Options Interface: `(953,558) to (1340,680)`: size `(388,123)`'''
        return arrayToImage(FRAME_OPTIONS_ARRAY)
    
    def saveState(self):
        pass
    def close(self):
        pass