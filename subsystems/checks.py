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
        
        # Themes
        Check.regenerateAllThemedOutline()

        # Tests?


        print("Finished Checks")

    def error(message):
        print(f"The check has detected an issue: {message}")

    def generateThemedOutline(path, name, frameColor = FRAME_COLOR, bgColor = BACKGROUND_COLOR):
        '''Generate a themed based on a black/transparent template'''
        frame = Image.open(path).convert("RGBA")
        frameArray = numpy.array(frame)
        
        blackMask = numpy.all(frameArray[:, :, :3] == [0, 0, 0], axis=-1)
        transparentMask = frameArray[:, :, 3] == 0
        
        result_array = numpy.copy(frameArray)
        result_array[blackMask] = hexColorToRGBA(frameColor)
        result_array[transparentMask] = (0,0,0,0) if bgColor=="transparent" else hexColorToRGBA(bgColor)
        
        with open(os.path.join("resources", "themed", f"{name}.png"), "w") as f:
            f.write("")
        Image.fromarray(result_array).save(os.path.join("resources", "themed", f"{name}.png"))

    def regenerateAllThemedOutline():
        '''Regenerate all themed images'''
        Check.generateThemedOutline(D_FRAME_ANIMATION_PATH, "u_frame_animation", bgColor="#000000")
        Check.generateThemedOutline(D_FRAME_TIMELINE_PATH, "u_frame_timeline")
        Check.generateThemedOutline(D_FRAME_EDITOR_PATH, "u_frame_editor")
        Check.generateThemedOutline(D_FRAME_EDITOR_VISUALS_PATH, "u_frame_editor_visuals")
        Check.generateThemedOutline(D_FRAME_EDITOR_VISUALS_GRAPH_PATH, "u_frame_editor_visuals_graph", frameColor=SELECTED_COLOR, bgColor="transparent")
        Check.generateThemedOutline(D_FRAME_EDITOR_VISUALS_GRAPH_BAR_PATH, "u_frame_editor_visuals_graph_bar")
        Check.generateThemedOutline(D_FRAME_OPTIONS_PATH, "u_frame_options")
        Check.generateThemedOutline(D_FRAME_OPTIONS_BUTTON_PATH, "u_frame_options_button_on", frameColor=SELECTED_COLOR)
        Check.generateThemedOutline(D_FRAME_OPTIONS_BUTTON_PATH, "u_frame_options_button_off")