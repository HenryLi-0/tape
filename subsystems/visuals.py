import time, numpy, random, os, math
from subsystems.pathing import bezierPathCoords, straightPathCoords
from subsystems.render import placeOver
from subsystems.fonts import displayText

class VisualManager:
    def __init__(self, worker, pruneCount = 5, maxLength = 15):
        '''A class for caching recently processed inputs in order to save on loading time and CPU power'''
        self.cache = {}
        self.memoryManage = []
        self.worker = worker
        self.pruneCount = min(pruneCount,maxLength)
        self.maxLength = maxLength
    def process(self, key):
        '''Process and caches an input's output if the input was not recently processed'''
        if not(str(key) in self.cache):
            self.cache[str(key)] = self.worker.get(key)
            self.memoryManage.append(time.time())
    def getRender(self, key):
        '''Returns an input's output if the input was recently processed, otherwise processes the input and returns the output'''
        self.process(key)
        key = str(key)         
        self.memoryManage[list(self.cache.keys()).index(key)] = time.time()
        if len(self.memoryManage) > self.maxLength:
            prune = self.memoryManage.copy()
            prune.sort()
            prune = prune[0:self.pruneCount]
            for item in prune:
                i = self.memoryManage.index(item)
                self.cache.pop(list(self.cache.keys())[i])
                self.memoryManage.pop(i)
        return self.cache[key]
    

class CircularPositionalBox:
    '''Just remembers where the object is supposed to be on screen, given the mouse position and updates when the mouse is in a specific ciruclar range'''
    def __init__(self, r:int = 10, ix = 0, iy = 0):
        '''Circular detection box will be centered!'''
        self.r, self.ix, self.iy = r, ix, iy
    def process(self, interact, mx, my):
        '''Should be called whenever the position wants to question its position'''
        if interact: self.ix, self.iy = mx, my
    def getInteract(self, mx, my): 
        '''Returns whether or not the mouse is in range of interaction'''
        return math.sqrt((mx-self.ix)**2 + (my-self.iy)**2) <= self.r
    def getPosition(self): return (self.ix, self.iy)
    def getX(self): return self.ix
    def getY(self): return self.iy
    def setPosition(self, position: tuple|list): self.ix, self.iy = position
    def setX(self, nx): self.ix = nx
    def setY(self, ny): self.iy = ny

class RectangularPositionalBox:
    '''Just remembers where the object is supposed to be on screen, given the mouse position and updates when the mouse is in a specific bounding box'''
    def __init__(self, bbox:tuple|list = (10,10), ix = 0, iy = 0):
        '''Bounding box will be centered!'''
        self.bbox, self.ix, self.iy = bbox, ix, iy
    def process(self, interact, mx, my):
        '''Should be called whenever the position wants to question its position'''
        if interact: self.ix, self.iy = mx, my
    def getInteract(self, mx, my):
        return (abs(self.mx-self.ix) < self.bbox[0]/2) and (abs(self.my-self.iy) < self.bbox[1]/2)
    def getPosition(self): return (self.ix, self.iy)
    def getX(self): return self.ix
    def getY(self): return self.iy
    def setPosition(self, position: tuple|list): self.ix, self.iy = position
    def setX(self, nx): self.ix = nx
    def setY(self, ny): self.iy = ny


from settings import ORB_IDLE_ARRAY, ORB_SELECTED_ARRAY, CURSOR_SELECT_ARRAY

class PathWorker: 
    '''Format inputs as a set-like of [bezier?, [coords], steps]'''
    def get(pathData):
        return bezierPathCoords(pathData[0], pathData[1]) if pathData[0] else straightPathCoords(pathData[0], pathData[1])
    
class PathVisualObject:
    def __init__(self, name):
        self.name = name
    def tick(self, window, points):
        path = bezierPathCoords(points, 10)
        for coord in path:
            placeOver(window, CURSOR_SELECT_ARRAY, coord, True)

class TestVisualObject:
    def __init__(self, name):
        self.name = name
        self.positionO = CircularPositionalBox(50)
        self.positionO.setPosition((random.randrange(0,903), random.randrange(0,507)))
        self.positionO.setPosition((random.randrange(0,903), random.randrange(0,507)))
    def tick(self, window, temp):
        placeOver(window, ORB_SELECTED_ARRAY if temp else ORB_IDLE_ARRAY, self.positionO.getPosition(), True)
        placeOver(window, displayText(self.name, "m"), self.positionO.getPosition(), True)
    def updatePos(self, interact, mx, my):
        self.positionO.setPosition((mx, my))
    def getInteractable(self, mx, my):
        return self.positionO.getInteract(mx, my)
