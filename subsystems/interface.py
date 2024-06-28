'''This file is all about managing what the user sees'''

from settings import *
from PIL import ImageTk, Image
import time, numpy, random, os, math
from subsystems.render import *
from subsystems.fancy import displayText, generateColorBox, generateBorderBox
from subsystems.visuals import OrbVisualObject, PathVisualObject, ButtonVisualObject, EditableTextBoxVisualObject, DummyVisualObject
from subsystems.counter import Counter
from subsystems.pathing import pointAt

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
        '''Interactable Visual Objects'''
        self.globalInteractableVisualObjects = [
            #["a",ButtonVisualObject(self.c.c(), "test", (0,0), RECTANGULAR_RED_BUTTON_ARRAY, RECTANGULAR_GREEN_BUTTON_ARRAY)],

            ["o",ButtonVisualObject(self.c.c(), "sprites",(7,0),FRAME_OPTIONS_BUTTON_OFF_ARRAY,FRAME_OPTIONS_BUTTON_ON_ARRAY)],
            ["o",ButtonVisualObject(self.c.c(), "visuals",(134,0),FRAME_OPTIONS_BUTTON_OFF_ARRAY,FRAME_OPTIONS_BUTTON_ON_ARRAY)],
            ["o",ButtonVisualObject(self.c.c(), "project",(261,0),FRAME_OPTIONS_BUTTON_OFF_ARRAY,FRAME_OPTIONS_BUTTON_ON_ARRAY)],
            ["a",EditableTextBoxVisualObject(self.c.c(), "test text box", (50,50), "in my humble unbiased opinion 1155 is a good team")],
            ["a",EditableTextBoxVisualObject(self.c.c(), "test text box", (150,150), "thanks for the star its really motivating")],
            ["a",EditableTextBoxVisualObject(self.c.c(), "test text box", (250,250), "lorem ipsum")]
        ]
        [self.globalInteractableVisualObjects.append(["a", OrbVisualObject(self.c.c(), f"test{i}")]) for i in range(10)]
        # self.interactableVisualObjects = [ButtonVisualObject(self.c.c(), "test", (0,0), RECTANGULAR_RED_BUTTON_ARRAY, RECTANGULAR_GREEN_BUTTON_ARRAY)]
        '''Noninteractable, Adaptive, Visual Objects'''
        self.pathVisualObject = PathVisualObject(self.c.c(), "path")
        '''Options - Interactable, Stationary, Visual Objects'''
        self.interacting = -999
        self.editorTab = "p"
        self.stringKeyQueue = ""
        pass

    def tick(self,mx,my,mPressed,fps,keyQueue):
        '''Entire Screen: `(0,0) to (1365,697)`: size `(1366,698)`'''
        self.mx = mx if (0<=mx and mx<=1365) and (0<=my and my<=697) else self.mx 
        self.my = my if (0<=mx and mx<=1365) and (0<=my and my<=697) else self.my
        self.mPressed = mPressed > 0
        self.mRising = mPressed==2
        self.fps = fps
        self.ticks += 1
        for key in keyQueue: 
            if key in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789":
                self.stringKeyQueue+=key
            else:
                if key=="space":
                    self.stringKeyQueue+=" "
                if key=="BackSpace":
                    self.stringKeyQueue=self.stringKeyQueue[0:-1]
                if key=="Return":
                    self.interacting = -998
                    break
        pass

        previousInteracting = self.interacting
        if not(self.mPressed):
            self.interacting = -999
        if self.interacting == -999 and self.mPressed:
            for i in range(len(self.globalInteractableVisualObjects)):
                if self.globalInteractableVisualObjects[i][0] == "a":
                    if self.globalInteractableVisualObjects[i][1].getInteractable(self.mx - 23, self.my - 36):
                        self.interacting = self.globalInteractableVisualObjects[i][1].id
                        break
                if self.globalInteractableVisualObjects[i][0] == "o":
                    if self.globalInteractableVisualObjects[i][1].getInteractable(self.mx - 953, self.my - 558):
                        self.interacting = self.globalInteractableVisualObjects[i][1].id
                        break
        if self.interacting != -999:
            section = self.globalInteractableVisualObjects[self.interacting][0]
            if section == "a": self.globalInteractableVisualObjects[self.interacting][1].updatePos(self.mx - 23, self.my - 36)
            if section == "o": self.globalInteractableVisualObjects[self.interacting][1].updatePos(self.mx - 953, self.my - 558)
        if ((self.mPressed)) and (previousInteracting == -999) and (self.interacting != -999) and (self.globalInteractableVisualObjects[self.interacting][1].type  == "textbox"): 
            self.stringKeyQueue = self.globalInteractableVisualObjects[self.interacting][1].txt
        if (self.interacting != -999) and (self.globalInteractableVisualObjects[self.interacting][1].type  == "textbox"):
            self.globalInteractableVisualObjects[self.interacting][1].updateText(self.stringKeyQueue)
        if (previousInteracting != -999) and (previousInteracting != -998) and (self.globalInteractableVisualObjects[previousInteracting][1].type  == "textbox"):
            if not(self.interacting == -998):
                self.interacting = previousInteracting
                self.globalInteractableVisualObjects[self.interacting][1].updateText(self.stringKeyQueue)
            else:
                self.globalInteractableVisualObjects[previousInteracting][1].updateText(self.stringKeyQueue)
        

    def getImageAnimation(self):
        '''Animation Interface: `(23,36) to (925,542)`: size `(903,507)`'''
        rmx = self.mx - 23
        rmy = self.my - 36
        img = FRAME_ANIMATION_ARRAY.copy()
        placeOver(img, displayText(f"FPS: {self.fps}", "m"), (50,350))
        placeOver(img, displayText(f"Mouse Position: ({rmx}, {rmy})", "m"), (50,200))
        placeOver(img, displayText(f"Mouse Pressed: {self.mPressed}", "m", colorTXT = (0,255,0,255) if self.mPressed else (255,0,0,255)), (50,250))
        placeOver(img, displayText(f"Rising Edge: {self.mRising}", "m", colorTXT = (0,255,0,255) if self.mRising else (255,0,0,255)), (50,300))
        placeOver(img, displayText(f"Interacting With Element: {self.interacting}", "m"), (50,400))
        placeOver(img, displayText(f"stringKeyQueue: {self.stringKeyQueue}", "m"), (50,450))
        placeOver(img, generateColorBox((50,100),(255,255,0,255)), (50,50))
        placeOver(img, generateBorderBox((100,260),5,(0,255,0,255)), (100,10))

        tempPoint = self.pathVisualObject.path[self.ticks%len(self.pathVisualObject.path)]
        aSillyCat = rotateDeg(UP_ARROW_ARRAY, tempPoint[2]%360)
        placeOver(img, aSillyCat, (round(tempPoint[0]+(128-aSillyCat.shape[1])/2),round(tempPoint[1]+(128-aSillyCat.shape[0])/2)), False)

        # placeOver(img, displayText(f"Pointing At: {pointAt((350,350),(self.mx, self.my))}", "m"), (200,100))
        # aSillyCat = rotateDeg(UP_ARROW_ARRAY,pointAt((350,350),(self.mx, self.my)))
        # placeOver(img, aSillyCat, (round(350+(128-aSillyCat.shape[1])/2),round(350+(128-aSillyCat.shape[0])/2)))

        for item in self.globalInteractableVisualObjects:
            if item[0] == "a":
                item[1].tick(img, self.interacting==item[1].id)

        tempPath = []
        for item in self.globalInteractableVisualObjects: 
            if item[1].type == "orb": tempPath.append(item[1].positionO.getPosition())
        self.pathVisualObject.tick(img, tempPath)

        return arrayToImage(img)
    
    def getImageTimeline(self):
        '''Timeline Interface: `(23,558) to (925,680)`: size `(903,123)`'''
        return arrayToImage(FRAME_TIMELINE_ARRAY)
    
    def getImageEditor(self):
        '''Editor Interface: `(953,36) to (1340,542)`: size `(388,507)`'''
        img = FRAME_EDITOR_ARRAY.copy()
        if self.editorTab == "p":
            '''About Project Tab!'''
            placeOver(img, displayText("Project:", "m"),                                    (15,EDITOR_SPACING(1))) 
            placeOver(img, displayText("Name: please implement this", "m"),                 (20,EDITOR_SPACING(2)))
            placeOver(img, displayText("Size: 1155 MB (please implement this)", "m"),       (20,EDITOR_SPACING(3)))

            placeOver(img, displayText("Elements:", "m"),                                   (15,EDITOR_SPACING(5)))
            placeOver(img, displayText("Sprites: please implement this", "m"),              (20,EDITOR_SPACING(6))) 
            placeOver(img, displayText("Folders: please implement this", "m"),              (20,EDITOR_SPACING(7))) 
            placeOver(img, displayText("Paths: please implement this", "m"),                (20,EDITOR_SPACING(8))) 
            placeOver(img, displayText("Total Path Elements: please implement this", "m"),  (20,EDITOR_SPACING(9))) 
            placeOver(img, displayText("Total Path Waypoints: please implement this", "m"), (20,EDITOR_SPACING(10))) 

            placeOver(img, displayText("Dates:", "m"),                                      (15,EDITOR_SPACING(12)))
            placeOver(img, displayText("Created On: ", "m"),                                (20,EDITOR_SPACING(13)))  
            placeOver(img, displayText("Last Saved: ", "m"),                                (20,EDITOR_SPACING(14)))  
            placeOver(img, displayText("Version Created: ", "m"),                           (20,EDITOR_SPACING(15)))  
            placeOver(img, displayText("Current Version: ", "m"),                           (20,EDITOR_SPACING(16)))  
            placeOver(img, displayText("Time Spent: ", "m"),                                (20,EDITOR_SPACING(17))) 

        return arrayToImage(img)
    
    def getImageOptions(self):
        '''Options Interface: `(953,558) to (1340,680)`: size `(388,123)`'''
        img = FRAME_OPTIONS_ARRAY.copy()

        for item in self.globalInteractableVisualObjects:
            if item[0] == "o":
                if self.interacting==item[1].id: self.editorTab = item[1].name[0]
                item[1].tick(img, self.interacting==item[1].id or self.editorTab==item[1].name[0])

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