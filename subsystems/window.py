from settings import *
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
import time, numpy, os, math
from subsystems.interface import Interface
from settings import BACKGROUND_COLOR

class Window:
    def __init__(self):
        '''initalize tk window'''
        self.window= tk.Tk()
        self.window.grid()
        self.window.title("Tape")
        self.window.geometry("1366x697")
        self.window.configure(background=BACKGROUND_COLOR)
        self.fps = 0
        self.fpsCounter = 0
        self.fpsGood = False

        '''load test image'''
        self.animation = tk.Label(self.window, image = ImageTk.PhotoImage(PLACEHOLDER_IMAGE))
        self.animation.grid(column=1,row=1)
        self.timeline = tk.Label(self.window, image = ImageTk.PhotoImage(PLACEHOLDER_IMAGE))
        self.timeline.grid(column=1,row=2)
        self.editor = tk.Label(self.window, image = ImageTk.PhotoImage(PLACEHOLDER_IMAGE))
        self.editor.grid(column=2,row=1)
        self.options = tk.Label(self.window, image = ImageTk.PhotoImage(PLACEHOLDER_IMAGE))
        self.options.grid(column=2,row=2)

        '''start interface'''
        self.interface = Interface()

    def windowProcesses(self):
        '''window processes'''
        self.interface.tick()
        img = ImageTk.PhotoImage(self.interface.getImage())
        self.animation.configure(image = img)
        self.animation.image=img
        img = ImageTk.PhotoImage(PLACEHOLDER_IMAGE)
        self.timeline.configure(image = img)
        self.timeline.image = img
        self.window.after(TICK_MS, self.windowProcesses)

        self.fpsCounter +=1
        if math.floor(time.time()) == round(time.time()) and not(self.fpsGood):
            self.fps = self.fpsCounter
            self.fpsCounter = 0
            self.fpsGood = True
        if math.ceil(time.time()) == round(time.time()) and self.fpsGood:
            self.fpsGood = False
        # print(f"FPS: {self.fps}")
        
    def getFPS(self):
        return self.fps
    
    def start(self):
        '''start window main loop'''
        self.window.after(TICK_MS, self.windowProcesses)
        self.window.mainloop()