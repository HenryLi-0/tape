'''This file is all about managing what the user sees'''

from settings import *
from PIL import ImageTk, Image
from tkinter import filedialog
import time, random, ast, cv2
from subsystems.render import *
from subsystems.fancy import *
from subsystems.visuals import *
from subsystems.counter import Counter
from subsystems.pathing import pointAt, roundf, tcoordVelocity
from subsystems.sprite import *
from subsystems.simplefancy import *
from subsystems.bay import CacheManager

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
        self.cache = CacheManager()
        '''Interactable Visual Objects'''
        '''
        Code:
        a - animation
        es - editor > sprites
        ev - editor > visuals
        evg - editor > visuals > graph
        ep - editor > project
        o - options
        '''
        self.interactableVisualObjects = {
            -999 : [" ", DummyVisualObject("dummy", (0,0))], # used for not interacting with anything
            -998 : [" ", DummyVisualObject("dummy", (0,0))], # used for text boxes

            -99 : ["o",ButtonVisualObject("sprites",(7,0),FRAME_OPTIONS_BUTTON_OFF_ARRAY,FRAME_OPTIONS_BUTTON_ON_ARRAY)],
            -98 : ["o",ButtonVisualObject("visuals",(134,0),FRAME_OPTIONS_BUTTON_OFF_ARRAY,FRAME_OPTIONS_BUTTON_ON_ARRAY)],
            -97 : ["o",ButtonVisualObject("project",(261,0),FRAME_OPTIONS_BUTTON_OFF_ARRAY,FRAME_OPTIONS_BUTTON_ON_ARRAY)],
            -96 : ["o",IconVisualObject("Settings",(323,65), GEAR_ARRAY, (52,52))],

            -89 : ["es", IconVisualObject(   "New Sprite", (338, 15), PLUS_SIGN_ARRAY, (29,29))],
            -88 : ["es", IconVisualObject("Delete Sprite", (338, 65),  TRASHCAN_ARRAY, (29,29))],
            -87 : ["ev", IconVisualObject( "Import Image", (338,161),    IMPORT_ARRAY, (29,29))],
            -86 : ["ev", EditableTextBoxVisualObject("sprite name", (80,41), "Sprite Name")],
            -85 : ["ep", IconVisualObject("Export GIF", ( 7,457), RENDER_GIF_ICON_ARRAY, (37,37))],
            -84 : ["ep", IconVisualObject("Export MP4", (57,457), RENDER_MP4_ICON_ARRAY, (37,37))],
            -83 : ["ep", EditableTextBoxVisualObject("project name", (72,52), DEFAULT_PROJECT_NAME)],

            -72 : ["t", ButtonVisualObject("Play/Pause", (0,0), generateIcon(PLAY_BUTTON_ARRAY, False, (37,37)), generateIcon(PAUSE_BUTTON_ARRAY, False, (37,37)))],
            -71 : ["t", IconVisualObject("Save Project", (0,40),   SAVE_ICON_ARRAY, (37,37))],
            -70 : ["t", IconVisualObject("Load Project", (0,80),   LOAD_ICON_ARRAY, (37,37))]
        }
        #for i in range(10): self.interactableVisualObjects[self.c.c()] = ["a", OrbVisualObject(f"test{i}")]
        '''Noninteractable, Adaptive, Visual Objects'''
        self.pathVisualObject = PathVisualObject(self.c.c(), "path")
        '''Sprites'''
        self.sprites = [
            SingleSprite("Sprite"),
        ]
        self.selectedSprite = 0
        self.selectedProperty = 1
        self.previousSelectedProperty = self.selectedProperty
        self.interacting = -999
        self.editorTab = "p"
        self.previousEditorTab = self.editorTab
        self.stringKeyQueue = ""
        self.previousKeyQueue = []
        self.animationTime = 0
        self.lastAnimationUpdateData = []
        self.lastAnimationTimeline = self.animationTime - 1
        self.animationPlaying = False
        self.mouseScroll = 0 
        self.keybindLastUpdate = time.time()
        self.blankProcessingLayerSector = generateColorBox((129,169), (0,0,0,0))
        self.updateAnimationRegions = []
        self.previousPath = []
        self.animationPathOverlay = None
        self.timelineFancyBar = None
        self.keybindRegen = False
        self.connectionEdit = ""
        self.requestSelectedProperty = self.selectedProperty
        '''Timelines'''
        self.graphScale = 1.0
        self.graphOffset = 0
        self.timelineScale = 1.0
        self.timelineOffset = 0
        self.spriteListOffset = 0
        self.spriteListVelocity = 0
        self.apperancePanelOffset = 0
        '''Project'''
        self.projectUUID = str(uuid.uuid4())
        self.projectName = DEFAULT_PROJECT_NAME
        self.projectCreatedOn = round(time.time())
        self.projectLastSaved = round(time.time())
        self.projectVersionCreated = VERSION
        self.projectPath = os.path.join("tapes", "temp.tape")
        self.projectStartTime = round(time.time())
        pass

    def tick(self,mx,my,mPressed,fps,keyQueue,mouseScroll):
        '''Entire Screen: `(0,0) to (1365,697)`: size `(1366,698)`'''
        self.mx = mx if (0<=mx and mx<=1365) and (0<=my and my<=697) else self.mx 
        self.my = my if (0<=mx and mx<=1365) and (0<=my and my<=697) else self.my
        self.keyQueue = keyQueue
        self.mPressed = mPressed > 0
        self.mRising = mPressed==2
        self.fps = fps
        self.deltaTicks = 1 if self.fps==0 else round(RENDER_FPS/self.fps)
        self.ticks += self.deltaTicks

        self.mouseInAnimationSection =  23 < self.mx and self.mx <  925 and  36 < self.my and self.my < 542
        self.mouseInTimelineSection  =  23 < self.mx and self.mx <  925 and 558 < self.my and self.my < 680
        self.mouseInEditorSection    = 953 < self.mx and self.mx < 1340 and  36 < self.my and self.my < 542
        self.mouseInOptionsSection   = 953 < self.mx and self.mx < 1340 and 558 < self.my and self.my < 680

        if self.interacting == -89 and mPressed < 3: 
            self.sprites.append(SingleSprite(f"New Sprite {len(self.sprites)}"))
        if self.interacting == -88 and mPressed < 3 and len(self.sprites) > 1: 
            self.sprites.pop(self.selectedSprite)
            self.selectedSprite = max(0, min(self.selectedProperty, len(self.sprites)-1))
        if self.interacting == -87 and mPressed < 3 or (self.editorTab == "v" and 1152<self.mx and 36<self.my and self.mx<1340 and self.my<245 and self.interacting == -999 and KB_CREATE(self.keyQueue) and (time.time() - self.keybindLastUpdate > KEYBIND_DIFFERENCE)): 
            if (time.time() - self.keybindLastUpdate > KEYBIND_DIFFERENCE):
                self.keybindLastUpdate = time.time()
            path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
            try: 
                self.sprites[self.selectedSprite].addImageUUID(self.cache.importImage(path))
            except:
                pass
        if self.interacting == -72 and mPressed < 3: 
            self.animationPlaying = not(self.animationPlaying)
        if self.animationPlaying:
            self.animationTime += self.deltaTicks/RENDER_FPS
        if self.interacting == -71 and mPressed < 3: 
            self.exportProject(EXPORT_IMAGE_DATA)
        if self.interacting == -70 and mPressed < 3: 
            self.importProject(CLEAR_ON_OPEN)
        if self.interacting == -85 and mPressed < 3: 
            self.renderGIF()
        if self.interacting == -84 and mPressed < 3: 
            self.renderMP4()
        if self.interacting == -96 and mPressed < 3: 
            os.startfile(os.path.join("settings.py"))

        '''Keyboard'''
        for key in keyQueue: 
            if not key in self.previousKeyQueue:
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
        self.previousKeyQueue = self.keyQueue.copy()
        if self.interacting == -999 and (time.time() - self.keybindLastUpdate > KEYBIND_DIFFERENCE):
            if self.editorTab == "s":
                '''SPRITES EDITOR TAB'''
                if KB_S_LIST_OFFSET_UP(self.keyQueue):
                    '''SCROLL UP IN SPRITE LIST'''
                    self.keybindLastUpdate = time.time()
                    self.spriteListVelocity -= 25
                if KB_S_LIST_OFFSET_DOWN(self.keyQueue):
                    '''SCROLL DOWN IN SPRITE LIST'''
                    self.keybindLastUpdate = time.time()
                    self.spriteListVelocity += 25
                if KB_EV_OFFSET_LEFT(self.keyQueue):  
                    '''MOVE SPRITE UP IN LIST'''
                    self.keybindLastUpdate = time.time()
                    if 1 <= self.selectedSprite and self.selectedSprite <= len(self.sprites)-1:
                        temp = self.sprites[self.selectedSprite]
                        self.sprites.pop(self.selectedSprite)
                        self.selectedSprite -= 1
                        self.sprites.insert(self.selectedSprite, temp)
                if KB_EV_OFFSET_RIGHT(self.keyQueue): 
                    '''MOVE SPRITE DOWN IN LIST'''
                    self.keybindLastUpdate = time.time()
                    if 0 <= self.selectedSprite and self.selectedSprite <= len(self.sprites)-2:
                        temp = self.sprites[self.selectedSprite]
                        self.sprites.pop(self.selectedSprite)
                        self.selectedSprite += 1
                        self.sprites.insert(self.selectedSprite, temp)
                if KB_CREATE(self.keyQueue): 
                    '''CREATE SPRITE'''
                    self.keybindLastUpdate = time.time()
                    if 953<self.mx and 36<self.my and self.mx<1340 and self.my<542:
                        target = math.floor(((self.my-36)+self.spriteListOffset-25)/30)
                        self.sprites.insert(max(0, min(target, len(self.sprites))), SingleSprite(f"Sprite {len(self.sprites)}"))
                    else:
                        self.sprites.insert(len(self.sprites), SingleSprite(f"Sprite {len(self.sprites)}"))
                if KB_DELETE(self.keyQueue):
                    '''DELETE SPRITE'''
                    self.keybindLastUpdate = time.time()
                    if len(self.sprites) > 1:
                        self.sprites.pop(self.selectedSprite)
                self.selectedSprite = max(0,min(self.selectedSprite, len(self.sprites)-1))
            if self.editorTab == "v":
                '''VISUAL EDITOR TAB'''
                if KB_EV_OFFSET_LEFT(self.keyQueue):
                    '''MOVE GRAPH TIMELINE LEFT'''
                    self.graphOffset -= (self.graphScale+0.000001)
                if KB_EV_OFFSET_RIGHT(self.keyQueue):
                    '''MOVE GRAPH TIMELINE RIGHT'''
                    self.graphOffset += (self.graphScale+0.000001)
                if 1152<self.mx and 36<self.my and self.mx<1340 and self.my<245:
                    if KB_DELETE(self.keyQueue):
                        '''DELETE IMAGE'''
                        self.keybindLastUpdate = time.time()
                        self.sprites[self.selectedSprite].removeImageUUID(math.floor(((self.mx-1152)+2*(self.my-36)-2*self.apperancePanelOffset-6)/90))
            if KB_T_OFFSET_LEFT(self.keyQueue):
                '''MOVE TIMELINE LEFT'''
                self.timelineOffset -= (self.timelineScale+0.000001)
            if KB_T_OFFSET_RIGHT(self.keyQueue):
                '''MOVE TIMELINE RIGHT'''
                self.timelineOffset += (self.timelineScale+0.000001)
        else:
            if self.selectedProperty == 1 and self.editorTab == "v":
                if self.interactableVisualObjects[self.interacting][1].type == "point":
                    if KB_A_POINT_POSITION_EDIT(self.keyQueue):
                        '''MOVE SELECTED POINT POINT TO MOUSE POSITION'''
                        self.interactableVisualObjects[self.interacting][1].setPointData((self.mx-23, self.my-36))

        self.requestSelectedProperty = self.selectedProperty
        if self.previousEditorTab == "v" and self.editorTab == "v" and self.selectedSprite != -999:
            data = self.sprites[self.selectedSprite].getData("crashtbw"[self.selectedProperty-1])
            dataCheck("crashtbw"[self.selectedProperty-1], data)
            lenData = round(len(data)/3)

            for i in range(1,8+1):
                if str(i) in self.keyQueue and len(self.keyQueue) == 1: 
                    self.requestSelectedProperty = i
                    self.interacting = -999
            self.connectionEdit = ""
            if (time.time() - self.keybindLastUpdate > KEYBIND_DIFFERENCE):
                if KB_EV_LINEAR_CONNECTION(self.keyQueue): 
                    '''CHANGE CONNECTION TO LINEAR'''
                    self.keybindLastUpdate = time.time()
                    self.connectionEdit = "L"
                if KB_EV_SMOOTH_CONNECTION(self.keyQueue): 
                    '''CHANGE CONNECTION TO SMOOTH'''
                    self.keybindLastUpdate = time.time()
                    self.connectionEdit = "S"
                if 953<self.mx and 255<self.my and self.mx<1340 and self.my<542:
                    if KB_CREATE(self.keyQueue):
                        '''CREATE POINT'''
                        self.keybindLastUpdate = time.time()
                        if self.interacting == -999:
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
                            self.interacting = -999
                            self.keybindRegen = True
                    if KB_DELETE(self.keyQueue):
                        '''DELETE POINT'''
                        self.keybindLastUpdate = time.time()
                        if self.interacting != -999:
                            if self.interactableVisualObjects[self.interacting][1].type == "point":
                                index = listEVGPoints(self.interactableVisualObjects).index(self.interacting)
                                for i in range(3): data.pop(index*3)
                                self.sprites[self.selectedSprite].setData("crashtbw"[self.selectedProperty-1], data)
                                self.interacting = -999
                                self.keybindRegen = True

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
        if self.editorTab == "v" and 1152<self.mx and 36<self.my and self.mx<1340 and self.my<245 and self.interacting == -999:
            if abs(self.mouseScroll) > 0:
                self.apperancePanelOffset -= self.mouseScroll/10
                self.apperancePanelOffset = max(0, min(self.apperancePanelOffset, (math.ceil(len(self.sprites[self.selectedSprite].imageUUIDs)/2)-1)*90))
        if self.editorTab == "s":
            if abs(self.mouseScroll) > 0:
                self.spriteListVelocity = 0
                self.spriteListOffset += self.mouseScroll / 5
            self.spriteListVelocity = self.spriteListVelocity * 0.9
            self.spriteListOffset += self.spriteListVelocity
            if self.spriteListOffset > len(self.sprites)*35-507:
                self.spriteListOffset = len(self.sprites)*35-507
                self.spriteListVelocity = 0
            if self.spriteListOffset < 0: 
                self.spriteListOffset = 0
                self.spriteListVelocity = 0
            self.spriteListOffset = round(self.spriteListOffset)
        else:
            self.spriteListVelocity = 0

        pass

        '''Interacting With...'''
        self.previousInteracting = self.interacting
        if not(self.mPressed):
            self.interacting = -999
        if self.interacting == -999 and self.mPressed and self.mRising:
            for id in self.interactableVisualObjects:
                if self.interactableVisualObjects[id][0] == "a":
                    if self.interactableVisualObjects[id][1].getInteractable(self.mx - 23, self.my - 36):
                        self.interacting = id
                        break
                if self.interactableVisualObjects[id][0] == "es" and self.editorTab == "s":
                    if self.interactableVisualObjects[id][1].getInteractable(self.mx - 953, self.my - 36):
                        self.interacting = id
                        break
                if self.interactableVisualObjects[id][0] == "ev" and self.editorTab == "v":
                    if self.interactableVisualObjects[id][1].getInteractable(self.mx - 953, self.my - 36):
                        self.interacting = id
                        break
                if self.interactableVisualObjects[id][0] == "ep" and self.editorTab == "p":
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
                if self.interactableVisualObjects[id][0] == "t":
                    if self.interactableVisualObjects[id][1].getInteractable(self.mx - 23, self.my - 558):
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
                self.interactableVisualObjects[self.interacting][1].keepInFrame(0,0,903,507)
            if section == "es" or section == "ep": 
                self.interactableVisualObjects[self.interacting][1].updatePos(self.mx - 953, self.my - 36)
                self.interactableVisualObjects[self.interacting][1].keepInFrame(0,0,388,507)
            if section == "evg": 
                self.interactableVisualObjects[self.interacting][1].updatePos(self.mx - 982, self.my - 278)
                self.interactableVisualObjects[self.interacting][1].keepInFrame(0,0,337,233)
            if section == "t": 
                self.interactableVisualObjects[self.interacting][1].updatePos(self.mx - 23, self.my - 558)
                self.interactableVisualObjects[self.interacting][1].keepInFrame(0,0,903,123)
            if section == "o": 
                self.interactableVisualObjects[self.interacting][1].updatePos(self.mx - 953, self.my - 558)
                self.interactableVisualObjects[self.interacting][1].keepInFrame(0,0,388,123)
        if ((self.mPressed)) and (self.previousInteracting == -999) and (self.interacting != -999) and (self.interactableVisualObjects[self.interacting][1].type  == "textbox"): 
            self.stringKeyQueue = self.interactableVisualObjects[self.interacting][1].txt
        if (self.interacting != -999) and (self.interactableVisualObjects[self.interacting][1].type  == "textbox"):
            self.interactableVisualObjects[self.interacting][1].updateText(self.stringKeyQueue)
        if (self.previousInteracting != -999) and (self.previousInteracting != -998):
            if (self.interactableVisualObjects[self.previousInteracting][1].type  == "textbox"):
                if not(self.interacting == -998):
                    self.interacting = self.previousInteracting
                    self.interactableVisualObjects[self.interacting][1].updateText(self.stringKeyQueue)
                else:
                    self.interactableVisualObjects[self.previousInteracting][1].updateText(self.stringKeyQueue)
            
            if (self.selectedProperty == 1) and (self.interactableVisualObjects[self.previousInteracting][1].type  == "point"):
                if not(self.interacting == -998):
                    self.interacting = self.previousInteracting

        if self.editorTab == "s" and self.interacting == -999:
            if 953<self.mx and 36<self.my and self.mx<1340 and self.my<542:
                if self.mPressed and mPressed < 3:
                    target = math.floor(((self.my-36)+self.spriteListOffset-25)/30)
                    if 0 <= target and target <= len(self.sprites)-1:
                        self.selectedSprite = target

    def getDoesNeedGetImageAnimation(self):
        '''Returns if the window should run `getImageAnimation()`'''
        if self.ticks < 3:
            return True
        if self.interacting != -999 and self.interactableVisualObjects[self.interacting][1].type == "point" and self.selectedProperty == 1:
            return True
        if (self.previousInteracting != -999 and self.interactableVisualObjects[self.previousInteracting][1].type == "point" and self.selectedProperty == 1) or self.previousSelectedProperty == 1:
            return True
        return False

    def getImageAnimation(self, im):
        '''Animation Interface: `(23,36) to (925,542)`: size `(903,507)`'''
        rmx = self.mx - 23
        rmy = self.my - 36
        img = im.copy()

        # placeOver(img, displayText(f"FPS: {self.fps}", "m"), (55,15))
        # placeOver(img, displayText(f"Relative (animation) Mouse Position: ({self.mx-23}, {self.my-36})", "m"), (455,55))
        # placeOver(img, displayText(f"Mouse Pressed: {self.mPressed}", "m", colorTXT = (0,255,0,255) if self.mPressed else (255,0,0,255)), (55,55))
        # placeOver(img, displayText(f"Rising Edge: {self.mRising}", "m", colorTXT = (0,255,0,255) if self.mRising else (255,0,0,255)), (55,95))
        # placeOver(img, displayText(f"Interacting With Element: {self.interacting}", "m"), (455,15))
        # placeOver(img, displayText(f"stringKeyQueue: {self.stringKeyQueue}", "m"), (455,95))


        if self.interacting != -999 and self.interactableVisualObjects[self.interacting][1].type == "point" and self.selectedProperty == 1:
            data = self.sprites[self.selectedSprite].getData("crashtbw"[self.selectedProperty-1])
            previousPath = self.previousPath.copy()
            coords = iterateThroughPath(data)
            self.previousPath = coords
            if previousPath != self.previousPath: self.scheduleAllRegions()
            for coord in coords:
                placeOver(img, PATH_POINT_IDLE_ARRAY, coord, True)
            evgP = listEVGPoints(self.interactableVisualObjects)
            extent = findExtentThroughPath(data, evgP.index(self.interacting))
            if extent[-1] > len(evgP)-1:
                extent = extent[0:-2]
            for id in [evgP[index] for index in extent]:
                placeOver(img, ORB_SELECTED_ARRAY if id==self.interacting else ORB_IDLE_ARRAY, self.interactableVisualObjects[id][1].pointData, True)

        if self.interacting == -999 and self.previousInteracting != -999 and self.interactableVisualObjects[self.previousInteracting][1].type == "point" and self.selectedProperty == 1:
            self.scheduleAllRegions()
        if self.previousSelectedProperty == 1 and self.selectedProperty != 1:
            self.scheduleAllRegions()
        
        for id in self.interactableVisualObjects:
            if self.interactableVisualObjects[id][0] == "a":
                self.interactableVisualObjects[id][1].tick(img, self.interacting==id)

        self.animationPathOverlay = img

    def getImageAnimationToProcess(self):
        for sprite in self.sprites:
            getUpdated = sprite.getUpdated(self.animationTime)
            if getUpdated[0]:
                for data in [getUpdated, [self.animationTime, ""]]:
                    pos = sprite.getStateAt("p",data[0], data[1])
                    size = self.cache.getImage(sprite.imageUUIDs[sprite.getStateAt("a", data[0], data[1])]).shape[:2]
                    scalar = sprite.getStateAt("s", data[0], data[1])
                    size = (max(1, (round(size[0]*(scalar/50)**2))),max(1, round(size[1]*(scalar/50)**2)))
                    rot = sprite.getStateAt("r", data[0], data[1])
                    a = ROTATE_AROUND_ORIGIN( size[0]/2,  size[1]/2, rot)
                    b = ROTATE_AROUND_ORIGIN(-size[0]/2,  size[1]/2, rot)
                    c = ROTATE_AROUND_ORIGIN( size[0]/2, -size[1]/2, rot)
                    d = ROTATE_AROUND_ORIGIN(-size[0]/2, -size[1]/2, rot)
                    self.scheduleRegionGivenArea(min(a[0], b[0], c[0], d[0]) + pos[0], min(a[1], b[1], c[1], d[1]) + pos[1], max(a[0], b[0], c[0], d[0]) + pos[0], max(a[1], b[1], c[1], d[1]) + pos[1])
    
    def getFetchAnimationSector(self, x, y):
        '''129x169'''
        img = self.blankProcessingLayerSector.copy()
        if DEBUG_BACKGROUND:
            if time.time() % 0.2 <= 0.1:
                img = generateColorBox((129,169),(155,0,0,255))
            else:
                img = generateColorBox((129,169),(0,155,0,255))

        for sprite in self.sprites:
            frame = sprite.getFullStateAt(self.animationTime)
            placeOver(img, readImgSingleFullState(frame, self.cache.getImage(sprite.imageUUIDs[frame[1]]), True), (frame[0][0]-x*129,frame[0][1]-y*169), True)

        placeOver(img, getRegion(self.animationPathOverlay, (x*129, y*169), ((x+1)*129, (y+1)*169), 1), (0,0))

        return img

    def getImageTimeline(self, im):
        '''Timeline Interface: `(23,558) to (925,680)`: size `(903,123)`'''
        if (self.interacting != -999 or self.interacting != -999) or self.ticks < 3 or self.animationTime != self.lastAnimationTimeline or self.animationPlaying or self.interactableVisualObjects[self.interacting][0] == "t" or self.interactableVisualObjects[self.previousInteracting][0] == "t":
            self.lastAnimationTimeline = self.animationTime
            img = im.copy()
            placeOver(img, self.timelineFancyBar, (0,0))

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

            '''Timeline Bar'''
            pos = (self.animationTime-self.timelineOffset)*25/(self.timelineScale+0.000001) + 47
            if 46 < pos and pos < 896:
                placeOver(img, FRAME_TIMELINE_READER_ARRAY, (max(51,pos), 3))

            for id in self.interactableVisualObjects:
                if self.interactableVisualObjects[id][0] == "t":
                    if id == -72:
                        self.interactableVisualObjects[id][1].tick(img, self.animationPlaying)
                    else:
                        self.interactableVisualObjects[id][1].tick(img, self.interacting==id)

            return img
    
    def getImageFancyTimeline(self, im):
        '''Fancy Sprite Timelines'''
        if (self.interacting != -999 or self.interacting != -999) or self.ticks < 3:
            img = im.copy()
            barHeight = max(2, min(round(95/len(self.sprites))-2,10))
            yOffset = 25
            i=0
            for i in range(len(self.sprites)):
                lowest = 999
                farthest = 0
                for prop in ["c","r","a","s","t","b","w"]:
                    data = self.sprites[i].getData(prop)
                    for ie in range(round(len(data)/3)):
                        if data[ie*3] < lowest: lowest = data[ie*3]
                        if data[ie*3] > farthest: farthest = data[ie*3]
                lowest=(lowest-self.timelineOffset)*25/(self.timelineScale+0.000001) + 47
                farthest=(farthest-self.timelineOffset)*25/(self.timelineScale+0.000001) + 47
                lowest=max(50,min(round(lowest), 922))
                farthest=max(50,min(round(farthest), 922))
                if i==self.selectedSprite: placeOver(img, generateColorBox((922,barHeight), hexColorToRGBA(FRAME_COLOR)), (50, yOffset))
                placeOver(img, generateColorBox((farthest-lowest, barHeight), translatePastelLight(self.sprites[i].getColor()) if i==self.selectedSprite else self.sprites[i].getColor()), (lowest, yOffset))
                yOffset += barHeight+2
                if yOffset > 119: break
            
            self.timelineFancyBar = img


    def getImageEditor(self, im):
        '''Editor Interface: `(953,36) to (1340,542)`: size `(388,507)`'''
        img = im.copy()
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
                frame = self.sprites[self.selectedSprite].getFullStateAt(self.animationTime)
                placeOver(img, setLimitedSize(readImgSingleFullState(frame, self.cache.getImage(self.sprites[self.selectedSprite].getImageUUIDAt(self.animationTime)), True), 50), (15,25))

                startI = round(self.graphOffset/(10**math.floor(math.log(self.graphScale+0.000001,10)+1)))
                for i in range(startI - 3, startI + 33):
                    pos = 29 + ((i*(10**math.floor(math.log(self.graphScale+0.000001,10)+1)))-self.graphOffset)*(1/(self.graphScale+0.000001))*25
                    if pos > 362: break
                    if pos > 29: 
                        placeOver(img, FRAME_EDITOR_VISUALS_GRAPH_BAR_ARRAY, (pos, 242))
                        displayTime = roundf((i*(10**math.floor(math.log(self.graphScale+0.000001,10)+1))),2)
                        if displayTime >= 1:
                            if displayTime < 3600:
                                displayTime = "{:02}:{:02}".format(math.floor(displayTime/60), roundf(displayTime%60,2))
                            else:
                                displayTime = "{:02}:{:02}:{:02}".format(math.floor(displayTime/3600), math.floor((displayTime-3600*math.floor(time/3600))/60), roundf(displayTime%60,2))
                        else:
                            displayTime = str(displayTime)
                        placeOver(img, displayText(displayTime, "s"), (pos,492), True)
                
                '''Get Data and Stuff'''
                data = self.sprites[self.selectedSprite].getData("crashtbw"[self.selectedProperty-1])
                dataCheck("crashtbw"[self.selectedProperty-1], data)
                if self.selectedProperty == 1: 
                    pathP = iterateThroughPath(data, True)
                    pathV = [tcoordVelocity(partition) for partition in pathP]
                else: 
                    pathP = iterateThroughSingle(data, True)
                lenData = round(len(data)/3)

                '''Graph Points and Editing'''
                evgPoints = listEVGPoints(self.interactableVisualObjects)
                evgConnections = listEVGConnections(self.interactableVisualObjects)
                if self.previousEditorTab != "v" or self.selectedProperty != self.previousSelectedProperty:
                    self.interactableVisualObjects[-86][1].updateText(self.sprites[self.selectedSprite].name)
                if self.previousEditorTab != "v" or self.selectedProperty != self.previousSelectedProperty or self.keybindRegen:
                    self.keybindRegen = False
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

                    data = self.sprites[self.selectedSprite].getData("crashtbw"[self.selectedProperty-1])
                    dataCheck("crashtbw"[self.selectedProperty-1], data)

                    dataS = [[data[i*3],data[i*3+1],data[i*3+2]] for i in range(lenData)]
                    dataS.sort(key = lambda x: x[0])
                    data = []
                    for timeState in dataS:
                        for thing in timeState: data.append(thing)
                    self.sprites[self.selectedSprite].setData("crashtbw"[self.selectedProperty-1], data)

                    if self.selectedProperty == 1:
                        pathP = iterateThroughPath(data, True)
                        pathV = [tcoordVelocity(partition) for partition in pathP]
                        for i in range(len(evgConnections)): self.interactableVisualObjects[evgConnections[i]][1].setPathData(pathV[i])
                    else:
                        pathP = iterateThroughSingle(data, True)
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
                    if self.interacting != -999 or self.previousInteracting != -999:
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
                        if self.connectionEdit in ["L", "S"]:
                            data[i*3+2] = self.connectionEdit
                            self.sprites[self.selectedSprite].setData("crashtbw"[self.selectedProperty-1], data)
                            self.connectionEdit = ""

                evgPoints = listEVGPoints(self.interactableVisualObjects)
                evgConnections = listEVGConnections(self.interactableVisualObjects)
                if 1 <= self.selectedProperty and self.selectedProperty <= 8:
                    placeOver(img, displayText(f"({self.selectedProperty}) - {PROPERTY_DISPLAY_NAMES[self.selectedProperty-1]}", "m"), (89,130), True)
                    if self.interacting == -999:
                        placeOver(img, displayText(f"[P: {len(evgPoints)}, C: {len(evgConnections)}, S: {sum([len(p) for p in pathP])}]", "m"), (89,190), True)


                '''Apperance Panel'''
                apperancePanel = generateColorBox((189,210), hexColorToRGBA(BACKGROUND_COLOR))
                placeOver(apperancePanel, generateBorderBox((183,206),3,hexColorToRGBA(FRAME_COLOR)), (0,0))
                resizedImgs = [setLimitedSize(self.cache.getImage(spriteImgUUID), 73) for spriteImgUUID in self.sprites[self.selectedSprite].imageUUIDs]
                for i in range(len(resizedImgs)):
                    # each image is 85x85 (including borders)
                    xPos = math.floor(i/2)*90-self.apperancePanelOffset
                    if -100 < xPos and xPos < 210:
                        y, x, temp = resizedImgs[i].shape
                        imgB = generateColorBox((x+12,y+12),hexColorToRGBA(BACKGROUND_COLOR))
                        placeOver(imgB, generateBorderBox((x, y), 6, hexColorToRGBA(FRAME_COLOR)), (0,0))
                        placeOver(imgB, resizedImgs[i], (6,6))
                        placeOver(imgB, displayText(str(i),"m", hexColorToRGBA(BACKGROUND_COLOR), hexColorToRGBA(SELECTED_COLOR)), (7,7))
                        placeOver(apperancePanel, imgB, (90*(i%2)+6, math.floor(i/2)*90-self.apperancePanelOffset))
                    if xPos > 210: break
                placeOver(img, apperancePanel, (199,0))

                self.selectedProperty = self.requestSelectedProperty
                placeOver(img, FRAME_EDITOR_VISUALS_GRAPH_ARRAY, (0,219))
                # placeOver(img, PLACEHOLDER_IMAGE_5_ARRAY, ((100-self.graphOffset)*25/(self.graphScale+0.000001)+29,219), True)

            for id in self.interactableVisualObjects:
                if self.interactableVisualObjects[id][0] == "evg":
                    if self.interactableVisualObjects[id][1].type == "connection":
                        self.interactableVisualObjects[id][1].tick(img, self.interacting==id, self.graphOffset, self.graphScale)
                if self.interactableVisualObjects[id][0] == "evg":
                    if self.interactableVisualObjects[id][1].type != "connection":
                        self.interactableVisualObjects[id][1].tick(img, self.interacting==id)
                if self.interactableVisualObjects[id][0] == "ev":
                    self.interactableVisualObjects[id][1].tick(img, self.interacting==id)
                    if self.interactableVisualObjects[id][1].name == "sprite name":
                        self.sprites[self.selectedSprite].name = self.interactableVisualObjects[id][1].txt

        if self.editorTab == "p":
            '''About Project Tab!'''
            placeOver(img, displayText("Project:", "m"),                                                            (15,EDITOR_SPACING(1))) 
            placeOver(img, displayText("Name:", "m"),                                                               (20,EDITOR_SPACING(2)))
            try:
                size = os.path.getsize(self.projectPath)
                unitPower = math.floor(math.log(size, 1000))
                unit = ["B", "KB", "MB", "GB", "TB", "PB", "units"][unitPower]
                placeOver(img, displayText(f"Size: {roundf(size/(1000^unitPower),2)} {unit}", "m"),                 (20,EDITOR_SPACING(3)))
            except:
                placeOver(img, displayText(f"Size: 0 B", "m"),                                                      (20,EDITOR_SPACING(3)))

            placeOver(img, displayText("Elements:", "m"),                                                           (15,EDITOR_SPACING(5)))
            placeOver(img, displayText(f"Sprites: {len(self.sprites)}", "m"),                                       (20,EDITOR_SPACING(6))) 
            placeOver(img, displayText("Folders: please implement this", "m"),                                      (20,EDITOR_SPACING(7))) 
            placeOver(img, displayText(f"Total Apperances: {sum(len(s.imageUUIDs) for s in self.sprites)}", "m"),   (20,EDITOR_SPACING(8)))
            temp = round(sum([len(sprite.getData("c")) for sprite in self.sprites])/3)
            placeOver(img, displayText(f"Total Path Elements: {temp*2-1}", "m"),                                    (20,EDITOR_SPACING(9))) 
            placeOver(img, displayText(f"Total Path Waypoints: {temp}", "m"),                                       (20,EDITOR_SPACING(10))) 
            placeOver(img, displayText(f"Interactable Visual Objects: {len(self.interactableVisualObjects)}", "m"), (20,EDITOR_SPACING(11))) 

            placeOver(img, displayText("Dates:", "m"),                                                              (15,EDITOR_SPACING(13)))
            placeOver(img, displayText(f"Created On: {FORMAT_TIME(self.projectCreatedOn)}", "m"),                   (20,EDITOR_SPACING(14)))  
            placeOver(img, displayText(f"Last Saved: {FORMAT_TIME(self.projectLastSaved)}", "m"),                   (20,EDITOR_SPACING(15)))  
            placeOver(img, displayText(f"Version Created: {self.projectVersionCreated}", "m"),                      (20,EDITOR_SPACING(16)))  
            placeOver(img, displayText(f"Current Version: {VERSION}", "m"),                                         (20,EDITOR_SPACING(17))) 
            temp = round(time.time() - self.projectStartTime)
            formated=f"{math.floor(temp%60)}s"
            if temp >= 60: formated=f"{math.floor((temp-3600*math.floor(temp/3600))/60)}m "+formated
            if temp >= 3600: formated=f"{math.floor(temp/3600)}h "+formated
            placeOver(img, displayText(f"Time Spent: {formated}", "m"),                                             (20,EDITOR_SPACING(18))) 

            for id in self.interactableVisualObjects:
                if self.interactableVisualObjects[id][0] == "ep":
                    self.interactableVisualObjects[id][1].tick(img, self.interacting==id or self.interactableVisualObjects[id][1].getInteractable(self.mx - 953, self.my - 36))
                    if self.interactableVisualObjects[id][1].name == "project name":
                        self.projectName = self.interactableVisualObjects[id][1].txt

        return img
    
    def getImageOptions(self, im):
        '''Options Interface: `(953,558) to (1340,680)`: size `(388,123)`'''
        img = im.copy()
        
        self.previousEditorTab = self.editorTab 

        for id in self.interactableVisualObjects:
            if self.interactableVisualObjects[id][0] == "o":
                if self.interacting==id and self.interactableVisualObjects[id][1].name in ["sprites", "visuals", "project"]: self.editorTab = self.interactableVisualObjects[id][1].name[0]
                self.interactableVisualObjects[id][1].tick(img, self.interacting==id or (self.editorTab==self.interactableVisualObjects[id][1].name[0] and self.interactableVisualObjects[id][1].name in ["sprites", "visuals", "project"]))

        if self.mouseInAnimationSection:
            placeOver(img, displayText(f"rx: {self.mx-23}", "m"), (20,73)) 
            placeOver(img, displayText(f"ry: {self.my-36}", "m"), (80,73))
        else:            
            placeOver(img, displayText(f"x: {self.mx}", "m", colorTXT=(155,155,155,255)), (20,73)) 
            placeOver(img, displayText(f"y: {self.my}", "m", colorTXT=(155,155,155,255)), (80,73))
        placeOver(img, displayText(f"FPS: {self.fps}", "m", colorTXT=(155,155,155,255)), (20,95))
        placeOver(img, displayText(f"Interacting: {self.interacting}", "m", colorTXT= (225,225,225,255) if self.mPressed else (155,155,155,255)), (80,95))
        placeOver(img, displayText("Sprites                  Visuals                  Project", "m"), (193, 31), True)
        return img

    def importProject(self, clear = True):
        '''Import stuffs'''
        path = filedialog.askopenfilename(initialdir=PATH_SAVE_DEFAULT, defaultextension=".tape", filetypes=[("Tape", "*.tape"), ("All files", "*.*")])
        if path != "":
            self.projectPath = path
            with open(path, "r") as f:
                file = f.read()
                project = ast.literal_eval(file)
                f.close()
            #project data
            if clear:
                self.sprites = []
            projectData = project[0]
            self.projectName = projectData["project name"]
            self.interactableVisualObjects[-83][1].updateText(self.projectName)
            self.projectUUID = projectData["UUID"]
            try:
                self.projectCreatedOn = projectData["created on"]
                self.projectLastSaved = projectData["last saved"]
                self.projectStartTime = round(time.time() - projectData["time spent"])
            except: 
                self.projectCreatedOn = round(time.time())
                self.projectLastSaved = round(time.time())
                self.projectStartTime = round(time.time())
            #sprite data
            spriteData = project[1]
            for uuid in list(spriteData.keys()):
                temp = SingleSprite("Imported Sprite")
                temp.fullDataImport(spriteData[uuid])
                self.sprites.append(temp)
            #image data
            if len(spriteData) == 2:
                pass
            else: 
                #contains image data
                imageData = project[2]
                for uuid in list(imageData.keys()):
                    try: self.cache.importIDRawImage(uuid, imageData[uuid][0], imageData[uuid][1])
                    except: pass
            #reset
            self.selectedSprite = 0
            self.selectedProperty = 1
            self.previousSelectedProperty = self.selectedProperty
            self.graphScale = 1.0
            self.graphOffset = 0
            self.timelineScale = 1.0
            self.timelineOffset = 0
            self.spriteListOffset = 0
            self.interacting = -999
            self.editorTab = "p"
            self.previousEditorTab = self.editorTab
            self.animationTime = 0
            self.animationPlaying = False
            
    def exportProject(self, saveImageData = True):
        '''Export stuffs'''
        path = filedialog.asksaveasfilename(initialdir=PATH_SAVE_DEFAULT, defaultextension=".tape", filetypes=[("Tape", "*.tape"), ("All files", "*.*")])
        if path != "":
            self.projectPath = path
            self.projectLastSaved = round(time.time())
            export = []
            #project data
            projectData = {
                "project name": self.projectName,
                "version" : VERSION,
                "UUID" : self.projectUUID,
                "created on": self.projectCreatedOn,
                "version created": self.projectVersionCreated,
                "last saved": round(time.time()),
                "time spent": round(time.time() - self.projectStartTime)
            }
            export.append(projectData)
            #sprite data
            spriteData = {}
            for sprite in self.sprites: spriteData[sprite.uuid] = sprite.data
            export.append(spriteData)
            #image data
            if saveImageData:
                imageData = {}
                uuidToGather = []
                for sprite in self.sprites:
                    for uuid in sprite.imageUUIDs:
                        uuidToGather.append(uuid)
                for uuid in uuidToGather:
                    imageData[uuid] = [self.cache.getPath(uuid), self.cache.getImageRaw(uuid)]
                export.append(imageData)
            #write to file
            with open(path, "w") as f:
                f.write(str(export))
                f.close()

    def renderGIF(self):
        path = filedialog.asksaveasfilename(initialdir=PATH_SAVE_DEFAULT, defaultextension=".gif", filetypes=[("GIF", "*.gif")])
        if path != "":
            farthest = 0
            for sprite in self.sprites:
                for prop in ["c","r","a","s","t","b","w"]:
                    data = sprite.getData(prop)
                    for i in range(round(len(data)/3)):
                        if data[i*3] > farthest: farthest = data[i*3]
            bg = generateColorBox((903,507), (0,0,0,255))
            images = []
            for i in range(math.ceil(farthest * RENDER_FPS)):
                img = bg.copy()
                for sprite in self.sprites:
                    frame = sprite.getFullStateAt(i/RENDER_FPS)
                    placeOver(img, readImgSingleFullState(frame, self.cache.getImage(sprite.imageUUIDs[frame[1]]), True), (frame[0][0],frame[0][1]), True)
                images.append(Image.fromarray(img))  
            images[0].save(path, format='gif', append_images=images[1:], save_all=True, duration=1000/RENDER_FPS, loop=0)
        
    def renderMP4(self):
        path = filedialog.asksaveasfilename(initialdir=PATH_SAVE_DEFAULT, defaultextension=".mp4", filetypes=[("MP4", "*.mp4")])
        if path != "":
            farthest = 0
            for sprite in self.sprites:
                for prop in ["c","r","a","s","t","b","w"]:
                    data = sprite.getData(prop)
                    for i in range(round(len(data)/3)):
                        if data[i*3] > farthest: farthest = data[i*3]
            bg = generateColorBox((903,507), (0,0,0,255))
            y, x = bg.shape[:2]
            video = cv2.VideoWriter(path, cv2.VideoWriter_fourcc(*'mp4v'), RENDER_FPS, (x, y))
            for i in range(math.ceil(farthest * RENDER_FPS)):
                img = bg.copy()
                for sprite in self.sprites:
                    frame = sprite.getFullStateAt(i/RENDER_FPS)
                    placeOver(img, readImgSingleFullState(frame, self.cache.getImage(sprite.imageUUIDs[frame[1]]), True), (frame[0][0],frame[0][1]), True)
                video.write(cv2.cvtColor(img[:,:,:3], cv2.COLOR_RGB2BGR))
            video.release()    

    def scheduleRegionGivenArea(self, x1, y1, x2, y2):
        cornerA = (max(0, min(math.floor((min(x1, x2))/129), 7-1)), max(0, min(math.floor((min(y1, y2))/169), 3-1)))
        cornerB = (max(0, min(math.ceil ((max(x1, x2))/129), 7-1)), max(0, min(math.ceil ((max(y1, y2))/169), 3-1)))
        for ix in range(cornerB[0]-cornerA[0]+1):
            for iy in range(cornerB[1]-cornerA[1]+1):
                self.scheduleRegion((cornerA[0]+ix, cornerA[1]+iy))

    def scheduleRegionGivenPixel(self, pixel):
        region = (max(0, min(pixel[0] // 129, 7-1)), max(0, min(pixel[1] // 169, 3-1)))
        if region in self.updateAnimationRegions:
            self.updateAnimationRegions.remove(region)
        self.updateAnimationRegions.append(region)

    def scheduleRegion(self, region):
        safeRegion = (max(0, min(region[0], 7-1)), max(0, min(region[1], 3-1)))
        if safeRegion in self.updateAnimationRegions:
            self.updateAnimationRegions.remove(safeRegion)
        self.updateAnimationRegions.append(safeRegion)

    def scheduleAllRegions(self):
        for region in ALL_REGIONS:
            if region not in self.updateAnimationRegions:
                self.updateAnimationRegions.append(region)

    def saveState(self):
        pass

    def close(self):
        pass