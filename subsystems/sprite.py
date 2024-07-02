'''The class all about the sprites, which are the manipulatable images that move across the screen.'''

from settings import *
import numpy, math
from subsystems.pathing import smoothChangeAt, straightChangeAt, roundf, timelyBezierPathCoords, selectiveBezierPathCoords, straightPathCoords, mergeCoordRotationPath, betweenP
from subsystems.render import rotateDeg, setSize, setColorEffect, setTransparency, setBrightness, setBlur
from settings import PATH_FLOAT_ACCURACY, RENDER_FPS

class SingleSprite:
    '''
    Sprite Data Storage (all are type list):
    c (coord)   - coords compact path         (x,y)
    r (rots)    - rotations compact path      (dir)
    a (->)      - apperance (image)
    s (->)      - size path
    h (hue)     - color effect
    t (->)      - transparency
    b (->)      - brightness
    w (weird)   - blur

    not stored:
    p (path)    - full path compact path      (x,y,dir)

    Full State Data:
    [(x,y,dir), a, s, h, t, b, w]

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
    def __init__(self,name, img = PLACEHOLDER_IMAGE_5_ARRAY):
        self.name = name
        self.images = [
            numpy.array(img)
        ]
        self.data = {
            "name":name, 
            "images":self.images, 
            "c":[], 
            "r":[],
            "a":[], 
            "s":[], 
            "h":[],
            "t":[],
            "b":[],
            "w":[]
        }
    def setData(self, key, data):
        '''Sets a properity's set of data, given the key and data'''
        self.data[key] = data
    def getData(self, key):
        '''Gets a properity's set of data, given the key'''
        return self.data[key]
    def generateSequence(self, key):
        '''Generates a state sequence for a given property, given the key'''
        if key == "c": return iterateThroughPath(self.data["c"])
        if key == "p": return mergeCoordRotationPath(iterateThroughPath(self.data["c"]), iterateThoughSingle(self.data["r"]))
        if key == "a": return [max(0, min(len(self.images)-1, round(item))) for item in iterateThoughSingle(self.data["a"])]
        if key in "rshtbw" and len(key) == 1: return iterateThoughSingle(self.data[key])
    def getStateAt(self, key, time):
        '''Returns a state of a given property for a given time, given the key and time'''
        if key == "c": return findStateThroughPath(self.data["c"], time)
        if key == "p":
            cx, cy = findStateThroughPath(self.data["c"], time) 
            return (cx, cy, findStateThroughSingle(self.data["r"], time))
        if key == "a": return max(0, min(len(self.images)-1, round(findStateThroughSingle(self.data["a"],time))))
        if key in "rshtbw" and len(key) == 1: return findStateThroughSingle(self.data[key], time)
    def generateFullSequence(self):
        '''Generates a full state sequence for all properties for the entire duration of importance'''
        p = self.generateSequence("p")
        a = self.generateSequence("a")
        s = self.generateSequence("s")
        h = self.generateSequence("h")
        t = self.generateSequence("t")
        b = self.generateSequence("b")
        w = self.generateSequence("w")
        return [
            (
                protectedBoundary(p,i),
                protectedBoundary(a,i),
                protectedBoundary(s,i),
                protectedBoundary(h,i),
                protectedBoundary(t,i),
                protectedBoundary(b,i),
                protectedBoundary(w,i)
            ) for i in range(max(len(p), len(a), len(s), len(h), len(t), len(b), len(w))-1)
        ]
    def getFullStateAt(self, time):
        '''Returns a full state of all properties for a given time'''
        return [
            self.getStateAt("p", time),
            self.getStateAt("a", time),
            self.getStateAt("s", time),
            self.getStateAt("h", time),
            self.getStateAt("t", time),
            self.getStateAt("b", time),
            self.getStateAt("w", time)
        ]
    def addImage(self, img):
        '''Adds an image to the sprite's appearances'''
        self.images.append(numpy.array(img))
        self.data["images"] = self.images
    def removeImage(self, img):
        '''Removes an image from the sprite's apperances, given the image'''
        self.images.pop(self.images.index(numpy.array(img)))
        self.data["images"] = self.images
    def getImageAt(self, time):
        '''Returns the array of an image of the sprite at a given time'''
        try: return self.images[self.getStateAt("a", time)]
        except: return self.images[0]
    def getName(self):
        '''Gets the name of the sprite'''
        return self.name
    def setName(self, name):
        '''Sets the name of the sprite'''
        self.name = name


# Compact Storage Reading

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
        if connections[i] == "L": add = straightPathCoords([compact[i*3+1], compact[(i+1)*3+1]], round((compact[(i+1)*3]-compact[i*3])*RENDER_FPS))
        if connections[i] == "S":
            temp = [i]
            while connections[i+1] == "S":
                temp.append(i+1)
                i+=1
            temp.append(i+1)
            add = timelyBezierPathCoords([compact[ie*3+1] for ie in temp], [round((timeStamps[temp[ie]]-timeStamps[temp[ie-1]])*RENDER_FPS) for ie in range(1,len(temp))])
        for coord in add: path.append((coord[0], coord[1]))
        i+=1
    return path

def findStateThroughPath(compact, time):
    '''Returns a path of coordinates at a given time, given the compact storage of the path'''
    timeStamps = [compact[i*3] for i in range(math.floor(len(compact)/3))]
    connections = [compact[i*3+2] for i in range(math.floor(len(compact)/3))]
    for i in range(len(timeStamps)-1):
        if timeStamps[i]<=time: low = i
        else: break
    if connections[low] == "L":
        cx, cy = betweenP(compact[low*3+1], compact[(low+1)*3+1])(time-compact[(low)*3])
        return (roundf(cx, PATH_FLOAT_ACCURACY), roundf(cy, PATH_FLOAT_ACCURACY))
    if connections[low] == "S":
        bottom, top = low, low
        while connections[bottom-1] == "S":
            bottom += -1
        while connections[top+1] == "S":
            top += 1
        segment = selectiveBezierPathCoords([compact[point*3+1] for point in range(bottom, top+2)], (compact[(low+1)*3]-compact[low*3])*RENDER_FPS, low)
        return segment[round((time-compact[(low)*3])*RENDER_FPS)]

def protectedBoundary(sequence, i):
    if len(sequence) == 0: return 0
    return sequence[max(0, min(i, len(sequence)-1))]

def readImgSingleFullState(state, images):
    '''Returns an array of the image of the sprite at a given full state in [(x,y,dir), a, s, h, t, b, w] form, given the full state and the set of images'''
    try: img = images[state[1]].copy()
    except: img = images[0].copy()
    img = setSize(img, state[2])
    img = setColorEffect(img, state[3])
    img = setTransparency(img, state[4])
    img = setBrightness(img, state[5])
    img = setBlur(img, state[6])
    img = rotateDeg(img, state[0][2])
    return img
