'''The class all about the sprites, which are the manipulatable images that move across the screen.'''

from settings import *
import numpy, math, uuid
from subsystems.pathing import smoothChangeAt, straightChangeAt, roundf, timelyBezierPathCoords, selectiveBezierPathCoords, straightPathCoords, mergeCoordRotationPath, betweenP
from subsystems.render import rotateDegHundred, setSize, setColorEffect, setTransparency, setBrightness, setBlur
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
    def __init__(self,name, imgUUID = "placeholder5"):
        self.uuid = str(uuid.uuid4())
        self.name = name
        self.imageUUIDs = [
            imgUUID
        ]
        self.data = {
            "name":name, 
            "uuid":self.uuid,
            "images":self.imageUUIDs, 
            "c":[0,(0,0),"L",1,(0,0),"L"],  # Coordinate
            "r":[0,    0,"L",1,    0,"L"],  # Rotation - 0 up CCW
            "a":[0,    0,"L",1,    0,"L"],  # Apperance - 0 = image0
            "s":[0,   50,"L",1,   50,"L"],  # Size - 50 = normal
            "h":[0,    0,"L",1,    0,"L"],  # Hue - 0 = normal
            "t":[0,  100,"L",1,  100,"L"],  # Transparency - 100 = normal
            "b":[0,   50,"L",1,   50,"L"],  # Brightness - 50 = normal
            "w":[0,    0,"L",1,    0,"L"]   # Blur - 0 = normal
        }
    def setData(self, key, data):
        '''Sets a properity's set of data, given the key and data'''
        dataCheck(key, data)
        self.data[key] = data
    def getData(self, key):
        '''Gets a properity's set of data, given the key'''
        return self.data[key]
    def generateSequence(self, key):
        '''Generates a state sequence for a given property, given the key'''
        if key == "c": return iterateThroughPath(self.data["c"])
        if key == "p": return mergeCoordRotationPath(iterateThroughPath(self.data["c"]), iterateThroughSingle(self.data["r"]))
        if key == "a": return [max(0, min(len(self.imageUUIDs)-1, round(item))) for item in iterateThroughSingle(self.data["a"])]
        if key in "rshtbw" and len(key) == 1: return iterateThroughSingle(self.data[key])
    def getStateAt(self, key, time):
        '''Returns a state of a given property for a given time, given the key and time'''
        if key == "c": return findStateThroughPath(self.data["c"], time)
        if key == "p":
            cx, cy = findStateThroughPath(self.data["c"], time) 
            return (cx, cy, findStateThroughSingle(self.data["r"], time))
        if key == "a": return max(0, min(len(self.imageUUIDs)-1, round(findStateThroughSingle(self.data["a"],time))))
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
    def addImageUUID(self, imgUUID):
        '''Adds an image UUID to the sprite's appearances'''
        self.imageUUIDs.append(imgUUID)
        self.data["images"] = self.imageUUIDs
    def removeImageUUID(self, img):
        '''Removes an image from the sprite's apperances, given the imageUUID or index'''
        if type(img) == str: 
            self.imageUUIDs.pop(self.imageUUIDs.index(numpy.array(img)))
        else: 
            if len(self.imageUUIDs) > 1: self.imageUUIDs.pop(max(0, min(img, len(self.imageUUIDs)-1)))
        self.data["images"] = self.imageUUIDs
    def getImageUUIDAt(self, time):
        '''Returns the array of an image of the sprite at a given time'''
        try: return self.imageUUIDs[self.getStateAt("a", time)]
        except: return self.imageUUIDs[0]
    def getName(self):
        '''Gets the name of the sprite'''
        return self.name
    def setName(self, name):
        '''Sets the name of the sprite'''
        self.name = name
        self.data["name"] = name
    def fullDataImport(self, data):
        '''Imports all the sprite data'''
        self.data = data
        self.name = self.data["name"]
        self.uuid = self.data["uuid"]
        self.imageUUIDs = self.data["images"]

