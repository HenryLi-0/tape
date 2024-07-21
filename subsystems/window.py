'''This file is just the window that pops up and refreshes itself!'''

from settings import *
import tkinter as tk
from PIL import ImageTk, Image
import time, math
from subsystems.interface import Interface
from settings import *

class Window:
    def __init__(self):
        '''initalize tk window'''
        self.window= tk.Tk()
        self.window.grid()
        self.window.title("Tape")
        self.window.geometry("1366x698")
        self.window.configure(background=BACKGROUND_COLOR)
        self.fps = 0
        self.fpsCounter = 0
        self.fpsGood = False
        self.mPressed = False
        self.keyQueue = []
        self.mouseScroll = 0

        '''load test image'''
        testImage = ImageTk.PhotoImage(PLACEHOLDER_IMAGE)
        self.w_animation = tk.Label(self.window, image = testImage, highlightthickness=0, bd=0)
        self.w_animation.grid(column=0,row=1, padx=(23,27), pady=(36,15))
        self.w_timeline = tk.Label(self.window, image = testImage, highlightthickness=0, bd=0)
        self.w_timeline.grid(column=0,row=2, padx=(23,27), pady=(0,0))
        self.w_editor = tk.Label(self.window, image = testImage, highlightthickness=0, bd=0)
        self.w_editor.grid(column=1,row=1, padx=(0,0), pady=(36,15))
        self.w_options = tk.Label(self.window, image = testImage, highlightthickness=0, bd=0)
        self.w_options.grid(column=1,row=2, padx=(0,0), pady=(0,0))

        '''start interface'''
        self.interface = Interface()

    def windowProcesses(self):
        '''window processes'''
        mx = self.window.winfo_pointerx()-self.window.winfo_rootx()
        my = self.window.winfo_pointery()-self.window.winfo_rooty()
        if self.mPressed > 0:
            self.mPressed += 1
        else:
            self.mPressed = 0

        '''update screens'''
        self.interface.tick(mx,my,self.mPressed, self.fps, self.keyQueue, self.mouseScroll)
        self.keyQueue = []
        self.mouseScroll = 0
        img = ImageTk.PhotoImage(self.interface.getImageAnimation())
        self.w_animation.configure(image = img)
        self.w_animation.image=img
        img = ImageTk.PhotoImage(self.interface.getImageTimeline())
        self.w_timeline.configure(image = img)
        self.w_timeline.image = img
        img = ImageTk.PhotoImage(self.interface.getImageEditor())
        self.w_editor.configure(image = img)
        self.w_editor.image = img
        img = ImageTk.PhotoImage(self.interface.getImageOptions())
        self.w_options.configure(image = img)
        self.w_options.image = img
        self.window.after(TICK_MS, self.windowProcesses)

        self.fpsCounter +=1
        if math.floor(time.time()) == round(time.time()) and not(self.fpsGood):
            self.fps = self.fpsCounter
            self.fpsCounter = 0
            self.fpsGood = True
        if math.ceil(time.time()) == round(time.time()) and self.fpsGood:
            self.fpsGood = False
        # print(f"FPS: {self.fps}")

    def windowOccasionalProcesses(self):
        '''window processes that happen less frequently (once every 3 seconds)'''
        print("windowOccaionalProcess")
        self.window.title(f"Tape - Editing: {self.interface.projectName}")
        print(self.getFPS())
        self.window.after(OCCASIONAL_TICK_MS, self.windowOccasionalProcesses)

    def windowStartupProcesses(self):
        '''window processes that occur once when startup'''
        print("windowStartupProcess")
        pass
    
    def getFPS(self): return self.fps
    def mPress(self, side = 0): self.mPressed = 1
    def mRelease(self, side = 0): self.mPressed = -999
    def keyPressed(self, key): self.keyQueue.append(str(key.keysym))
    def mouseWheel(self, event): self.mouseScroll -= event.delta
    
    def start(self):
        '''start window main loop'''
        print("windowStart")
        
        self.window.bind("<ButtonPress-1>", self.mPress)
        self.window.bind("<ButtonRelease-1>", self.mRelease)
        self.window.bind("<Key>", self.keyPressed)
        self.window.bind_all("<MouseWheel>", self.mouseWheel)

        self.window.after(TICK_MS, self.windowProcesses)
        self.window.after(TICK_MS, self.windowOccasionalProcesses)
        self.window.mainloop()
        self.window.after(0, self.windowStartupProcesses)