'''This file contains classes all about the visual objects the user sees'''

import time, numpy, random, math
from subsystems.point import addP, subtractP, roundf
from subsystems.render import placeOver
from subsystems.fancy import *
from settings import *

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
    
'''Hitboxes'''

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
        '''Returns whether or not the mouse is in the bounding box of interaction'''
        return (self.ix < rmx) and (rmx < (self.ix+self.bbox[0])) and (self.iy < rmy) and (rmy < (self.iy+self.bbox[1]))
    def getPosition(self): return (self.ix, self.iy)
    def getX(self): return self.ix
    def getY(self): return self.iy
    def getBBOX(self): return self.bbox
    def setPosition(self, position: tuple|list): self.ix, self.iy = position
    def setX(self, nx): self.ix = nx
    def setY(self, ny): self.iy = ny
    def setBBOX(self, nbbox): self.bbox = nbbox

class FixedRegionPositionalBox:
    '''Just remembers where the object is supposed to be on screen, given the mouse position and updates when the mouse is in a specific region. Not movable by interaction.'''
    def __init__(self, pointA:tuple|list = (0,0), pointB:tuple|list = (10,10)):
        '''Point A and Point B are two opposite corners of a region!'''
        self.pointA = (min(pointA[0], pointB[0]), min(pointA[1], pointB[1]))
        self.pointB = (max(pointA[0], pointB[0]), max(pointA[1], pointB[1]))
    def process(self, interact, rmx, rmy):
        '''Should be called whenever the position wants to question its position'''
        pass
    def getInteract(self, rmx, rmy):
        '''Returns whether or not the mouse is in the region of interaction'''
        return (self.pointA[0] < rmx) and (rmx < self.pointB[0]) and (self.pointA[1] < rmy) and (rmy < self.pointB[1])
    def getPosition(self): return self.pointA
    def getX(self): return self.pointA[0]
    def getY(self): return self.pointA[1]
    def getRegion(self): return (self.pointA, self.pointB)
    def setPosition(self, position: tuple|list): 
        self.pointB = subtractP(self.pointB, subtractP(self.pointA, position))
        self.pointA = position
    def setRegion(self, pointA, pointB):
        self.pointA = (min(pointA[0], pointB[0]), min(pointA[1], pointB[1]))
        self.pointB = (max(pointA[0], pointB[0]), max(pointA[1], pointB[1]))

'''Visual Objects'''

from settings import ORB_IDLE, ORB_SELECTED

class VisualObject:
    '''Basic template for Visual Objects'''
    def keepInFrame(self, minX, minY, maxX, maxY):
        pos = self.positionO.getPosition()
        if pos[0] < minX or maxX < pos[0] or pos[1] < minY or maxY < pos[1]:
            self.positionO.setPosition((max(minX,min(pos[0],maxX)), max(minY,min(pos[1],maxY))))
    def getInteractable(self, rmx, rmy):
        return self.positionO.getInteract(rmx, rmy)
    def keyAction(self, keys):
        pass

# class PathWorker: 
#     '''Format inputs as a set-like of [bezier?, [coords], steps]'''
#     def get(pathData):
#         return bezierPathCoords(pathData[0], pathData[1]) if pathData[0] else straightPathCoords(pathData[0], pathData[1])
    
# class PathVisualObject:
#     '''A path.'''
#     def __init__(self, id, name):
#         self.id = id
#         self.name = name
#         self.path = [(0,0,0)]
#     def tick(self, window, points):
#         '''Takes in a set of points and draws the path'''
#         self.path = bezierPathCoords(points, 10)
#         self.path = mergeCoordRotationPath(self.path, pointNextCoordRotationPath(self.path))
#         for coord in self.path:
#             placeOver(window, CURSOR_SELECT_ARRAY, (coord[0], coord[1]), True)

class OrbVisualObject(VisualObject):
    '''A movable point.'''
    def __init__(self, name, pos:tuple|list = (random.randrange(0,903), random.randrange(0,507))):
        self.type = "orb"
        self.name = name
        self.lastInteraction = time.time()
        self.positionO = CircularPositionalBox(50)
        self.positionO.setPosition(pos)
    def tick(self, img, visualactive, active):
        if active: self.lastInteraction = time.time()
        placeOver(img, ORB_SELECTED if visualactive else ORB_IDLE, self.positionO.getPosition(), True)
        placeOver(img, displayText(self.name, "s"), self.positionO.getPosition(), True)
    def updatePos(self, rmx, rmy):
        self.positionO.setPosition((rmx, rmy))


