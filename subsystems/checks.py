'''This file makes sure that everything the program needs is set and ready to run!'''

'''Test import all major modules'''
from PIL import Image, ImageTk, ImageDraw
import tkinter as tk
import os, numpy, uuid, ast, time, math
from settings import *

'''Test import all subsystems'''


class Check:
    def check():
        # Program/Subsystem Files
        import subsystems.bay
        import subsystems.counter
        import subsystems.fancy
        import subsystems.interface
        import subsystems.pathing
        import subsystems.render
        import subsystems.visuals
        import subsystems.window
        # Resource Files
        
        # Cache

        # Tests?


        print("Finished Checks")

    def error(message):
        print(f"The check has detected an issue: {message}")
