from settings import *
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
import time, numpy, os, math
from subsystems.interface import Interface
from settings import *

class Window:
    def __init__(self):
        '''initalize tk window'''
        self.window= tk.Tk()
        self.window.grid()
        self.window.title("Tape")
        self.window.geometry("1366x698")
        self.window.configure(background="#555555")
        self.fps = 0
        self.fpsCounter = 0
        self.fpsGood = False

        '''load test image'''
        testImage = ImageTk.PhotoImage(PLACEHOLDER_IMAGE)
        self.w_animation = tk.Label(self.window, image = testImage, highlightthickness=0, bd=0)
        self.w_animation.grid(column=1,row=1)
        self.w_timeline = tk.Label(self.window, image = testImage, highlightthickness=0, bd=0)
        self.w_timeline.grid(column=1,row=3)
        self.w_editor = tk.Label(self.window, image = testImage, highlightthickness=0, bd=0)
        self.w_editor.grid(column=3,row=1)
        self.w_options = tk.Label(self.window, image = testImage, highlightthickness=0, bd=0)
        self.w_options.grid(column=3,row=3)

        '''load spacers'''
        self.w_spacer00 = tk.Label(self.window, image = testImage, highlightthickness=0, bd=0)
        self.w_spacer00.grid(column=0,row=0)
        self.w_spacer20 = tk.Label(self.window, image = testImage, highlightthickness=0, bd=0)
        self.w_spacer20.grid(column=2,row=0)
        self.w_spacer02 = tk.Label(self.window, image = testImage, highlightthickness=0, bd=0)
        self.w_spacer02.grid(column=0,row=2)

        '''start interface'''
        self.interface = Interface()

    def windowProcesses(self):
        '''window processes'''
        self.interface.tick()
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
        print(f"FPS: {self.fps}")

    def windowOccasionalProcesses(self):
        '''window processes that happen less frequently (once every 3 seconds)'''
        print("test")
        self.window.after(OCCASIONAL_TICK_MS, self.windowOccasionalProcesses)

    def windowStartupProcesses(self):
        '''window processes that occur once when startup'''
        self.w_spacer00.configure(image = ImageTk.PhotoImage(SPACER00))
        self.w_spacer00.image=ImageTk.PhotoImage(SPACER00)
        self.w_spacer20.configure(image = ImageTk.PhotoImage(SPACER02))
        self.w_spacer20.image=ImageTk.PhotoImage(SPACER02)
        self.w_spacer02.configure(image = ImageTk.PhotoImage(SPACER20))
        self.w_spacer02.image=ImageTk.PhotoImage(SPACER20)
    
    def getFPS(self):
        return self.fps
    
    def start(self):
        '''start window main loop'''
        self.window.after(TICK_MS, self.windowProcesses)
        self.window.after(TICK_MS, self.windowOccasionalProcesses)
        self.window.mainloop()
        self.window.after(0, self.windowStartupProcesses)