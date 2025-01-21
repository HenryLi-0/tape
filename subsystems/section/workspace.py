from subsystems.section.section import *

def scaleCoords(state:State, x, y):
    return (state.workspaceZoom*x-state.workspaceX, state.workspaceZoom*y-state.workspaceY)

def scaleImage(state:State, img):
    return setSize(img, state.workspaceZoom*100)

class Workspace(Section):
    def render(state: State, im):
        '''Workspace Interface:  `( 485,  10) to (1355, 687)`: size `( 871, 678)`'''
        img = im.copy()
        rmx = state.mx - 485
        rmy = state.my - 10

        placeOver(img, scaleImage(state, PLACEHOLDER_IMAGE_5), scaleCoords(state, 110, 110))
        placeOver(img, scaleImage(state, PLACEHOLDER_IMAGE_5), scaleCoords(state, 150, 150))



        placeOver(img, displayText(f"FPS: {state.fps}", "m", (0,0,0,50), (255,255,255,255)), (20,20))
        placeOver(img, displayText(f"X,Y,ZOOM: {state.workspaceX, state.workspaceY, state.workspaceZoom}", "m", (0,0,0,50), (255,255,255,255)), (20,50))

        for id in state.ivos:
            if state.ivos[id][0] == "w":
                state.ivos[id][1].tick(img, state.interacting==id or ((state.lastInteraction==id) and (abs(time.time() - state.ivos[id][1].lastInteraction) < LAST_INTERACTION_KEY_TIME)), state.interacting==id)
                if state.ivos[id][1].type == "node":
                    state.ivos[id][1].render(img, scaleCoords(state, state.ivos[id][1].positionO.getX(), state.ivos[id][1].positionO.getY()))

        Section.overlayCrosshair(state, img, rmx, rmy)

        return img