class ButtonVisualObject(VisualObject):
    '''A button.'''
    def __init__(self, name, pos:tuple|list, img:Image, img2:Image):
        self.type = "button"
        self.name = name
        self.lastInteraction = time.time()
        self.img = img
        self.img2 = img2
        self.positionO = RectangularPositionalBox((img.width,img.height), pos[0], pos[1])
    def tick(self, img, visualactive, active):
        if active: self.lastInteraction = time.time()
        placeOver(img, self.img2 if active else self.img, self.positionO.getPosition(), False)
    def updatePos(self, rmx, rmy):
        pass
    
class EditableTextBoxVisualObject(VisualObject):
    '''An editable text box.'''
    def __init__(self, name, pos:tuple|list, startTxt= "", intOnly = False):
        self.type = "textbox"
        self.name = name
        self.lastInteraction = time.time()
        self.txt = str(startTxt)
        self.txtImg = displayText(self.txt, "m")
        self.intOnly = intOnly
        self.positionO = RectangularPositionalBox((max(self.txtImg.width,10),max(self.txtImg.height,23)), pos[0], pos[1])
        self.underlineIdle = generateColorBox((self.positionO.getBBOX()[0],3), FRAME_COLOR_RGBA)
        self.underlineActive = generateColorBox((self.positionO.getBBOX()[0],3), SELECTED_COLOR_RGBA)
    def tick(self, img, visualactive, active):
        if active: self.lastInteraction = time.time()
        temp = generateColorBox(addP(self.positionO.getBBOX(), (0,3)), FRAME_COLOR_RGBA if visualactive else BACKGROUND_COLOR_RGBA)
        placeOver(temp, self.underlineActive if visualactive else self.underlineIdle, (0, self.positionO.getBBOX()[1]))
        placeOver(img, temp, self.positionO.getPosition())
        placeOver(img, self.txtImg, self.positionO.getPosition(), False)
    def updateText(self, txt):
        if self.intOnly:
            if txt == "" or len(str(txt)) == 0:
                self.txt = "0"
            else:
                temp = list(str(txt))
                for item in temp:
                    if item not in "0123456789":
                        while item in temp: temp.remove(item)
                    self.txt = "".join(temp)
        self.txtImg = displayText(self.txt, "m")
        self.positionO.setBBOX((max(self.txtImg.width+3,10),max(self.txtImg.height,23)))
        self.underlineIdle = generateColorBox((self.positionO.getBBOX()[0],3), FRAME_COLOR_RGBA)
        self.underlineActive = generateColorBox((self.positionO.getBBOX()[0],3), SELECTED_COLOR_RGBA)
    def keyAction(self, keys):
        self.lastInteraction = time.time()
        prevtxt = self.txt
        for key in keys:
            if key in KB_CONFIRM: break
            if key == -1:self.txt = self.txt[0:-1]
            else: self.txt += chr(key)
        if prevtxt != self.txt:
            self.updateText(self.txt)
    def updatePos(self, rmx, rmy):
        pass

class DummyVisualObject(VisualObject):
    '''I sit around doing nothing and can store data. A little better that one group member in randomly assigned class projects. That person didn't deserve that 100, did they now? (joke)'''
    def __init__(self, name, pos:tuple|list, data = None):
        self.type = "dummy"
        self.name = name
        self.lastInteraction = time.time()
        self.positionO = RectangularPositionalBox((0,0), pos[0], pos[1])
        self.data = data
    def tick(self, img, visualactive, actives):
        pass
    def updatePos(self, rmx, rmy):
        pass
    def keepInFrame(self, minX, minY, maxX, maxY):
        pass
    def getInteractable(self,rmx,rmy):
        return False

class IconVisualObject(VisualObject):
    '''An icon, basically a fancy button.'''
    # generateIcon(img, active = False, size = (29,29), color = "")
    def __init__(self, name, pos:tuple|list, icon:Image, size:tuple|list = (29,29), outline = True):
        self.type = "icon"
        self.name = name
        self.lastInteraction = time.time()
        if outline:
            self.img = generateOutlineIcon(icon, False, size)
            self.img2 = generateOutlineIcon(icon, True, size)
        else:
            self.img = generateHoverIcon(icon, False)
            self.img2 = generateHoverIcon(icon, True)
        self.positionO = RectangularPositionalBox((self.img.width,self.img.height), pos[0], pos[1])
    def tick(self, img, visualactive, active):
        if active: self.lastInteraction = time.time()
        placeOver(img, self.img2 if visualactive else self.img, self.positionO.getPosition(), False)
        if active: placeOver(img, displayText(self.name, "s", (0,0,0,200)), self.positionO.getPosition(), False)
    def updatePos(self, rmx, rmy):
        pass

