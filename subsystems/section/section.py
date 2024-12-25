'''This file is a template section'''
from subsystems.state import State
from subsystems.render import *
from subsystems.fancy import *
from subsystems.simplefancy import *
from subsystems.visuals import *
from subsystems.point import *

class Section:
    def render(state: State, im):
        '''Example Area: `(   x,   y) to (   x,   y)` : size `(   x,   y)`'''
        img = im.copy()
        rmx = state.mx - 0
        rmy = state.my - 0

        placeOver(img, displayText(f"FPS: {state.fps}", "m"), (20,20))
        placeOver(img, displayText(f"Interacting With: {state.interacting}", "m"), (20,55))
        placeOver(img, displayText(f"length of IVO: {len(state.ivos)}", "m"), (20,90))
        placeOver(img, displayText(f"Mouse Pos: ({state.mx}, {state.my})", "m"), (200,20))
        placeOver(img, displayText(f"Mouse Press: {state.mPressed}", "m", colorTXT=(100,255,100,255) if state.mPressed else (255,100,100,255)), (200,55))

        for id in state.ivos:
            if state.ivos[id][0] == "h":
                state.ivos[id][1].tick(img, state.interacting==id or ((state.lastInteraction==id) and (abs(time.time() - state.ivos[id][1].lastInteraction) < LAST_INTERACTION_KEY_TIME)), state.interacting==id)

        Section.overlayCrosshair(state, img, rmx, rmy)

        return img    
    
    def overlayCrosshair(state: State, im, rmx, rmy):
        if SHOW_CROSSHAIR:
            if state.mPressed: placeOver(im, CURSOR_SELECT, (rmx, rmy), True)
            else: placeOver(im, CURSOR_ARROW, (rmx, rmy), True)