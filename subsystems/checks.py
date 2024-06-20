'''This file makes sure that everything the program needs is set and ready to run!'''

from PIL import Image
import os, numpy
from settings import *

class Check:
    def check():
        # Program/Subsystem Files
        
        # Resource Files
        
        # Cache
        
        # Themes
        Check.fixGeneratedThemedOutline()

        # Tests?


        print("Finished Checks")

    def generateThemedOutline(path, name):
        frame = Image.open(path).convert("RGBA")
        frameArray = numpy.array(frame)
        
        blackMask = numpy.all(frameArray[:, :, :3] == [0, 0, 0], axis=-1)
        transparentMask = frameArray[:, :, 3] == 0
        
        result_array = numpy.copy(frameArray)
        result_array[blackMask] = hexColorToRGB(FRAME_COLOR)
        result_array[transparentMask] = hexColorToRGB(BACKGROUND_COLOR)
        
        with open(os.path.join("resources", "themed", f"{name}.png"), "w") as f:
            f.write("")
        Image.fromarray(result_array).save(os.path.join("resources", "themed", f"{name}.png"))

    def fixGeneratedThemedOutline():
        Check.generateThemedOutline(D_FRAME_ANIMATION_PATH, "u_frame_animation")
        Check.generateThemedOutline(D_FRAME_TIMELINE_PATH, "u_frame_timeline")
        Check.generateThemedOutline(D_FRAME_EDITOR_PATH, "u_frame_editor")
        Check.generateThemedOutline(D_FRAME_OPTIONS_PATH, "u_frame_options")
