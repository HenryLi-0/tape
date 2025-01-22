from subsystems.node.node import Node
from subsystems.visuals import *
from subsystems.settings import *

class VisualNode(VisualObject):
    '''A visual representation of a node.'''
    def __init__(self, name, pos:tuple|list, node:Node):
        # init
        self.type = "node"
        self.name = name
        self.node = node
        self.lastInteraction = time.time()
        self.positionO = RectangularPositionalBox((0,0), pos[0], pos[1])
        
        self.n_input = self.node.Input
        self.n_display = self.node.Display
        self.n_output = self.node.Output
        self.r_divider = generateColorBox((round(NODE_WIDTH.get()*0.5),1), (125,125,125,255))
        self.generateTemplate()
    
    def generateTemplate(self):
        x = NODE_WIDTH.get()+6*2
        mid_x = (NODE_WIDTH.get()+6)/2
        y_header = (NODE_SECTION_HEIGHT.get() + NODE_SECTION_DIVIDER_HEIGHT.get())
        y_body = max(len(self.n_display)*(NODE_SECTION_HEIGHT.get()+NODE_SECTION_DIVIDER_HEIGHT.get()), len(self.n_input)*12, len(self.n_output)*12)
        y = y_header + y_body
    
        self.r_template_main = generateBorderBox((x, y), 3, BACKGROUND_COLOR_RGBA, FRAME_COLOR_RGBA)
        placeOver(self.r_template_main, displayText(self.node.__class__.__name__, "m"), (mid_x, 3+NODE_SECTION_HEIGHT.get()/2), True)
        '''Displays'''
        for i in range(len(self.n_display)):
            h = (NODE_SECTION_HEIGHT.get() + NODE_SECTION_DIVIDER_HEIGHT.get())*i
            placeOver(self.r_template_main, self.r_divider, (mid_x, 10+NODE_SECTION_HEIGHT.get()+ h), True)
            placeOver(self.r_template_main, displayText(self.n_display[i][0], "m"), (6+3+5,NODE_SECTION_HEIGHT.get()*1.5+h))
            if not(self.n_display[i][1]): # not modifyable
                temp = displayText(self.n_display[i][2](), "m")
                placeOver(self.r_template_main, temp, (x-3-temp.width,NODE_SECTION_HEIGHT.get()*1.5+h))
            else:
                pass # TO-DO: FILL IN AREA

        '''Inputs'''
        if len(self.n_input) > 0:
            temp = []
            for i in range(len(self.n_input)):
                temp.append(displayText(f" {self.n_input[i][0]} ", "sm", NODE_IO_BACKGROUND_RGBA.get(), NODE_IO_UNCAPPED_RGBA.get() if self.n_input[i][3] else NODE_IO_NORMAL_RGBA.get()))
            x = max([x.width for x in temp])
            self.r_template_inputs = generateColorBox((x, y_body), (0,0,0,0))
            mul = y_body/(len(temp)+1)
            for i in range(len(temp)):
                placeOver(self.r_template_inputs, temp[i], (x-temp[i].width/2, mul*(1+i)), True)
                placeOver(self.r_template_main) # TO-DO: CONTINUE HERE!
        else:
            self.r_template_inputs = EMPTY_IMAGE.copy()
        
        '''Output'''
        if len(self.n_output) > 0:
            temp = []
            for i in range(len(self.n_output)):
                temp.append(displayText(f" {self.n_output[i][0]} ", "sm", NODE_IO_BACKGROUND_RGBA.get(), NODE_IO_NORMAL_RGBA.get()))
            x = max([x.width for x in temp])
            self.r_template_outputs = generateColorBox((x, y_header+y_body), (0,0,0,0))
            mul = y_body/(len(temp)+1)
            for i in range(len(temp)):
                placeOver(self.r_template_outputs, temp[i], (temp[i].width/2, y_header+mul*(1+i)), True)
        else:
            self.r_template_outputs = EMPTY_IMAGE.copy()




    def tick(self, img, visualactive, active):
        y = 0
    
    def render(self, img, pos):
        placeOver(img, self.r_template_main, (pos[0],pos[1]))
        placeOver(img, self.r_template_inputs, (pos[0]-self.r_template_inputs.width-5,pos[1]+3))
        placeOver(img, self.r_template_outputs, (pos[0]+self.r_template_main.width+5,pos[1]+3))

        
        
    def updateText(self, txt):
        pass
    def keyAction(self, keys):
        pass
    def updatePos(self, rmx, rmy):
        pass