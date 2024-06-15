from settings import TICK_MS, PLACEHOLDER_IMAGE
import tkinter as tk
from PIL import ImageTk, Image
import time, numpy, os
from subsystems.interface import Interface

class Window:
    def __init__(self):
        '''initalize tk window'''
        self.window= tk.Tk()
        self.window.grid()
        self.window.title("Tape")
        self.window.geometry("500x500")
        self.window.configure(background='grey')

        '''load test image'''
        img = ImageTk.PhotoImage(PLACEHOLDER_IMAGE)
        self.panel = tk.Label(self.window, image = img)
        self.panel.pack(side = "bottom", fill = "both", expand = "yes")

        '''start interface'''
        self.interface = Interface()

    def windowProcesses(self):
        '''window processes'''
        self.interface.tick()
        img = ImageTk.PhotoImage(self.interface.getImage())
        self.panel.configure(image = img)
        self.panel.image=img
        self.window.after(TICK_MS, self.windowProcesses)
    
    def start(self):
        '''start window main loop'''
        self.window.after(TICK_MS, self.windowProcesses)
        self.window.mainloop()