def dataCheck(key, data):
    '''Modifies the original given data with all checked values (rounding and connections)'''
    dataLen = round(len(data)/3)
    for i in range(dataLen):
        data[i*3] = roundf(data[i*3], PATH_FLOAT_ACCURACY)
        if key in "rashtbw " and len(key) == 1:
            data[i*3+1] = roundf(data[i*3+1], PATH_FLOAT_ACCURACY)
        if key == "c":
            data[i*3+1] = (roundf(data[i*3+1][0], PATH_FLOAT_ACCURACY), roundf(data[i*3+1][1], PATH_FLOAT_ACCURACY))
        if data[i*3+2] == None and i != dataLen-1:
            data[i*3+2] = "L"
    if dataLen == 0:
        for thing in ["L", (0,0) if key == "c" else 0, 2]: data.insert(0, thing)
    if dataLen == 1:
        for thing in ["L", (0,0) if key == "c" else 0, 1]: data.insert(0, thing)

# Compact Storage Reading

def iterateThroughSingle(compact, partition = False):
    '''Returns a path of single sequences with straight or smooth connections given the compact path'''
    sequence = []
    timeStamps = [compact[i*3] for i in range(math.floor(len(compact)/3))]
    for i in range(len(timeStamps)-1):
        add = []
        if compact[i*3+2] == "L": add = straightChangeAt(compact[i*3+1], compact[(i+1)*3+1], (compact[(i+1)*3]-compact[i*3])*RENDER_FPS)
        if compact[i*3+2] == "S": add = smoothChangeAt(compact[i*3+1], compact[(i+1)*3+1], (compact[(i+1)*3]-compact[i*3])*RENDER_FPS)
        if partition:
            sequence.append([(compact[i*3] + roundf(ie/RENDER_FPS, PATH_FLOAT_ACCURACY), add[ie]) for ie in range(len(add))])
        else:
            for state in add: sequence.append(roundf(state, PATH_FLOAT_ACCURACY))
    return sequence

def findStateThroughSingle(compact, time):
    '''Returns the state of a property on single sequence given the compact path and time'''
    timeStamps = [compact[i*3] for i in range(math.floor(len(compact)/3))]
    if time <= timeStamps[0]: return compact[1]
    if time >= timeStamps[-1]: return compact[-2]
    low = 0
    for i in range(len(timeStamps)-1):
        if timeStamps[i]<=time: low = i
        else: break
    index = round((time-compact[low*3])*RENDER_FPS)
    if compact[low*3+2] == "L": return protectedBoundary(straightChangeAt(compact[low*3+1], compact[(low+1)*3+1], (compact[(low+1)*3]-compact[low*3])*RENDER_FPS), index)
    elif compact[low*3+2] == "S": return protectedBoundary(smoothChangeAt(compact[low*3+1], compact[(low+1)*3+1], (compact[(low+1)*3]-compact[low*3])*RENDER_FPS), index)
    else: return compact[low*3+1]

def iterateThroughPath(compact, partion = False):
    '''Returns a path of coordinates, given the compact storage of the path'''
    path = []
    timeStamps = [compact[i*3] for i in range(math.floor(len(compact)/3))]
    connections = [compact[i*3+2] for i in range(math.floor(len(compact)/3))]
    i = 0
    while i < len(timeStamps)-1:
        if connections[i] == "L": 
            add = straightPathCoords([compact[i*3+1], compact[(i+1)*3+1]], round((compact[(i+1)*3]-compact[i*3])*RENDER_FPS))
            if partion: path.append([(compact[i*3] + roundf(ie/RENDER_FPS, PATH_FLOAT_ACCURACY), add[ie]) for ie in range(len(add))])
        if connections[i] == "S":
            temp = [i]
            while connections[i+1] == "S" and i+1<len(connections)-1:
                temp.append(i+1)
                i+=1
                if i+1 > len(connections)-1: break
            temp.append(i+1)
            add = timelyBezierPathCoords([protectedBoundary(compact,iee*3+1) for iee in temp], [round((timeStamps[temp[ie]]-timeStamps[temp[ie-1]])*RENDER_FPS) for ie in range(1,len(temp))], partion)
            if partion:
                for iee in range(len(add)):
                    path.append([(compact[(temp[0]+iee)*3] + roundf(ie/RENDER_FPS, PATH_FLOAT_ACCURACY), add[iee][ie]) for ie in range(len(add[iee]))])
        if not(partion):
            for coord in add: path.append(coord)
        i+=1
    return path

