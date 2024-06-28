import time, numpy, random, os, math
from subsystems.pathing import bezierPathCoords, straightPathCoords, addP
from subsystems.render import placeOver
from subsystems.fancy import displayText, generateColorBox, generateBorderBox
from settings import FRAME_COLOR, SELECTED_COLOR, BACKGROUND_COLOR, hexColorToRGBA

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
    def process(self, interact, rmx, rmy):
        '''Should be called whenever the position wants to question its position'''
        if interact: self.ix, self.iy = rmx, rmy
    def getInteract(self, rmx, rmy): 
        '''Returns whether or not the mouse is in range of interaction'''
        return math.sqrt((rmx-self.ix)**2 + (rmy-self.iy)**2) <= self.r
    def getPosition(self): return (self.ix, self.iy)
    def getX(self): return self.ix
    def getY(self): return self.iy
    def getR(self): return self.r
    def setPosition(self, position: tuple|list): self.ix, self.iy = position
    def setX(self, nx): self.ix = nx
    def setY(self, ny): self.iy = ny
    def setR(self, nr): self.r = nr

class RectangularPositionalBox:
    '''Just remembers where the object is supposed to be on screen, given the mouse position and updates when the mouse is in a specific bounding box'''
    def __init__(self, bbox:tuple|list = (10,10), ix = 0, iy = 0):
        '''Bounding box will NOT be centered!'''
        self.bbox, self.ix, self.iy = bbox, ix, iy
    def process(self, interact, rmx, rmy):
        '''Should be called whenever the position wants to question its position'''
        if interact: self.ix, self.iy = rmx, rmy
    def getInteract(self, rmx, rmy):
        return (self.ix < rmx) and (rmx < (self.ix+self.bbox[0])) and (self.iy < rmy) and (rmy < (self.iy+self.bbox[1]))
    def getPosition(self): return (self.ix, self.iy)
    def getX(self): return self.ix
    def getY(self): return self.iy
    def getBBOX(self): return self.bbox
    def setPosition(self, position: tuple|list): self.ix, self.iy = position
    def setX(self, nx): self.ix = nx
    def setY(self, ny): self.iy = ny
    def setBBOX(self, nbbox): self.bbox = nbbox


from settings import ORB_IDLE_ARRAY, ORB_SELECTED_ARRAY, CURSOR_SELECT_ARRAY

class PathWorker: 
    '''Format inputs as a set-like of [bezier?, [coords], steps]'''
    def get(pathData):
        return bezierPathCoords(pathData[0], pathData[1]) if pathData[0] else straightPathCoords(pathData[0], pathData[1])
    
class PathVisualObject:
    '''A path'''
    def __init__(self, id, name):
        self.id = id
        self.name = name
    def tick(self, window, points):
        '''Takes in a set of points and draws the path'''
        path = bezierPathCoords(points, 10)
        for coord in path:
            placeOver(window, CURSOR_SELECT_ARRAY, coord, True)

class OrbVisualObject:
    '''A movable point.'''
    def __init__(self, id, name):
        self.type = "orb"
        self.id = id
        self.name = name
        self.positionO = CircularPositionalBox(50)
        self.positionO.setPosition((random.randrange(0,903), random.randrange(0,507)))
    def tick(self, window, active):
        placeOver(window, ORB_SELECTED_ARRAY if active else ORB_IDLE_ARRAY, self.positionO.getPosition(), True)
        placeOver(window, displayText(self.name, "m"), self.positionO.getPosition(), True)
    def updatePos(self, rmx, rmy):
        self.positionO.setPosition((rmx, rmy))
    def getInteractable(self, rmx, rmy):
        return self.positionO.getInteract(rmx, rmy)

class ButtonVisualObject:
    '''A button.'''
    def __init__(self, id, name, pos:tuple|list, img:numpy.ndarray, img2:numpy.ndarray):
        self.type = "button"
        self.id = id
        self.name = name
        self.img = img
        self.img2 = img2
        self.positionO = RectangularPositionalBox((img.shape[1],img.shape[0]), pos[0], pos[1])
    def tick(self, window, active):
        placeOver(window, self.img2 if active else self.img, self.positionO.getPosition(), False)
    def updatePos(self, rmx, rmy):
        pass
    def getInteractable(self,rmx,rmy):
        return self.positionO.getInteract(rmx, rmy)
    
class EditableTextBoxVisualObject:
    '''An editable text box.'''
    def __init__(self, id, name, pos:tuple|list, startTxt= ""):
        self.type = "textbox"
        self.id = id
        self.name = name
        self.txt = startTxt
        self.txtImg = displayText(self.txt, "m")
        self.positionO = RectangularPositionalBox((max(self.txtImg.shape[1]+3,10),max(self.txtImg.shape[0],23)), pos[0]-3, pos[1]-3)
    def tick(self, window, active):
        placeOver(window, generateColorBox(addP(self.positionO.getBBOX(), (5,3)), hexColorToRGBA(BACKGROUND_COLOR)), self.positionO.getPosition())
        placeOver(window, generateBorderBox(self.positionO.getBBOX(), 3, hexColorToRGBA(SELECTED_COLOR) if active else hexColorToRGBA(FRAME_COLOR)), self.positionO.getPosition())
        placeOver(window, self.txtImg, addP(self.positionO.getPosition(),(5,3)), False)
    def updateText(self, txt):
        if self.txt!=txt:
            self.txt = txt
            self.txtImg = displayText(self.txt, "m")
            self.positionO.setBBOX((max(self.txtImg.shape[1]+3,10),max(self.txtImg.shape[0],23)))
    def updatePos(self, rmx, rmy):
        pass
    def getInteractable(self,rmx,rmy):
        return self.positionO.getInteract(rmx, rmy)
    
class DummyVisualObject:
    '''I sit around doing nothing. Like that one group member in randomly assigned class projects. That person didn't deserve that 100, did they now? (joke)'''
    def __init__(self, id, name, pos:tuple|list):
        self.type = "dummy"
        self.id = id
        self.name = name
        self.positionO = RectangularPositionalBox((0,0), pos[0], pos[1])
    def tick(self, window, active):
        pass
    def updatePos(self, rmx, rmy):
        pass
    def getInteractable(self,rmx,rmy):
        return False