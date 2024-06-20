'''This file is all about what the user sees'''

from settings import *
from PIL import ImageTk, Image
import time, numpy, random, os, subsystems.interface
from subsystems.pathing import bezierPathCoords, straightPathCoords
from subsystems.render import *

class Interface:
    def __init__(self):
        pass

    def tick(self):
        '''Entire Screen: `(0,0) to (1365,697)`: size `(1366,698)`'''
        pass

    def getImageAnimation(self):
        '''Animation Interface: `(23,36) to (925,542)`: size `(903,507)`'''
        return arrayToImage(FRAME_ANIMATION_ARRAY)
    
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