def findStateThroughPath(compact, time):
    '''Returns a path of coordinates at a given time, given the compact storage of the path'''
    timeStamps = [compact[i*3] for i in range(math.floor(len(compact)/3))]
    connections = [compact[i*3+2] for i in range(math.floor(len(compact)/3))]
    low = 0
    for i in range(len(timeStamps)-1):
        if timeStamps[i]<=time: low = i
        else: break
    if connections[low] == "L":
        timeC = round((time-compact[low*3])/(compact[(low+1)*3]-compact[low*3]+0.000001))
        timeC = max(0, min(timeC, 1))
        cx, cy = betweenP(compact[low*3+1], compact[(low+1)*3+1])(timeC)
        return (roundf(cx, PATH_FLOAT_ACCURACY), roundf(cy, PATH_FLOAT_ACCURACY))
    if connections[low] == "S":
        bottom, top = low, low
        while connections[bottom-1] == "S":
            bottom += -1
            if bottom < 0: 
                bottom = 0
                break
        while connections[top+1] == "S":
            top += 1
            if top+1 > len(connections)-1: 
                break
        segment = selectiveBezierPathCoords([compact[point*3+1] for point in range(bottom, top+2)], math.ceil((compact[(low+1)*3]-compact[low*3])*RENDER_FPS), low-bottom)
        return protectedBoundary(segment, round((time-compact[low*3])*RENDER_FPS), (0,0))

def findExtentThroughPath(compact, low):
    '''Returns a list of indexes of points that are how far the connections go, given the compact storage of the path'''
    connections = [compact[i*3+2] for i in range(math.floor(len(compact)/3))]
    if connections[low] == "L": return [low, low + 1] if low<len(connections)-1 else [low]
    if connections[low] == "S":
        bottom, top = low, low
        while connections[bottom-1] == "S": 
            bottom += -1
            if bottom < 0:
                bottom = 0
                break
        if not(top+1 > len(connections)-1):
            while connections[top+1] == "S":
                top += 1
                if top+1 > len(connections)-1: break
        return list(range(bottom, top+2))

def protectedBoundary(sequence, i, empty = 0):
    '''Returns the index closest to i of a list, given a list and index. (if i is too high, gives the highest index, if it is too low, gives the least index)'''
    if len(sequence) == 0: return empty
    return sequence[max(0, min(round(i), len(sequence)-1))]

def readImgSingleFullState(state, images, singleImage = False):
    '''Returns an array of the image of the sprite at a given full state in [(x,y,dir), a, s, h, t, b, w] form, given the full state and the set of images'''
    if singleImage:
        img = images
    else:
        try: img = images[state[1]].copy()
        except: img = images[0].copy()
    img = setSize(img, state[2])
    img = setColorEffect(img, state[3])
    img = setTransparency(img, state[4])
    img = setBrightness(img, state[5])
    img = setBlur(img, state[6])
    img = rotateDegHundred(img, state[0][2])
    return img

def listEVGPoints(interactableVisualObjects):
    '''Returns a list of all EVG Point Visual Object IDs in the given `interactableVisualObjects` list'''
    ids = []
    allIDs= list(interactableVisualObjects.keys())
    for id in allIDs:
        if interactableVisualObjects[id][0]=="evg" and interactableVisualObjects[id][1].type=="point": ids.append(id)
    return ids

def listEVGConnections(interactableVisualObjects):
    '''Returns a list of all EVG Point Connection Visual Object IDs in the given `interactableVisualObjects` list'''
    ids = []
    allIDs= list(interactableVisualObjects.keys())
    for id in allIDs:
        if interactableVisualObjects[id][0]=="evg" and interactableVisualObjects[id][1].type=="connection": ids.append(id)
    return ids