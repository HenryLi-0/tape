'''This file is all about managing what the user sees'''

from settings import *
from PIL import ImageTk, Image
import time, random
from subsystems.render import *
from subsystems.fancy import displayText, generateColorBox, generateBorderBox
from subsystems.visuals import OrbVisualObject, PathVisualObject, ButtonVisualObject, EditableTextBoxVisualObject, DummyVisualObject, PointVisualObject, PointConnectionVisualObject
from subsystems.counter import Counter
from subsystems.pathing import pointAt, roundf, tcoordVelocity
from subsystems.sprite import *

class Interface:
    def __init__(self):
        self.mx = 0
        self.my = 0
        self.mPressed = False
        self.mRising = False
        self.fps = 0
        self.ticks = 0
        self.activity = ""
        self.c = Counter()
        '''Generate Icons'''
        i_plusIconIdle = generateColorBox((35,35),hexColorToRGBA(BACKGROUND_COLOR))
        placeOver(i_plusIconIdle, generateBorderBox((29,29),3, hexColorToRGBA(FRAME_COLOR)), (0,0))
        placeOver(i_plusIconIdle, PLUS_SIGN_ARRAY, (17,17), True)
        i_plusIconActive = generateColorBox((35,35),hexColorToRGBA(BACKGROUND_COLOR))
        placeOver(i_plusIconActive, generateBorderBox((29,29),3, hexColorToRGBA(SELECTED_COLOR)), (0,0))
        placeOver(i_plusIconActive, PLUS_SIGN_ARRAY, (17,17), True)
        i_trashcabIconIdle = generateColorBox((35,35),hexColorToRGBA(BACKGROUND_COLOR))
        placeOver(i_trashcabIconIdle, generateBorderBox((29,29),3, hexColorToRGBA(FRAME_COLOR)), (0,0))
        placeOver(i_trashcabIconIdle, TRASHCAN_ARRAY, (17,17), True)
        i_trashcabIconActive = generateColorBox((35,35),hexColorToRGBA(BACKGROUND_COLOR))
        placeOver(i_trashcabIconActive, generateBorderBox((29,29),3, hexColorToRGBA(SELECTED_COLOR)), (0,0))
        placeOver(i_trashcabIconActive, TRASHCAN_ARRAY, (17,17), True)

        '''Interactable Visual Objects'''
        '''
        Code:
        a - animation
        es - editor > sprites
        evg - editor > visuals > graph
        o - options
        '''
        self.interactableVisualObjects = {
            -999 : [" ", DummyVisualObject("dummy", (0,0))],
            -998 : [" ", DummyVisualObject("dummy", (0,0))],

            self.c.c():["o",ButtonVisualObject("sprites",(7,0),FRAME_OPTIONS_BUTTON_OFF_ARRAY,FRAME_OPTIONS_BUTTON_ON_ARRAY)],
            self.c.c():["o",ButtonVisualObject("visuals",(134,0),FRAME_OPTIONS_BUTTON_OFF_ARRAY,FRAME_OPTIONS_BUTTON_ON_ARRAY)],
            self.c.c():["o",ButtonVisualObject("project",(261,0),FRAME_OPTIONS_BUTTON_OFF_ARRAY,FRAME_OPTIONS_BUTTON_ON_ARRAY)],

            self.c.c():["es", ButtonVisualObject("new sprite", (338,15), i_plusIconIdle, i_plusIconActive)],
            self.c.c():["es", ButtonVisualObject("delete sprite", (338,65), i_trashcabIconIdle, i_trashcabIconActive)]
    
        }
        #for i in range(10): self.interactableVisualObjects[self.c.c()] = ["a", OrbVisualObject(f"test{i}")]
        '''Noninteractable, Adaptive, Visual Objects'''
        self.pathVisualObject = PathVisualObject(self.c.c(), "path")
        '''Sprites'''
        self.sprites = [
            SingleSprite("test"),
        ]
        self.selectedSprite = 0
        self.selectedProperty = 1
        self.previousSelectedProperty = self.selectedProperty
        self.graphScale = 1.0
        self.graphOffset = 0
        self.timelineScale = 1.0
        self.timelineOffset = 0
        self.spriteListOffset = 0
        self.spriteListVelocity = 0
        self.interacting = -999
        self.editorTab = "p"
        self.previousEditorTab = self.editorTab
        self.stringKeyQueue = ""
        self.animationTime = 0
        self.mouseScroll = 0 
        pass

    def tick(self,mx,my,mPressed,fps,keyQueue,mouseScroll):
        '''Entire Screen: `(0,0) to (1365,697)`: size `(1366,698)`'''
        self.mx = mx if (0<=mx and mx<=1365) and (0<=my and my<=697) else self.mx 
        self.my = my if (0<=mx and mx<=1365) and (0<=my and my<=697) else self.my
        self.mPressed = mPressed > 0
        self.mRising = mPressed==2
        self.fps = fps
        self.ticks += 1 if self.fps==0 else round(RENDER_FPS/self.fps)
        if self.interactableVisualObjects[self.interacting][1].name == "new sprite" and mPressed < 3: 
            self.sprites.append(SingleSprite(f"New Sprite {len(self.sprites)}"))
        if self.interactableVisualObjects[self.interacting][1].name == "delete sprite" and mPressed < 3 and len(self.sprites) > 1: 
            self.sprites.pop(self.selectedSprite)
            self.selectedSprite = max(0, min(self.selectedProperty, len(self.sprites)-1))

        '''Keyboard and Scroll (graph and timeline)'''
        for key in keyQueue: 
            if key in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789":
                self.stringKeyQueue+=key
            else:
                if key=="space":
                    self.stringKeyQueue+=" "
                if key=="BackSpace":
                    self.stringKeyQueue=self.stringKeyQueue[0:-1]
                if key=="Return" or key=="Control_L":
                    self.interacting = -998
                    break
            if self.interacting == -999:
                if self.editorTab == "s":
                    if key in SPRITE_LIST_OFFSET_UP:   self.spriteListVelocity -= 25
                    if key in SPRITE_LIST_OFFSET_DOWN: self.spriteListVelocity += 25
                    if key in EDITOR_VISUAL_OFFSET_LEFT:  
                        if 1 <= self.selectedSprite and self.selectedSprite <= len(self.sprites)-1:
                            temp = self.sprites[self.selectedSprite]
                            self.sprites.pop(self.selectedSprite)
                            self.selectedSprite -= 1
                            self.sprites.insert(self.selectedSprite, temp)
                    if key in EDITOR_VISUAL_OFFSET_RIGHT: 
                        if 0 <= self.selectedSprite and self.selectedSprite <= len(self.sprites)-2:
                            temp = self.sprites[self.selectedSprite]
                            self.sprites.pop(self.selectedSprite)
                            self.selectedSprite += 1
                            self.sprites.insert(self.selectedSprite, temp)
                    if key in EDITOR_VISUAL_POINT_CREATE: 
                        if 953<self.mx and 36<self.my and self.mx<1340 and self.my<542:
                            target = math.floor(((self.my-36)+self.spriteListOffset-25)/30)
                            self.sprites.insert(max(0, min(target, len(self.sprites))), SingleSprite(f"New Sprite {len(self.sprites)}"))
                        else:
                            self.sprites.insert(len(self.sprites), SingleSprite(f"New Sprite {len(self.sprites)}"))
                    if key in EDITOR_VISUAL_POINT_DELETE:
                        if len(self.sprites) > 1:
                            self.sprites.pop(self.selectedSprite)
                if self.editorTab == "v":
                    if key in EDITOR_VISUAL_OFFSET_LEFT:  self.graphOffset -= (self.graphScale+0.000001)
                    if key in EDITOR_VISUAL_OFFSET_RIGHT: self.graphOffset += (self.graphScale+0.000001)
                if key in TIMELINE_OFFSET_LEFT:  self.timelineOffset -= (self.timelineScale+0.000001)
                if key in TIMELINE_OFFSET_RIGHT: self.timelineOffset += (self.timelineScale+0.000001)
            else:
                if self.selectedProperty == 1 and self.editorTab == "v":
                    if self.interactableVisualObjects[self.interacting][1].type == "point":
                        if key in ANIMATION_POINT_POSITION_EDIT:
                            self.interactableVisualObjects[self.interacting][1].setPointData((self.mx-23, self.my-36))
                            
        self.mouseScroll = mouseScroll
        if self.editorTab == "v" and 955<self.mx and 257<self.my and self.mx<1336 and self.my<537 and self.interacting == -999:
            graphScalePrevious = self.graphScale
            self.graphScale = 10**(math.log(self.graphScale+0.000001,10) + self.mouseScroll/2500)-0.000001
            if abs(self.mouseScroll) > 0:
                self.graphOffset -= (self.graphScale-graphScalePrevious)*(self.mx-982)/25
        self.graphScale = 0.001 if self.graphScale < 0.001 else self.graphScale
        self.graphScale = 2000 if 2000 < self.graphScale else self.graphScale
        self.graphOffset = 0 if self.graphOffset < 0 else self.graphOffset
        if 71<self.mx and 558<self.my and self.mx<925 and self.my<679 and self.interacting == -999:
            timelineScalePrevious = self.timelineScale
            self.timelineScale = 10**(math.log(self.timelineScale+0.000001,10) + self.mouseScroll/2500)-0.000001
            if abs(self.mouseScroll) > 0:
                self.timelineOffset -= (self.timelineScale-timelineScalePrevious)*(self.mx-71)/25
            if mPressed:
                self.animationTime = (self.mx-71)*(self.timelineScale+0.000001)/25+self.timelineOffset
                self.animationTime = roundf(round(self.animationTime * RENDER_FPS) / RENDER_FPS, PATH_FLOAT_ACCURACY)
                if self.animationTime < 0: self.animationTime = 0
        self.timelineScale = 0.001 if self.timelineScale < 0.001 else self.timelineScale
        self.timelineScale = 2000 if 2000 < self.timelineScale else self.timelineScale
        self.timelineOffset = 0 if self.timelineOffset < 0 else self.timelineOffset
        if self.editorTab == "s":
            if abs(self.mouseScroll) > 0:
                self.spriteListVelocity = 0
                self.spriteListOffset += self.mouseScroll / 5
            self.spriteListVelocity = self.spriteListVelocity * 0.9
            self.spriteListOffset += self.spriteListVelocity
            if self.spriteListOffset > len(self.sprites)*30-507:
                self.spriteListOffset = len(self.sprites)*30-507
                self.spriteListVelocity = 0
            if self.spriteListOffset < 0: 
                self.spriteListOffset = 0
                self.spriteListVelocity = 0
            self.spriteListOffset = round(self.spriteListOffset)
        else:
            self.spriteListVelocity = 0

        pass

        '''Interacting With...'''
        previousInteracting = self.interacting
        if not(self.mPressed):
            self.interacting = -999
        if self.interacting == -999 and self.mPressed:
            for id in self.interactableVisualObjects:
                if self.interactableVisualObjects[id][0] == "a":
                    if self.interactableVisualObjects[id][1].getInteractable(self.mx - 23, self.my - 36):
                        self.interacting = id
                        break
                if self.interactableVisualObjects[id][0] == "es":
                    if self.interactableVisualObjects[id][1].getInteractable(self.mx - 953, self.my - 36):
                        self.interacting = id
                        break
                if self.interactableVisualObjects[id][0] == "evg":
                    if self.interactableVisualObjects[id][1].type == "point":
                        if self.interactableVisualObjects[id][1].getInteractable(self.mx - 982, self.my - 278):
                            self.interacting = id
                            break
                    elif self.interactableVisualObjects[id][1].type == "connection":
                        if self.interactableVisualObjects[id][1].getInteractable(self.mx - 982, self.my - 36):
                            self.interacting = id
                            break
                if self.interactableVisualObjects[id][0] == "o":
                    if self.interactableVisualObjects[id][1].getInteractable(self.mx - 953, self.my - 558):
                        self.interacting = id
                        break
        if self.interacting != -999:
            section = self.interactableVisualObjects[self.interacting][0]
            if section == "a": 
                self.interactableVisualObjects[self.interacting][1].updatePos(self.mx - 23, self.my - 36)
                self.interactableVisualObjects[self.interacting][1].keepInFrame(903,507)
            if section == "es": 
                self.interactableVisualObjects[self.interacting][1].updatePos(self.mx - 953, self.my - 36)
                self.interactableVisualObjects[self.interacting][1].keepInFrame(388,507)
            if section == "evg": 
                self.interactableVisualObjects[self.interacting][1].updatePos(self.mx - 982, self.my - 278)
                self.interactableVisualObjects[self.interacting][1].keepInFrame(337,233)
            if section == "o": 
                self.interactableVisualObjects[self.interacting][1].updatePos(self.mx - 953, self.my - 558)
                self.interactableVisualObjects[self.interacting][1].keepInFrame(388,123)
        if ((self.mPressed)) and (previousInteracting == -999) and (self.interacting != -999) and (self.interactableVisualObjects[self.interacting][1].type  == "textbox"): 
            self.stringKeyQueue = self.interactableVisualObjects[self.interacting][1].txt
        if (self.interacting != -999) and (self.interactableVisualObjects[self.interacting][1].type  == "textbox"):
            self.interactableVisualObjects[self.interacting][1].updateText(self.stringKeyQueue)
        if (previousInteracting != -999) and (previousInteracting != -998):
            if (self.interactableVisualObjects[previousInteracting][1].type  == "textbox"):
                if not(self.interacting == -998):
                    self.interacting = previousInteracting
                    self.interactableVisualObjects[self.interacting][1].updateText(self.stringKeyQueue)
                else:
                    self.interactableVisualObjects[previousInteracting][1].updateText(self.stringKeyQueue)
            if (self.selectedProperty == 1) and (self.interactableVisualObjects[previousInteracting][1].type  == "point"):
                if not(self.interacting == -998):
                    self.interacting = previousInteracting

        if self.editorTab == "s" and self.interacting == -999:
            if 953<self.mx and 36<self.my and self.mx<1340 and self.my<542:
                if self.mPressed and mPressed < 3:
                    target = math.floor(((self.my-36)+self.spriteListOffset-25)/30)
                    if 0 <= target and target <= len(self.sprites)-1:
                        self.selectedSprite = target

    def getImageAnimation(self):
        '''Animation Interface: `(23,36) to (925,542)`: size `(903,507)`'''
        rmx = self.mx - 23
        rmy = self.my - 36
        img = FRAME_ANIMATION_ARRAY.copy()

        placeOver(img, displayText(f"FPS: {self.fps}", "m"), (55,15))
        placeOver(img, displayText(f"Relative (animation) Mouse Position: ({self.mx-23}, {self.my-36})", "m"), (455,55))
        placeOver(img, displayText(f"Mouse Pressed: {self.mPressed}", "m", colorTXT = (0,255,0,255) if self.mPressed else (255,0,0,255)), (55,55))
        placeOver(img, displayText(f"Rising Edge: {self.mRising}", "m", colorTXT = (0,255,0,255) if self.mRising else (255,0,0,255)), (55,95))
        placeOver(img, displayText(f"Interacting With Element: {self.interacting}", "m"), (455,15))
        placeOver(img, displayText(f"stringKeyQueue: {self.stringKeyQueue}", "m"), (455,95))


        for id in self.interactableVisualObjects:
            if self.interactableVisualObjects[id][0] == "a":
                self.interactableVisualObjects[id][1].tick(img, self.interacting==id)

        tempPath = []
        for id in self.interactableVisualObjects: 
            if self.interactableVisualObjects[id][1].type == "orb": 
                tempPath.append(self.interactableVisualObjects[id][1].positionO.getPosition())
        self.pathVisualObject.tick(img, tempPath)

        for sprite in self.sprites:
            frame = sprite.getFullStateAt(self.animationTime)
            placeOver(img, readImgSingleFullState(frame, sprite.images), (frame[0][0],frame[0][1]), True)

        if self.interacting != -999 and self.interactableVisualObjects[self.interacting][1].type == "point" and self.selectedProperty == 1:
            data = self.sprites[self.selectedSprite].getData("crashtbw"[self.selectedProperty-1])
            coords = iterateThroughPath(data)
            for coord in coords:
                placeOver(img, PATH_POINT_IDLE_ARRAY, coord, True)
            evgP = listEVGPoints(self.interactableVisualObjects)
            extent = findExtentThroughPath(data, evgP.index(self.interacting))
            if extent[-1] > len(evgP)-1:
                extent = extent[0:-2]
            for id in [evgP[index] for index in extent]:
                placeOver(img, ORB_SELECTED_ARRAY if id==self.interacting else ORB_IDLE_ARRAY, self.interactableVisualObjects[id][1].pointData, True)
                

        return arrayToImage(img)
    
    def getImageTimeline(self):
        '''Timeline Interface: `(23,558) to (925,680)`: size `(903,123)`'''
        img = FRAME_TIMELINE_ARRAY.copy()
        startI = round(self.timelineOffset/(10**math.floor(math.log(self.timelineScale+0.000001,10)+1)))
        for i in range(startI - 3, startI + 33):
            pos = 48 + ((i*(10**math.floor(math.log(self.timelineScale+0.000001,10)+1)))-self.timelineOffset)*(1/(self.timelineScale+0.000001))*25
            if pos > 902: break
            if pos > 48: 
                placeOver(img, FRAME_EDITOR_VISUALS_GRAPH_BAR_ARRAY, (pos, 25))
                time = roundf((i*(10**math.floor(math.log(self.timelineScale+0.000001,10)+1))),2)
                if time >= 1:
                    if time < 3600:
                        time = "{:02}:{:02}".format(math.floor(time/60), roundf(time%60,2))
                    else:
                        time = "{:02}:{:02}:{:02}".format(math.floor(time/3600), math.floor((time-3600*math.floor(time/3600))/60), roundf(time%60,2))
                else:
                    time = str(time)
                placeOver(img, displayText(time, "s"), (pos,15), True)
        
        pos = (self.animationTime-self.timelineOffset)*25/(self.timelineScale+0.000001) + 47
        if 46 < pos and pos < 896:
            placeOver(img, FRAME_TIMELINE_READER_ARRAY, (max(51,pos), 3))

        return arrayToImage(img)
    
    def getImageEditor(self):
        '''Editor Interface: `(953,36) to (1340,542)`: size `(388,507)`'''
        img = FRAME_EDITOR_VISUALS_ARRAY.copy() if self.editorTab=="v" else FRAME_EDITOR_ARRAY.copy()
        if self.editorTab == "s":
            '''Sprites Tab!'''
            placeOver(img, generateColorBox((348,25), hexColorToRGBA(SELECTED_COLOR)), (20, 21+self.selectedSprite*30-self.spriteListOffset))
            i = 0
            for sprite in self.sprites:
                placeOver(img, displayText(sprite.getName(), "m"), (25, 25+i*30-self.spriteListOffset))
                i+=1
            
            for id in self.interactableVisualObjects:
                if self.interactableVisualObjects[id][0] == "es":
                    self.interactableVisualObjects[id][1].tick(img, self.interacting==id)

        if self.editorTab == "v":
            '''Visuals Tab!'''
            if self.selectedSprite != -999:
                '''Graph Display'''
                placeOver(img, setLimitedSize(self.sprites[self.selectedSprite].getImageAt(self.animationTime), 50), (25,25))
                placeOver(img, displayText(self.sprites[self.selectedSprite].getName(), "l"), (110,37))

                startI = round(self.graphOffset/(10**math.floor(math.log(self.graphScale+0.000001,10)+1)))
                for i in range(startI - 3, startI + 33):
                    pos = 29 + ((i*(10**math.floor(math.log(self.graphScale+0.000001,10)+1)))-self.graphOffset)*(1/(self.graphScale+0.000001))*25
                    if pos > 362: break
                    if pos > 29: 
                        placeOver(img, FRAME_EDITOR_VISUALS_GRAPH_BAR_ARRAY, (pos, 242))
                        time = roundf((i*(10**math.floor(math.log(self.graphScale+0.000001,10)+1))),2)
                        if time >= 1:
                            if time < 3600:
                                time = "{:02}:{:02}".format(math.floor(time/60), roundf(time%60,2))
                            else:
                                time = "{:02}:{:02}:{:02}".format(math.floor(time/3600), math.floor((time-3600*math.floor(time/3600))/60), roundf(time%60,2))
                        else:
                            time = str(time)
                        placeOver(img, displayText(time, "s"), (pos,492), True)
                
                '''Get Data and Stuff'''
                data = self.sprites[self.selectedSprite].getData("crashtbw"[self.selectedProperty-1])
                dataCheck("crashtbw"[self.selectedProperty-1], data)
                if self.selectedProperty == 1: 
                    pathP = iterateThroughPath(data, True)
                    pathV = [tcoordVelocity(partition) for partition in pathP]
                else: 
                    pathP = iterateThroughSingle(data, True)
                lenData = round(len(data)/3)

                '''Keybinds'''
                regen = False
                requestSelectedProperty = self.selectedProperty
                if self.previousEditorTab != "v":
                    self.stringKeyQueue = ""
                else:
                    for i in range(1,8+1):
                        if str(i) in self.stringKeyQueue: requestSelectedProperty = i
                    connectionEdit = ""
                    for keybind in EDITOR_VISUAL_LINEAR_CONNECTION:
                        if str(keybind) in self.stringKeyQueue: connectionEdit = "L"
                    for keybind in EDITOR_VISUAL_SMOOTH_CONNECTION:
                        if str(keybind) in self.stringKeyQueue: connectionEdit = "S"

                    for keybind in EDITOR_VISUAL_POINT_CREATE:
                        if str(keybind) in self.stringKeyQueue and self.interacting == -999:
                            x = (self.mx-982)*(self.graphScale+0.000001)/25+self.graphOffset
                            y = 100-((self.my-279)/2.33)   
                            timeStamps = [data[i*3] for i in range(lenData)]
                            low = -1
                            for i in range(len(timeStamps)-1):
                                if timeStamps[i]<=x: low = i
                                else: break
                            for item in ["L", (random.randrange(0,903),random.randrange(0,507)) if self.selectedProperty == 1 else y, x]: data.insert((low+1)*3, item)
                            self.sprites[self.selectedSprite].setData("crashtbw"[self.selectedProperty-1], data)
                            dataCheck("crashtbw"[self.selectedProperty-1], data)
                            if self.selectedProperty == 1: 
                                pathP = iterateThroughPath(data, True)
                                pathV = [tcoordVelocity(partition) for partition in pathP]
                            else: 
                                pathP = iterateThroughSingle(data, True)
                            lenData = round(len(data)/3)
                            self.interacting = -999
                            regen = True                                
                    for keybind in EDITOR_VISUAL_POINT_DELETE:
                        if str(keybind) in self.stringKeyQueue and self.interacting != -999:
                            if self.interactableVisualObjects[self.interacting][1].type == "point":
                                index = listEVGPoints(self.interactableVisualObjects).index(self.interacting)
                                for i in range(3): data.pop(index*3)
                                self.sprites[self.selectedSprite].setData("crashtbw"[self.selectedProperty-1], data)
                                lenData = round(len(data)/3)
                                self.interacting = -999
                                regen = True
                    
                    self.stringKeyQueue = ""

                '''Graph Points and Editing'''
                evgPoints = listEVGPoints(self.interactableVisualObjects)
                evgConnections = listEVGConnections(self.interactableVisualObjects)
                if self.previousEditorTab != "v" or self.selectedProperty != self.previousSelectedProperty or regen:
                    self.graphLastCheck = self.ticks
                    if len(evgPoints) > lenData:
                        for i in range(len(evgPoints)-lenData): self.interactableVisualObjects.pop(evgPoints[i])
                    else:
                        i = 0
                        while len(evgPoints) + i < lenData:
                            self.interactableVisualObjects[self.c.c()] = ["evg",PointVisualObject("point",(0,0))]
                            i+=1

                    if len(evgConnections) > lenData-1:
                        for i in range(len(evgConnections)-(lenData-1)): self.interactableVisualObjects.pop(evgConnections[i])
                    else:
                        i = 0
                        while len(evgConnections) + i < lenData-1:
                            self.interactableVisualObjects[self.c.c()] = ["evg",PointConnectionVisualObject("connection",(0,0),(0,0))]
                            i+=1

                    evgPoints = listEVGPoints(self.interactableVisualObjects)
                    evgConnections = listEVGConnections(self.interactableVisualObjects)

                    for i in range(len(evgPoints)):
                        self.interactableVisualObjects[evgPoints[i]][1].setPointData(data[i*3+1])
                        if self.selectedProperty == 1: self.interactableVisualObjects[evgPoints[i]][1].updatePos((data[i*3]-self.graphOffset)*25/(self.graphScale+0.000001),223)
                        else: self.interactableVisualObjects[evgPoints[i]][1].updatePos((data[i*3]-self.graphOffset)*25/(self.graphScale+0.000001),(100-data[i*3+1])*2.23)


                    if self.selectedProperty == 1:
                        for i in range(len(evgConnections)): self.interactableVisualObjects[evgConnections[i]][1].setPathData(pathV[i])
                    else:
                        for i in range(len(evgConnections)): self.interactableVisualObjects[evgConnections[i]][1].setPathData(pathP[i])
                else:

                    if self.selectedProperty == 1:
                        if self.interactableVisualObjects[self.interacting][1].type == "point":
                            self.interacting = self.interacting

                    evgPoints = listEVGPoints(self.interactableVisualObjects)
                    if self.interacting == -999:
                        for i in range(len(evgPoints)):
                            self.interactableVisualObjects[evgPoints[i]][1].setPointData(data[i*3+1])
                            if self.selectedProperty == 1:
                                self.interactableVisualObjects[evgPoints[i]][1].updatePos((data[i*3]-self.graphOffset)*25/(self.graphScale+0.000001),223)
                            else:
                                self.interactableVisualObjects[evgPoints[i]][1].updatePos((data[i*3]-self.graphOffset)*25/(self.graphScale+0.000001),(100-data[i*3+1])*2.23)
                    for i in range(len(evgPoints)):
                        x, y = self.interactableVisualObjects[evgPoints[i]][1].positionO.getPosition()
                        data[i*3] = x*(self.graphScale+0.000001)/25+self.graphOffset
                        if self.selectedProperty == 1:
                            data[i*3+1] = self.interactableVisualObjects[evgPoints[i]][1].pointData
                        else:
                            y = 100-(y/2.33)
                            data[i*3+1] = y if abs(data[i*3+1]-y) > 5 else data[i*3+1]
                    evgPoints = [data[i*3] for i in range(len(evgPoints))]
                    evgsS = evgPoints.copy()
                    evgsS.sort()
                    if evgPoints != evgsS:
                        dataS = [[data[i*3],data[i*3+1],data[i*3+2]] for i in range(lenData)]
                        dataS.sort(key = lambda x: x[0])
                        data = []
                        for timeState in dataS: 
                            for thing in timeState: data.append(thing)
                    dataCheck("crashtbw"[self.selectedProperty-1], data)
                    self.sprites[self.selectedSprite].setData("crashtbw"[self.selectedProperty-1], data)
                    evgConnections = listEVGConnections(self.interactableVisualObjects)
                    for i in range(len(evgConnections)):
                        if self.selectedProperty == 1: 
                            self.interactableVisualObjects[evgConnections[i]][1].setPathData(pathV[i])
                        else: self.interactableVisualObjects[evgConnections[i]][1].setPathData(pathP[i])
                    

                self.previousSelectedProperty = self.selectedProperty
                evgPoints = listEVGPoints(self.interactableVisualObjects)
                evgConnections = listEVGConnections(self.interactableVisualObjects)
                if self.interacting != -999:
                    if self.interactableVisualObjects[self.interacting][1].type == "point":
                        i = evgPoints.index(self.interacting)
                        x, y = self.interactableVisualObjects[self.interacting][1].positionO.getPosition()
                        x = x*(self.graphScale+0.000001)/25+self.graphOffset
                        y = 100-(y/2.33)                        
                        placeOver(img, displayText(f"P {i+1}: {(roundf(x,2),roundf(y,2))}", "m"), (89,190), True)
                    if self.interactableVisualObjects[self.interacting][1].type == "connection":
                        i = evgConnections.index(self.interacting)
                        if data[i*3+2] == "L": placeOver(img, displayText(f"C {i+1}: Linear", "m"), (89,190), True)
                        elif data[i*3+2] == "S": placeOver(img, displayText(f"C {i+1}: Smooth", "m"), (89,190), True)
                        else: placeOver(img, displayText(f"C {i+1}: {data[i*3+2]}", "m"), (89,190), True)
                        if connectionEdit in ["L", "S"]:
                            data[i*3+2] = connectionEdit
                            self.sprites[self.selectedSprite].setData("crashtbw"[self.selectedProperty-1], data)

                evgPoints = listEVGPoints(self.interactableVisualObjects)
                evgConnections = listEVGConnections(self.interactableVisualObjects)
                if 1 <= self.selectedProperty and self.selectedProperty <= 8:
                    placeOver(img, displayText(f"({self.selectedProperty}) - {PROPERTY_DISPLAY_NAMES[self.selectedProperty-1]}", "m"), (89,130), True)
                    if self.interacting == -999:
                        placeOver(img, displayText(f"[P: {len(evgPoints)}, C: {len(evgConnections)}, S: {sum([len(p) for p in pathP])}]", "m"), (89,190), True)


                '''Apperance Panel'''
                apperancePanel = generateColorBox((189,210), hexColorToRGBA(BACKGROUND_COLOR))
                placeOver(apperancePanel, generateBorderBox((183,206),3,hexColorToRGBA(FRAME_COLOR)), (0,0))
                resizedImgs = [setLimitedSize(spriteImg, 79) for spriteImg in self.sprites[self.selectedSprite].images]
                yOffset = 6
                for i in range(len(resizedImgs)):
                    # each image is 85x85 (including borders)
                    y, x, temp = resizedImgs[i].shape
                    imgB = generateColorBox((x+6,y+6),hexColorToRGBA(BACKGROUND_COLOR))
                    placeOver(imgB, generateBorderBox((x, y), 3, hexColorToRGBA(FRAME_COLOR)), (0,0))
                    placeOver(imgB, resizedImgs[i], (3,3))
                    placeOver(apperancePanel, imgB, (90*(i%2)+5, yOffset))
                    try: yOffset += max(resizedImgs[(i - i % 2)].shape[0], resizedImgs[(i - i % 2 + 1)].shape[0])
                    except: yOffset += resizedImgs[(i - i % 2)].shape[0]
                placeOver(img, apperancePanel, (199,0))

                    





                for id in self.interactableVisualObjects:
                    if self.interactableVisualObjects[id][0] == "evg":
                        if self.interactableVisualObjects[id][1].type == "connection":
                            self.interactableVisualObjects[id][1].tick(img, self.interacting==id, self.graphOffset, self.graphScale)
                for id in self.interactableVisualObjects:
                    if self.interactableVisualObjects[id][0] == "evg":
                        if self.interactableVisualObjects[id][1].type != "connection":
                            self.interactableVisualObjects[id][1].tick(img, self.interacting==id)
                
                self.selectedProperty = requestSelectedProperty
                placeOver(img, FRAME_EDITOR_VISUALS_GRAPH_ARRAY, (0,219))
                # placeOver(img, PLACEHOLDER_IMAGE_5_ARRAY, ((100-self.graphOffset)*25/(self.graphScale+0.000001)+29,219), True)
        if self.editorTab == "p":
            '''About Project Tab!'''
            placeOver(img, displayText("Project:", "m"),                                                            (15,EDITOR_SPACING(1))) 
            placeOver(img, displayText("Name: please implement this", "m"),                                         (20,EDITOR_SPACING(2)))
            placeOver(img, displayText("Size: 1155 MB (please implement this)", "m"),                               (20,EDITOR_SPACING(3)))

            placeOver(img, displayText("Elements:", "m"),                                                           (15,EDITOR_SPACING(5)))
            placeOver(img, displayText("Sprites: please implement this", "m"),                                      (20,EDITOR_SPACING(6))) 
            placeOver(img, displayText("Folders: please implement this", "m"),                                      (20,EDITOR_SPACING(7))) 
            placeOver(img, displayText("Paths: please implement this", "m"),                                        (20,EDITOR_SPACING(8))) 
            placeOver(img, displayText("Total Path Elements: please implement this", "m"),                          (20,EDITOR_SPACING(9))) 
            placeOver(img, displayText("Total Path Waypoints: please implement this", "m"),                         (20,EDITOR_SPACING(10))) 
            placeOver(img, displayText(f"Interactable Visual Objects: {len(self.interactableVisualObjects)}", "m"), (20,EDITOR_SPACING(11))) 

            placeOver(img, displayText("Dates:", "m"),                                                              (15,EDITOR_SPACING(13)))
            placeOver(img, displayText("Created On: ", "m"),                                                        (20,EDITOR_SPACING(14)))  
            placeOver(img, displayText("Last Saved: ", "m"),                                                        (20,EDITOR_SPACING(15)))  
            placeOver(img, displayText("Version Created: ", "m"),                                                   (20,EDITOR_SPACING(16)))  
            placeOver(img, displayText("Current Version: ", "m"),                                                   (20,EDITOR_SPACING(17)))  
            placeOver(img, displayText("Time Spent: ", "m"),                                                        (20,EDITOR_SPACING(18))) 

        return arrayToImage(img)
    
    def getImageOptions(self):
        '''Options Interface: `(953,558) to (1340,680)`: size `(388,123)`'''
        img = FRAME_OPTIONS_ARRAY.copy()
        
        self.previousEditorTab = self.editorTab 

        for id in self.interactableVisualObjects:
            if self.interactableVisualObjects[id][0] == "o":
                if self.interacting==id: self.editorTab = self.interactableVisualObjects[id][1].name[0]
                self.interactableVisualObjects[id][1].tick(img, self.interacting==id or self.editorTab==self.interactableVisualObjects[id][1].name[0])

        if 23 <= self.mx and self.mx <= 925 and 36 <= self.my and self.my <= 542:
            placeOver(img, displayText(f"rx: {self.mx-23}", "l"), (20,83)) 
            placeOver(img, displayText(f"ry: {self.my-36}", "l"), (120,83))
        else:            
            placeOver(img, displayText(f" x: {self.mx}", "l", colorTXT=(155,155,155,255)), (20,83)) 
            placeOver(img, displayText(f" y: {self.my}", "l", colorTXT=(155,155,155,255)), (120,83))
        placeOver(img, displayText("Sprites                  Visuals                  Project", "m"), (193, 31), True)
        placeOver(img, GEAR_ARRAY, (338,80))
        return arrayToImage(img)
    
    def saveState(self):
        pass

    def close(self):
        pass