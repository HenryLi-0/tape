'''The class all about the sprites, which are the manipulatable images that move across the screen.'''

from settings import *
import numpy, math
from subsystems.pathing import smoothChangeAt, straightChangeAt, roundf
from settings import PATH_FLOAT_ACCURACY, RENDER_FPS

class SingleSprite:
    '''
    Sprite Data Storage (all are type list):
    c (coord)   - coords compact path         (x,y)
    r (rots)    - rotations compact path      (dir)
    p (path)    - full path compact path      (x,y,dir)
    s (->)      - size path
    h (hue)     - color effect
    t (->)      - transparency
    b (->)      - brightness
    w (weird)   - pixelation

    Full State Data:
    [(x,y,dir), s, h, t, b, w]

    compact storage example:
    [
        1, [state], connection to next,
        3, [state], connection to next,
        10, [state], None
    ]

    Connection Type:
    L - linear, straight line
    S - smooth, curved approach, also represents beizer for coordinates
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
        if key == "p":
            pass # requires c and r to be complete
        if key in "rshtbw" and len(key) == 1:
            iterateThoughSingle(self.data[key])
    def getStateAt(self, key, time):
        if key == "c":
            pass # CODE
        if key == "p":
            pass # CODE
        if key in "rshtbw" and len(key) == 1: #
            findStateThroughSingle(self.data[key], time)

def iterateThoughSingle(compact):
    '''Returns a path of single sequences with straight or smooth connections given the compact path'''
    sequence = []
    timeStamps = [compact[i*3] for i in range(math.floor(len(compact)/3))]
    for i in range(len(timeStamps)-1):
        add = []
        if compact[i*3+2] == "L": add = straightChangeAt(compact[i*3+1], compact[(i+1)*3+1], (compact[(i+1)*3]-compact[i*3])*RENDER_FPS)
        if compact[i*3+2] == "S": add = smoothChangeAt(compact[i*3+1], compact[(i+1)*3+1], (compact[(i+1)*3]-compact[i*3])*RENDER_FPS)
        for state in add: sequence.append(roundf(state, PATH_FLOAT_ACCURACY))
    return sequence

def findStateThroughSingle(compact, time):
    '''Returns the state of a property on single sequence given the compact path and time'''
    timeStamps = [compact[i*3] for i in range(math.floor(len(compact)/3))]
    if time <= timeStamps[0]: return compact[1]
    if time >= timeStamps[-1]: return compact[-2]
    for i in range(len(timeStamps)-1):
        if timeStamps[i]<=time: low = i
        else: break
    index = round((time-compact[low*3])*RENDER_FPS)
    if compact[low*3+2] == "L": return straightChangeAt(compact[low*3+1], compact[(low+1)*3+1], (compact[(low+1)*3]-compact[low*3])*RENDER_FPS)[index]
    elif compact[low*3+2] == "S": return smoothChangeAt(compact[low*3+1], compact[(low+1)*3+1], (compact[(low+1)*3]-compact[low*3])*RENDER_FPS)[index]
    else: return compact[low*3+1]

