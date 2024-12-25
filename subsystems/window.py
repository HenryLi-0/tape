'''This file is just the window that pops up and refreshes itself!'''

from settings import *
import tkinter as tk
from PIL import ImageTk, Image
import time, math
from subsystems.interface import Interface
from subsystems.label import LabelWrapper
from settings import *

class Window:
    def __init__(self):
        '''initalize tk window'''
        self.window = tk.Tk()
        self.window.grid()
        self.window.title("Tape")
        self.window.geometry("1366x698")
        self.window.configure(background=BACKGROUND_COLOR)
        self.fps = 0
        self.fpsTimestamps = []
        self.mPressed = False
        self.keysPressed = []
        self.mouseScroll = 0

        '''load test image'''
        testImage = ImageTk.PhotoImage(PLACEHOLDER_IMAGE)
        self.labels = {}
        self.blankLabels = {}
        for section in SECTIONS:
            self.labels[section] = LabelWrapper(self.window, SECTIONS_DATA[section][2], SECTIONS_DATA[section][0], SECTIONS_DATA[section][0], BACKGROUND_COLOR, SECTIONS_FRAME_INSTRUCTIONS[section])
            self.blankLabels[section] = self.labels[section].getBlank()

        # self.b_animation_full =     generateColorBox(( 903, 507), (0,0,0,0))
        # self.w_animation = {}
        # for region in ALL_REGIONS:
        #     self.w_animation[region] = LabelWrapper(self.window, (129, 169), (region[0]*129+23, region[1]*169+36), (region[0]*129+23, region[1]*169+36), "#000000")
        # self.b_animation = self.w_animation[(0,0)].getBlank()
        # self.w_timeline  = LabelWrapper(self.window, ( 903, 123), (  23, 558), (  23, 558), BACKGROUND_COLOR, FRAME_TIMELINE_INSTRUCTIONS )
        # self.b_timeline  = self.w_timeline  .getBlank()
        # self.w_editor    = LabelWrapper(self.window, ( 388, 507), ( 953,  36), ( 953,  36), BACKGROUND_COLOR, FRAME_EDITOR_INSTRUCTIONS   )
        # self.b_editor    = self.w_editor    .getBlank()
        # self.b_editor_v  = followInstructions(       ( 388, 507),                           BACKGROUND_COLOR, FRAME_EDITOR_V_INSTRUCTIONS )
        # self.w_options   = LabelWrapper(self.window, ( 388, 123), ( 953, 558), ( 953, 558), BACKGROUND_COLOR, FRAME_OPTIONS_INSTRUCTIONS  )
        # self.b_options   = self.w_options   .getBlank()

        '''start interface'''
        self.interface = Interface()

        self.processFunctions = {
            " " : self.interface.processNone,
            "a" : self.interface.processExampleA,
            "b" : self.interface.processExampleB,
        }
        self.processFunctionsRegions = list(self.processFunctions.keys())

    def windowProcesses(self):
        '''window processes'''
        mx = self.window.winfo_pointerx()-self.window.winfo_rootx()
        my = self.window.winfo_pointery()-self.window.winfo_rooty()
        if self.mPressed > 0: self.mPressed += 1
        else: self.mPressed = 0

        '''update screens'''
        self.interface.tick(mx,my,self.mPressed, self.fps, self.keysPressed, self.mouseScroll)
        self.mouseScroll = 0

        if self.fps > INTERFACE_FPS:
            for region in self.processFunctionsRegions:
                if (region != " ") and (self.labels[region].shown):
                    self.labels[region].update(self.processFunctions[region](self.blankLabels[region]))
        else:
            for region in self.interface.s.scheduledSectionUpdate:
                if (region != " ") and (self.labels[region].shown):
                    self.labels[region].update(self.processFunctions[region](self.blankLabels[region]))
            self.interface.s.scheduledSectionUpdate = []

        now = time.time()
        self.fpsTimestamps.append(now)
        while now-self.fpsTimestamps[0] > FPS_DAMPENING:
            self.fpsTimestamps.pop(0)
        self.fps = round(len(self.fpsTimestamps)/FPS_DAMPENING)
        # print(f"FPS: {self.fps}")

        self.window.after(TICK_MS, self.windowProcesses)

    def windowOccasionalProcesses(self):
        '''window processes that happen less frequently (once every 5 seconds)'''
        print("windowOccaionalProcess")
        self.window.title(f"Tape - Editing: {self.interface.s.ticks}")
        print(self.getFPS())

        for region in self.processFunctionsRegions:
                if self.labels[region].shown:
                    self.labels[region].update(self.processFunctions[region](self.blankLabels[region]))

        self.window.after(OCCASIONAL_TICK_MS, self.windowOccasionalProcesses)

    def windowStartupProcesses(self):
        '''window processes that occur once when startup'''
        print("windowStartupProcess")
        pass
    
    def getFPS(self): return self.fps
    def mPress(self, side = 0): self.mPressed = 1
    def mRelease(self, side = 0): self.mPressed = -999
    def mouseWheel(self, event): self.mouseScroll -= event.delta
    def keyPressed(self, key): 
        if (not str(key.keysym) in self.keysPressed) and (not str(key.keysym) in KB_IGNORE):
            self.keysPressed.append(str(key.keysym))
    def keyReleased(self, key):
        if str(key.keysym) in self.keysPressed:
            self.keysPressed.remove(str(key.keysym))
    
    def start(self):
        '''start window main loop'''
        print("windowStart")
        
        self.window.bind("<ButtonPress-1>", self.mPress)
        self.window.bind("<ButtonRelease-1>", self.mRelease)
        self.window.bind("<KeyPress>", self.keyPressed)
        self.window.bind("<KeyRelease>", self.keyReleased)
        self.window.bind_all("<MouseWheel>", self.mouseWheel)

        self.window.after(2, self.windowProcesses)
        self.window.after(2, self.windowOccasionalProcesses)
        self.window.after(1, self.windowStartupProcesses)
        self.window.mainloop()