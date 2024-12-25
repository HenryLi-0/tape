'''This file makes sure that everything the program needs is set and ready to run!'''

'''Test import all major modules'''
from PIL import Image, ImageTk, ImageDraw
import tkinter as tk
import os, numpy, uuid, ast, time, math
from settings import *

'''Test import all subsystems'''
from subsystems.bay         import *
from subsystems.counter     import *
from subsystems.fancy       import *
from subsystems.interface   import *
from subsystems.point     import *
from subsystems.render      import *
from subsystems.visuals     import *
from subsystems.window      import *

class Check:
    def check():
        print("Finished Checks")

    def error(message):
        print(f"The check has detected an issue: {message}")
