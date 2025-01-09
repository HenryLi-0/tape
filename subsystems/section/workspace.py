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

        placeOver(img, scaleImage(state, PLACEHOLDER_IMAGE_5), scaleCoords(state, 10,10))
        placeOver(img, scaleImage(state, PLACEHOLDER_IMAGE_5), scaleCoords(state, 50,50))



        placeOver(img, displayText(f"FPS: {state.fps}", "m", (0,0,0,50), (255,255,255,255)), (20,20))
        placeOver(img, displayText(f"X,Y,ZOOM: {state.workspaceX, state.workspaceY, state.workspaceZoom}", "m", (0,0,0,50), (255,255,255,255)), (20,50))

        for id in state.ivos:
            if state.ivos[id][0] == "w":
                state.ivos[id][1].tick(img, state.interacting==id or ((state.lastInteraction==id) and (abs(time.time() - state.ivos[id][1].lastInteraction) < LAST_INTERACTION_KEY_TIME)), state.interacting==id)

        Section.overlayCrosshair(state, img, rmx, rmy)

        return img
    
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

from subsystems.node.node import Node
from subsystems.visuals import *

class VisualNode(VisualObject):
    '''A visual representation of a node.'''
    def __init__(self, name, pos:tuple|list, node:Node, intOnly = False):
        # init
        self.type = "node"
        self.name = name
        self.lastInteraction = time.time()

        self.header = generateColorBox((100,25),(255,127,0,255))
        placeOver(self.header, displayText(node.__class__.__name__, 7), (0,0))

        inputs = node.Inputs
        ouputs = node.Outputs



    def tick(self, img, visualactive, active):
        y = 0
        placeOver(img, self.header, (0,0))
        y += self.header.height
        
    def updateText(self, txt):
        pass
    def keyAction(self, keys):
        pass
    def updatePos(self, rmx, rmy):
        pass