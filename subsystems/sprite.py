'''The class all about the sprites, which are the manipulatable images that move across the screen.'''

from settings import *
import numpy, math
from subsystems.pathing import smoothChangeAt, straightChangeAt, roundf, timelyBezierPathCoords, straightPathCoords, betweenP
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
        if key == "c": iterateThroughPath(self.data["c"])
        if key == "p":
            pass # requires c and r to be complete
        if key in "rshtbw" and len(key) == 1: iterateThoughSingle(self.data[key])
    def getStateAt(self, key, time):
        if key == "c": findStateThroughPath(self.data["c"], time)
        if key == "p":
            pass # CODE
        if key in "rshtbw" and len(key) == 1: findStateThroughSingle(self.data[key], time)

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

def iterateThroughPath(compact):
    '''Returns a path of coordinates, given the compact storage of the path'''
    path = []
    timeStamps = [compact[i*3] for i in range(math.floor(len(compact)/3))]
    connections = [compact[i*3+2] for i in range(math.floor(len(compact)/3))]
    i = 0
    while i < len(timeStamps)-1:
        if connections[i] == "L": add = straightPathCoords([compact[i*3+1], compact[(i+1)*3+1]], (compact[(i+1)*3]-compact[i*3])*RENDER_FPS)
        if connections[i] == "S":
            temp = [i]
            while connections[i+1] == "S":
                temp.append(i+1)
                i+=1
            temp.append(i+1)
            add = timelyBezierPathCoords([compact[ie*3+1] for ie in temp], [round((timeStamps[temp[ie]]-timeStamps[temp[ie-1]])*RENDER_FPS) for ie in range(1,len(temp))])
        for coord in add: path.append((roundf(len(path)/RENDER_FPS, PATH_FLOAT_ACCURACY), coord[0], coord[1]))
        i+=1
    return path

def findStateThroughPath(compact, time):
    '''Returns a path of coordinates at a given time, given the compact storage of the path'''
    timeStamps = [compact[i*3] for i in range(math.floor(len(compact)/3))]
    connections = [compact[i*3+2] for i in range(math.floor(len(compact)/3))]
    for i in range(len(timeStamps)-1):
        if timeStamps[i]<=time: low = i
        else: break
    if connections[low] == "L": return betweenP(compact[low*3+1], compact[(low+1)*3+1])(0)
    '''FINSIH THIS'''