class ToggleVisualObject(VisualObject):
    '''A toggle, basically a fancy button/icon, but this time with two faces, on and off that switch on rising detection of clicks!'''
    # generateIcon(img, active = False, size = (29,29), color = "")
    def __init__(self, name, pos:tuple|list, iconOn:Image, iconOff:Image, size:tuple|list = (29,29), runOn = lambda: 0, runOff = lambda: 0):
        self.type = "icon"
        self.name = name
        self.lastInteraction = time.time()
        self.img = generateOutlineIcon(iconOn, False, size)
        self.img2 = generateOutlineIcon(iconOff, False, size)
        self.positionO = RectangularPositionalBox((self.img.width,self.img.height), pos[0], pos[1])
        self.active = 0
        self.state = False
        self.runOn = runOn
        self.runOff = runOff
    def tick(self, img, visualactive, active):
        if active: self.lastInteraction = time.time()
        if active: self.active +=1
        else: self.active = 0
        if self.active == 1:
            self.state = not(self.state)
            if self.state == True: self.runOn()
            if self.state == False: self.runOff()
        placeOver(img, self.img2 if self.state else self.img, self.positionO.getPosition(), False)
        if active: placeOver(img, displayText(self.name, "s", (0,0,0,200)), self.positionO.getPosition(), False)
    def setToggle(self, runOn, runOff):
        self.runOn = runOn
        self.runOff = runOff
    def updatePos(self, rmx, rmy):
        pass

class HorizontalSliderVisualObject(VisualObject):
    '''A slider!!! No way!!! (horizontal)'''
    def __init__(self, name, pos:tuple|list=(random.randrange(0,20), random.randrange(0,20)), length = random.randrange(50,100), sliderRange = [1,100]):
        self.type = "slider"
        self.name = name
        self.lastInteraction = time.time()
        self.originalPos = pos
        self.length = length
        self.positionO = CircularPositionalBox(15)
        self.positionO.setPosition(addP(pos, (10,10)))
        self.displayScalar = sliderRange[1]-sliderRange[0]
        self.sliderRange = sliderRange
        self.bar = generateColorBox((length, 20), (0,0,0,0))
        placeOver(self.bar, generateColorBox((length, 2), hexColorToRGBA(FRAME_COLOR)), (0,9))
        placeOver(self.bar, generateColorBox((3, 20), hexColorToRGBA(FRAME_COLOR)), (0,0))
        placeOver(self.bar, generateColorBox((3, 20), hexColorToRGBA(FRAME_COLOR)), (length-3,0))
        self.updatePos(-9999999, 0)
    def tick(self, img, visualactive, active):
        if active: self.lastInteraction = time.time()
        placeOver(img, self.bar, self.originalPos)
        placeOver(img, POINT_SELECTED if visualactive else POINT_IDLE, self.positionO.getPosition(), True)
        if visualactive: placeOver(img, displayText(str(round((self.positionO.getX()-self.originalPos[0])/self.length*self.displayScalar+self.sliderRange[0])), "s", (0,0,0,150), (255,255,255,255)), addP(self.positionO.getPosition(), (0,25)), True)
    def getData(self):
        return round((self.positionO.getX()-self.originalPos[0])/self.length*self.displayScalar+self.sliderRange[0])
    def setData(self, extent):
        self.updatePos(self.originalPos[0] + (extent-self.sliderRange[0])/self.displayScalar*self.length, 0)
    def updatePos(self, rmx, rmy):
        self.positionO.setX(max(self.originalPos[0], min(rmx, self.originalPos[0] + self.length)))
    def keepInFrame(self, minX, minY, maxX, maxY):
        pos = self.positionO.getPosition()
        if pos[0] < minX or maxX < pos[0] or pos[1] < minY or maxY < pos[1]:
            self.positionO.setPosition((round(max(minX,min(pos[0],maxX))), round(max(minY,min(pos[1],maxY)))))
    def getInteractable(self, rmx, rmy):
        return self.positionO.getInteract(rmx, rmy)

