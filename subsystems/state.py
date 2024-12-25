'''This file is used for transfering information from interface tick and image rendering processes'''

from subsystems.visuals import *
from subsystems.counter import Counter

class State:
    def __init__(self):
        self.mx = 0
        self.my = 0
        self.prevmx = 0
        self.prevmy = 0
        self.mPressed = False
        self.mRising = False
        self.fps = 0
        self.ticks = 0
        self.deltaTicks = 1
        self.activity = ""
        self.c = Counter()
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
        self.ivos = {
            -999 : [" ", DummyVisualObject("dummy", (0,0))], # used for not interacting with anything
            -998 : [" ", DummyVisualObject("dummy", (0,0))], # used for text boxes

            -99 : ["a",ButtonVisualObject("sprites",(7,450),FRAME_OPTIONS_BUTTON_OFF_ARRAY,FRAME_OPTIONS_BUTTON_ON_ARRAY)],
            -98 : ["a",ButtonVisualObject("visuals",(134,450),FRAME_OPTIONS_BUTTON_OFF_ARRAY,FRAME_OPTIONS_BUTTON_ON_ARRAY)],
            -97 : ["b",ButtonVisualObject("project",(7,450),FRAME_OPTIONS_BUTTON_OFF_ARRAY,FRAME_OPTIONS_BUTTON_ON_ARRAY)],
            -96 : ["b",IconVisualObject("Settings",(323,450), GEAR, (52,52))],
        }
        '''Control'''
        self.interacting = -999
        self.previousInteracting = -999
        self.lastInteraction = self.interacting
        self.mouseScroll = 0 
        self.risingKeyQueue = []
        self.previousKeyQueue = []
        self.consoleAlerts = []
        self.keybindLastUpdate = time.time()
        self.currentKeybind = [False, None]
        '''Sliders'''
        self.sliders = []
        self.slidersData = []
        '''Updating'''
        self.scheduledSectionUpdate = []

    def mouseInSection(self, section):
        return SECTIONS_DATA[section][0][0] <= self.mx and self.mx <= SECTIONS_DATA[section][1][0] and SECTIONS_DATA[section][0][1] <= self.my and self.my <= SECTIONS_DATA[section][1][1]
    def mouseWasInSection(self, section):
        return SECTIONS_DATA[section][0][0] <= self.prevmx and self.prevmx <= SECTIONS_DATA[section][1][0] and SECTIONS_DATA[section][0][1] <= self.prevmy and self.prevmy <= SECTIONS_DATA[section][1][1]

    def tick(self,mx,my,mPressed,fps,keyQueue,mouseScroll):
        '''Entire Screen: `(0,0) to (1365,697)`: size `(1366,698)`'''
        self.prevmx = self.mx
        self.prevmy = self.my
        self.mx = mx if (0<=mx and mx<=1365) and (0<=my and my<=697) else self.mx 
        self.my = my if (0<=mx and mx<=1365) and (0<=my and my<=697) else self.my
        self.mPressed = mPressed > 0
        self.mRising = mPressed==2
        self.fps = fps
        self.deltaTicks = 1 if self.fps==0 else round(INTERFACE_FPS/self.fps)
        self.ticks += self.deltaTicks
        
        self.mouseSectionA = self.mouseInSection("a")
        self.mouseSectionB = self.mouseInSection("b")

    def scheduleSectionUpdate(self, section):
        if not(section in self.scheduledSectionUpdate):
            self.scheduledSectionUpdate.append(section)
    
    def keyConversion(key):
        if key in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789":
            return ord(key)
        else:
            if key=="space":    return ord(" ")
            if key=="slash":    return ord("/")
            if key=="asterisk": return ord("*")
            if key=="equal":    return ord("=")
            if key=="at":       return ord("@")
            if key=="minus":    return ord("-")
            if key=="colon":    return ord(":")
            if key=="BackSpace":return -1
        return None