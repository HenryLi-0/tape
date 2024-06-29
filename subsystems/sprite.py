'''The class all about the sprites, which are the manipulatable images that move across the screen.'''

from settings import *
import numpy


class SingleSprite:
    '''
    Sprite Data Storage (all list format):
    c (coord)   - coords compact path         (x,y)
    r (rots)    - rotations compact path      (dir)
    p (path)    - full path compact path      (x,y,dir)
    s (->)      - size path
    h (hue)     - color effect
    t (->)      - transparency
    b (->)      - brightness
    w (weird)   - pixelation

    compact coords storage: (x,y), (straight, beizer), (x,y)...     (x and y are coords)
    compact rotations storage: (deg), (straight, smooth), (deg)...  (deg are degrees)
    compact effect storage: (t, y), (straight, curve), (t, y)...    (t and y is time and strength)
    '''
    def __init__(self,name, img = PLACEHOLDER_IMAGE_2_ARRAY):
        self.name = name
        self.img = numpy.array(img)
        self.data = {
            "name":name, 
            "img":self.img, 
            "c":[], 
            "r":[], 
            "p":[], 
            "s":[], 
            "h":[],
            "t":[],
            "b":[],
            "w":[]
        }
    def setData(self, key, data):
        self.data[key] = data
    def getData(self):
        return self.data
    def generateSequence(self, key):
        if key == "c":
            pass # CODE
        if key == "r":
            pass # requires smooth glide function
        if key == "p":
            pass # requires c and r to be complete
        if key in "shtbw":
            pass # requires smooth glide function

def iterateThoughSingle(compact):
    '''For single sequences with straight or smooth connections'''
    sequence = []
    for i in range(int((len(compact)-1)/2)):
        compact[i] 
        pass #finish later