class VerticalSliderVisualObject(VisualObject):
    '''A slider!!! No way!!! (vertical)'''
    def __init__(self, name, pos:tuple|list=(random.randrange(0,20), random.randrange(0,20)), length = random.randrange(50,100), sliderRange = [1,100]):
        self.type = "slider"
        self.name = name
        self.lastInteraction = time.time()
        self.originalPos = pos
        self.length = length
        self.positionO = CircularPositionalBox(15)
        self.positionO.setPosition(addP(pos, (10,10)))
        self.displayScalar = sliderRange[1]-sliderRange[0]
        self.sliderRange = sliderRange
        self.bar = generateColorBox((20, length), (0,0,0,0))
        placeOver(self.bar, generateColorBox((2, length), hexColorToRGBA(FRAME_COLOR)), (9,0))
        placeOver(self.bar, generateColorBox((20, 3), hexColorToRGBA(FRAME_COLOR)), (0,0))
        placeOver(self.bar, generateColorBox((20, 3), hexColorToRGBA(FRAME_COLOR)), (0, length-3))
        self.updatePos(0, -9999999)
    def tick(self, img, visualactive, active):
        if active: self.lastInteraction = time.time()
        placeOver(img, self.bar, self.originalPos)
        placeOver(img, POINT_SELECTED if visualactive else POINT_IDLE, self.positionO.getPosition(), True)
        if visualactive: placeOver(img, displayText(str(round((self.positionO.getY()-self.originalPos[1])/self.length*self.displayScalar+self.sliderRange[0])), "s", (0,0,0,150), (255,255,255,255)), addP(self.positionO.getPosition(), (0,25)), True)
    def getData(self):
        return round((self.positionO.getY()-self.originalPos[1])/self.length*self.displayScalar+self.sliderRange[0])
    def setData(self, extent):
        self.updatePos(0, self.originalPos[1] + (extent-self.sliderRange[0])/self.displayScalar*self.length)
    def updatePos(self, rmx, rmy):
        self.positionO.setY(max(self.originalPos[1], min(rmy, self.originalPos[1] + self.length)))
    def keepInFrame(self, minX, minY, maxX, maxY):
        pos = self.positionO.getPosition()
        if pos[0] < minX or maxX < pos[0] or pos[1] < minY or maxY < pos[1]:
            self.positionO.setPosition((round(max(minX,min(pos[0],maxX))), round(max(minY,min(pos[1],maxY)))))
    def getInteractable(self, rmx, rmy):
        return self.positionO.getInteract(rmx, rmy)

class CheckboxVisualObject(VisualObject):
    '''A checkbox, basically a simple toggle.'''
    def __init__(self, name, pos:tuple|list, size:tuple|list = (29,29), state = False):
        self.type = "checkbox"
        self.name = name
        self.lastInteraction = time.time()
        self.img = generateOutlineIcon(generateColorBox(size, (255,0,0,255)), False, size)
        self.img2 = generateOutlineIcon(generateColorBox(size, (0,255,0,255)), False, size)
        self.positionO = RectangularPositionalBox((self.img.width,self.img.height), pos[0], pos[1])
        self.active = 0
        self.state = state
    def tick(self, img, visualactive, active):
        if active: self.lastInteraction = time.time()
        if active: self.active +=1
        else: self.active = 0
        if self.active == 1: self.state = not(self.state)
        placeOver(img, self.img2 if self.state else self.img, self.positionO.getPosition(), False)
    def updatePos(self, rmx, rmy):
        pass

class TextButtonPushVisualObject(VisualObject):
    '''A button, but it has text! and it resets itself after some ticks!'''
    def __init__(self, name, text:numpy.ndarray, pos:tuple|list, ticks = 60):
        self.type = "button"
        self.name = name
        self.lastInteraction = time.time()
        temp = displayText(str(text), "m")
        self.img = generateOutlineIcon(temp, False, (temp.width, temp.height))
        self.img2 = generateOutlineIcon(temp, True, (temp.width, temp.height))
        self.positionO = RectangularPositionalBox((self.img.width,self.img.height), pos[0], pos[1])
        self.lastPressed = 9999999
        self.state = False
        self.time = ticks
    def tick(self, img, visualactive, active):
        if active: self.lastInteraction = time.time()
        if active: self.lastPressed = 0
        else: self.lastPressed += 1
        self.state = (self.time > self.lastPressed)
        placeOver(img, self.img2 if self.state else self.img, self.positionO.getPosition(), False)
    def updatePos(self, rmx, rmy):
        pass