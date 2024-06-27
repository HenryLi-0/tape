'''This file is all about managing what the user sees'''

from settings import *
from PIL import ImageTk, Image
import time, numpy, random, os, math
from subsystems.render import *
from subsystems.fonts import displayText
from subsystems.visuals import OrbVisualObject, PathVisualObject, ButtonVisualObject
from subsystems.counter import Counter

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
            ["a",ButtonVisualObject(self.c.c(), "test", (0,0), RECTANGULAR_RED_BUTTON_ARRAY, RECTANGULAR_GREEN_BUTTON_ARRAY)],

            ["o",ButtonVisualObject(self.c.c(), "Sprites",(7,0),FRAME_OPTIONS_BUTTON_OFF_ARRAY,FRAME_OPTIONS_BUTTON_ON_ARRAY)],
            ["o",ButtonVisualObject(self.c.c(), "Visuals",(134,0),FRAME_OPTIONS_BUTTON_OFF_ARRAY,FRAME_OPTIONS_BUTTON_ON_ARRAY)],
            ["o",ButtonVisualObject(self.c.c(), "Project",(261,0),FRAME_OPTIONS_BUTTON_OFF_ARRAY,FRAME_OPTIONS_BUTTON_ON_ARRAY)]
        
        ]
        # self.interactableVisualObjects = [OrbVisualObject(f"test{i}") for i in range(10)]
        # self.interactableVisualObjects = [ButtonVisualObject(self.c.c(), "test", (0,0), RECTANGULAR_RED_BUTTON_ARRAY, RECTANGULAR_GREEN_BUTTON_ARRAY)]
        '''Noninteractable, Adaptive, Visual Objects'''
        self.pathVisualObject = PathVisualObject(self.c.c(), "path")
        '''Options - Interactable, Stationary, Visual Objects'''
        self.interacting = -999
        pass

    def tick(self,mx,my,mPressed,fps):
        '''Entire Screen: `(0,0) to (1365,697)`: size `(1366,698)`'''
        self.mx = mx if (0<=mx and mx<=1365) and (0<=my and my<=697) else self.mx 
        self.my = my if (0<=mx and mx<=1365) and (0<=my and my<=697) else self.my
        self.mPressed = mPressed > 0
        self.mRising = mPressed==2
        self.fps = fps
        self.ticks += 1
        pass

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
        print(f"{type(self.interacting)} - {self.interacting}")

        if self.interacting != -999:
            section = self.globalInteractableVisualObjects[self.interacting][0]
            if section == "a": self.globalInteractableVisualObjects[self.interacting][1].updatePos(self.mx - 23, self.my - 36)
            if section == "o": self.globalInteractableVisualObjects[self.interacting][1].updatePos(self.mx - 953, self.my - 558)

        

    def getImageAnimation(self):
        '''Animation Interface: `(23,36) to (925,542)`: size `(903,507)`'''
        rmx = self.mx - 23
        rmy = self.my - 36
        rendered = 0
        img = FRAME_ANIMATION_ARRAY.copy()
        placeOver(img, displayText(f"FPS: {self.fps}", "m"), (50,350))
        placeOver(img, displayText(f"Mouse Position: ({rmx}, {rmy})", "m"), (50,200))
        placeOver(img, displayText(f"Mouse Pressed: {self.mPressed}", "m", colorTXT = (0,255,0,255) if self.mPressed else (255,0,0,255)), (50,250))
        placeOver(img, displayText(f"Rising Edge: {self.mRising}", "m", colorTXT = (0,255,0,255) if self.mRising else (255,0,0,255)), (50,300))
        placeOver(img, displayText(f"Interacting With Element: {self.interacting}", "m"), (50,400))
        
        for item in self.globalInteractableVisualObjects:
            if item[0] == "a":
                item[1].tick(img, self.interacting==item[1].id)

        # self.pathVisualObject.tick(img, [item[1].positionO.getPosition() for item in self.globalInteractableVisualObjects])

        print(self.interacting)
        return arrayToImage(img)
    
    def getImageTimeline(self):
        '''Timeline Interface: `(23,558) to (925,680)`: size `(903,123)`'''
        return arrayToImage(FRAME_TIMELINE_ARRAY)
    
    def getImageEditor(self):
        '''Editor Interface: `(953,36) to (1340,542)`: size `(388,507)`'''
        return arrayToImage(FRAME_EDITOR_ARRAY)
    
    def getImageOptions(self):
        '''Options Interface: `(953,558) to (1340,680)`: size `(388,123)`'''
        img = FRAME_OPTIONS_ARRAY.copy()

        for item in self.globalInteractableVisualObjects:
            if item[0] == "o":
                item[1].tick(img, self.interacting==item[1].id)
            
        placeOver(img, displayText(f"Mouse Position: ({self.mx}, {self.my})", "m"), (16,74))        
        return arrayToImage(img)
    
    def saveState(self):
        pass

    def close(self):
        pass