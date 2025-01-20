from subsystems.node.node import Node
from subsystems.visuals import *

class VisualNode(VisualObject):
    '''A visual representation of a node.'''
    def __init__(self, name, pos:tuple|list, node:Node):
        # init
        self.type = "node"
        self.name = name
        self.node = node
        self.lastInteraction = time.time()
        
        self.n_input = self.node.Input
        self.n_display = self.node.Display
        self.n_output = self.node.Output
        self.generateTemplate()

    
    def generateTemplate(self):
        x = 75
        y = 19 + max(len(self.n_display)*19, len(self.n_input)*12, len(self.n_output)*12)
    
        self.template = generateBorderBox((x, y), 3, BACKGROUND_COLOR_RGBA, FRAME_COLOR_RGBA)
        placeOver(self.template, displayText(self.node.__class__.__name__, "m"), ((x+6)/2, 8+3), True)
        




    def tick(self, img, visualactive, active):
        y = 0
        placeOver(img, self.template, (0,0))
        
        
    def updateText(self, txt):
        pass
    def keyAction(self, keys):
        pass
    def updatePos(self, rmx, rmy):
        pass