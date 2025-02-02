from subsystems.node.node import Node
from subsystems.visuals import *
from subsystems.settings import *
from subsystems.node.node import *

class NodeRectangularPositionalBox:
    def __init__(self, bbox:tuple|list = (10,10), ix = 0, iy = 0):
        '''Bounding box will NOT be centered!'''
        self.bbox, self.ix, self.iy, self.insx, self.insy = bbox, ix, iy, ix, iy
    def process(self, interact, rmx, rmy):
        '''Should be called whenever the position wants to question its position'''
        if interact: self.ix, self.iy = rmx, rmy
    def getInteract(self, rmx, rmy):
        '''Returns whether or not the mouse is in the bounding box of interaction'''
        return (self.ix < rmx) and (rmx < (self.ix+self.bbox[0])) and (self.iy < rmy) and (rmy < (self.iy+self.bbox[1]))
    def getPosition(self): return (self.ix, self.iy)
    def getX(self): return self.ix
    def getY(self): return self.iy
    def getBBOX(self): return self.bbox
    def setPosition(self, position: tuple|list): self.ix, self.iy = position
    def setX(self, nx): self.ix = nx
    def setY(self, ny): self.iy = ny
    def setBBOX(self, nbbox): self.bbox = nbbox

    def getNodeSpacePosition(self): return (self.insx, self.insy)
    def getNodeSpaceX(self): return self.insx
    def getNodeSpaceY(self): return self.insy
    def setNodeSpacePosition(self, position: tuple|list): self.insx, self.insy = position
    def setNodeSpaceX(self, nx): self.insx = nx
    def setNodeSpaceY(self, ny): self.insy = ny


class NodeNoPositionalBox:
    def __init__(self): pass
    def process(self, interact, rmx, rmy): pass
    def getInteract(self, rmx, rmy): return False
    def getPosition(self): return (0,0)
    def getX(self): return 0
    def getY(self): return 0
    def getBBOX(self): return (0,0)
    def setPosition(self, position: tuple|list): pass
    def setX(self, nx): pass
    def setY(self, ny): pass
    def setBBOX(self, nbbox): pass
    def getNodeSpacePosition(self): return (0,0)
    def getNodeSpaceX(self): return 0
    def getNodeSpaceY(self): return 0
    def setNodeSpacePosition(self, position: tuple|list): pass
    def setNodeSpaceX(self, nx): pass
    def setNodeSpaceY(self, ny): pass


class VisualNode(VisualObject):
    '''A visual representation of a node.'''
    def __init__(self, name, pos:tuple|list, node:Node):
        # init
        self.type = "node"
        self.name = name
        self.node = node
        self.lastInteraction = time.time()
        self.positionO = NodeRectangularPositionalBox((0,0), pos[0], pos[1])
        
        self.n_input = self.node.Input
        self.n_display = self.node.Display
        self.n_output = self.node.Output
        theme = NODE_THEMES_ASSGINMENT[self.node.__class__] if self.node.__class__ in NODE_THEMES_ASSGINMENT else NODE_THEMES_ASSGINMENT["default"]
        self.r_nodeInnerColor = translatePastel(theme, 0.5)
        self.r_nodeBorderColor = translatePastel(theme, 0.2)
        self.r_divider = generateColorBox((round(NODE_WIDTH.get()*0.5),1), self.r_nodeBorderColor)
        self.r_inputX = 0
        self.r_inputYAdd = 0
        self.r_inputYMul = 1
        self.r_outputX = 0
        self.r_outputYAdd = 0
        self.r_outputYMul = 1
        self.generateTemplate()
    
    def generateTemplate(self):
        node_x = NODE_WIDTH.get()
        node_mid_x = (NODE_WIDTH.get()+6+20)/2
        y_header = (NODE_SECTION_HEIGHT.get() + NODE_SECTION_DIVIDER_HEIGHT.get())
        y_body = max(len(self.n_display)*(NODE_SECTION_HEIGHT.get()+NODE_SECTION_DIVIDER_HEIGHT.get()), len(self.n_input)*24, len(self.n_output)*24)
        y = y_header + y_body
    
        self.r_template_main = generateBorderBox((node_x, y), 3, self.r_nodeBorderColor, self.r_nodeInnerColor)
        self.r_template_main = addBlank(self.r_template_main, 10, "E", (0,0,255,255) if DEBUG.get() else (0,0,0,0))
        self.r_template_main = addBlank(self.r_template_main, 10, "W", (0,0,255,255) if DEBUG.get() else (0,0,0,0))
        placeOver(self.r_template_main, displayText(self.node.__class__.__name__, "m"), (node_mid_x, 3+NODE_SECTION_HEIGHT.get()/2), True)
        '''Displays'''
        for i in range(len(self.n_display)):
            h = (NODE_SECTION_HEIGHT.get() + NODE_SECTION_DIVIDER_HEIGHT.get())*i
            placeOver(self.r_template_main, self.r_divider, (node_mid_x, 10+NODE_SECTION_HEIGHT.get()+ h), True)
            placeOver(self.r_template_main, displayText(self.n_display[i][0], "sm"), (10+3+5,NODE_SECTION_HEIGHT.get()*1.5+h))

        '''Inputs'''
        if len(self.n_input) > 0:
            temp = []
            for i in range(len(self.n_input)):
                temp.append(displayText(f" {self.n_input[i][0]} ", "s", NODE_IO_BACKGROUND_RGBA.get(), NODE_IO_UNCAPPED_RGBA.get() if self.n_input[i][3] else NODE_IO_NORMAL_RGBA.get()))
            x = max([x.width for x in temp])
            self.r_template_inputs = generateColorBox((x, y_header + y_body), (255,0,0,255) if DEBUG.get() else (0,0,0,0))
            self.r_inputX = 6
            self.r_inputYAdd = y_header + (y_body/(len(temp)+1))
            self.r_inputYMul = y_body/(len(temp)+1)
            for i in range(len(temp)):
                placeOver(self.r_template_inputs, temp[i], (x-temp[i].width/2, self.r_inputYMul * i + self.r_inputYAdd), True)
                placeOver(self.r_template_main, NODE_THEMES_TRIANGLES[NODE_THEMES_ASSGINMENT[self.n_input[i][1][0]]], (6, self.r_inputYMul * i  + self.r_inputYAdd), True)
        else:
            self.r_template_inputs = EMPTY_IMAGE.copy()
        
        '''Output'''
        if len(self.n_output) > 0:
            temp = []
            for i in range(len(self.n_output)):
                temp.append(displayText(f" {self.n_output[i][0]} ", "s", NODE_IO_BACKGROUND_RGBA.get(), NODE_IO_NORMAL_RGBA.get()))
            x = max([x.width for x in temp])
            self.r_template_outputs = generateColorBox((x, y_header+y_body), (255,0,0,255) if DEBUG.get() else (0,0,0,0))
            self.r_outputX = node_x + 15 + 2*3
            self.r_outputYAdd = y_header + (y_body/(len(temp)+1))
            self.r_outputYMul = y_body/(len(temp)+1)
            for i in range(len(temp)):
                placeOver(self.r_template_outputs, temp[i], (temp[i].width/2, i * self.r_outputYMul + self.r_outputYAdd), True)
                placeOver(self.r_template_main, NODE_THEMES_TRIANGLES[NODE_THEMES_ASSGINMENT[self.n_output[i][1]]], (self.r_outputX, i * self.r_outputYMul + self.r_outputYAdd), True)
        else:
            self.r_template_outputs = EMPTY_IMAGE.copy()

    def tick(self, img, visualactive, active):
        if active:
            pass
    
    def render(self, img, pos, zoom):
        templateC = self.r_template_main.copy()

        for i in range(len(self.n_display)):
            h = (NODE_SECTION_HEIGHT.get() + NODE_SECTION_DIVIDER_HEIGHT.get())*i
            if not(self.n_display[i][1]): # not modifyable
                data = self.n_display[i][2](self.node)
                if type(data) == bool:
                    temp = displayText(data, "sm", colorTXT=(150,255,150,255) if data else (255,150,150,255))
                elif type(data) == int:
                    if len(str(data)) > 7:
                        temp = displayText(format(data, ".2e"), "sm")
                    else:
                        temp = displayText(data, "sm")
                elif type(data) == float:
                    if len(str(data)) > 7:
                        if data < 10**5:
                            temp = displayText("{:5.3f}".format(data).rstrip("0").rstrip("."), "sm")
                        else:
                            temp = displayText(format(data, ".2e"), "sm")
                    else:
                        temp = displayText(data, "sm")
                else:
                    temp = displayText(data, "sm")
                placeOver(templateC, temp, (NODE_WIDTH.get()-3-temp.width,NODE_SECTION_HEIGHT.get()*1.5+h))
            else: pass

        placeOver(img, templateC, (pos[0],pos[1]))

        placeOver(img, self.r_template_inputs, (pos[0]-self.r_template_inputs.width-10,pos[1]+3))
        placeOver(img, self.r_template_outputs, (pos[0]+self.r_template_main.width+10,pos[1]+3))

        
        
    def updateText(self, txt):
        pass
    def keyAction(self, keys):
        pass
    def updatePos(self, rmx, rmy):
        pass


class VisualNodeConnection(VisualObject):
    '''A connection between two parts of a node.'''
    def __init__(self, name, nodeA:VisualNode, nodeAindex:int, nodeB:VisualNode, nodeBindex:int):
        # init
        self.type = "node connection"
        self.name = name
        self.lastInteraction = time.time()
        self.positionO = NodeNoPositionalBox()
        
        self.nodeA = nodeA # Output side
        self.nodeAindex = nodeAindex
        self.nodeB = nodeB # Input side
        self.nodeBindex = nodeBindex

        self.r_pixel = generateColorBox((3,3), NodeThemes.UNKNOWN)
        self.generateTemplate()

    def generateTemplate(self):
        self.r_pixel = generateColorBox((3,3), NODE_THEMES_ASSGINMENT[self.nodeA.node.Output[self.nodeAindex][1]])

    def render(self, img, pos, zoom):
        nodeApos = addP(self.nodeA.positionO.getPosition(), (self.nodeA.r_outputX, self.nodeAindex * self.nodeA.r_outputYMul + self.nodeA.r_outputYAdd))
        nodeBpos = addP(self.nodeB.positionO.getPosition(), (self.nodeB.r_inputX , self.nodeBindex * self.nodeB.r_inputYMul  + self.nodeB.r_inputYAdd ))

        step = multiplyP(subtractP(nodeBpos, nodeApos), 0.01)
        for i in range(100):
            placeOver(img, self.r_pixel, addP(multiplyP(addP(nodeApos, multiplyP(step, i)), zoom), pos))

    def tick(self, img, visualactive, active):
        pass
    def updateText(self, txt):
        pass
    def keyAction(self, keys):
        pass
    def updatePos(self, rmx, rmy):
        pass

class NodeEditableTextBoxVisualObject(VisualObject):
    '''An editable text box for nodes.'''
    def __init__(self, name, node:VisualNode, index:int = 0, startTxt= "", maxSize = (50,25)):
        self.type = "node textbox"
        self.name = name
        self.lastInteraction = time.time()

        self.n_node = node
        self.n_index = index

        self.txt = str(startTxt)
        self.txtImg = displayText(self.txt, "sm")

        temp = NODE_THEMES_ASSGINMENT[self.n_node.node.__class__]
        temp2 = translatePastel(temp, 0.3)
        temp3 = translatePastel(temp, 0.6)
        temp4 = translatePastel(temp, 0.8)
        self.r_templateIdle = generateColorBox(maxSize, temp2)
        self.r_templateActive = generateColorBox(maxSize, temp3)

        self.positionO = NodeRectangularPositionalBox(maxSize, self.n_node.positionO.getX(), self.n_node.positionO.getY() + (index+0.5) * NODE_SECTION_HEIGHT.get())
        self.underlineIdle = generateColorBox((maxSize[0],3), temp3)
        self.underlineActive = generateColorBox((maxSize[0],3), temp4)
        
    def tick(self, img, visualactive, active):
        if active: self.lastInteraction = time.time()
        temp = self.r_templateActive.copy() if visualactive else self.r_templateIdle.copy()
        placeOver(temp, self.underlineActive if visualactive else self.underlineIdle, (0, self.positionO.getBBOX()[1]-3))
        placeOver(temp, self.txtImg, (50-self.txtImg.width,0), False)
        placeOver(img, temp, self.positionO.getPosition())

    def updateText(self):
        output = self.txt
        if type(self.n_node.node)==Number:
            try:
                output = float(self.txt)
            except:
                temp = list(str(self.txt))
                for item in temp:
                    if item not in "0123456789":
                        while item in temp: temp.remove(item)
                    output = "".join(temp)
                    self.txt = output
        elif type(self.n_node.node)==Boolean:
            if output=="0" or output=="" or "f" in output or "F" in output:
                output = False
            else:
                output = True
        elif type(self.n_node.node)==String:
            output = str(self.txt)

        self.txtImg = displayText(self.txt, "sm")
        self.n_node.n_display[self.n_index][2](self.n_node.node, output)

    def keyAction(self, keys):
        self.lastInteraction = time.time()
        prevtxt = self.txt
        for key in keys:
            if key in KB_CONFIRM: break
            if key == -1:self.txt = self.txt[0:-1]
            else: self.txt += chr(key)
        if prevtxt != self.txt:
            self.updateText()

    def render(self, img, pos, zoom):
        self.positionO.setPosition(addP(pos, multiplyP((20 + NODE_WIDTH.get()/2, (self.n_index+1) * NODE_SECTION_HEIGHT.get() - 3), zoom)))

    def updatePos(self, rmx, rmy):
        pass

class NodeConnectionPoint(VisualObject):
    '''An connection point for nodes.'''
    def __init__(self, name, nodeID, node:VisualNode, index:int = 0, isInput = True):
        self.type = "node connection point"
        self.name = name
        self.lastInteraction = time.time()

        self.n_nodeID = nodeID
        self.n_node = node
        self.n_index = index
        if isInput:
            self.n_type = node.n_input[index][1]
        else:
            self.n_type = node.n_output[index][1]
        self.n_input = isInput
        self.out_connectionRequest = None
        
        if isInput:
            pos = addP(self.n_node.positionO.getNodeSpacePosition(), (self.n_node.r_inputX , self.n_index * self.n_node.r_inputYMul  + self.n_node.r_inputYAdd ))
        else:
            pos = addP(self.n_node.positionO.getNodeSpacePosition(), (self.n_node.r_outputX, self.n_index * self.n_node.r_outputYMul + self.n_node.r_outputYAdd))

        self.positionO = NodeRectangularPositionalBox((10,10), pos[0]-5, pos[1]-5)
        self.visual = generateColorBox((10,10), (255,255,255,127))
        
    def tick(self, img, visualactive, active):
        if active: self.lastInteraction = time.time()
        placeOver(img, self.visual, self.positionO.getPosition())

    def render(self, img, pos, zoom):
        self.positionO.setPosition(pos)

    def updatePos(self, rmx, rmy):
        if not(self.n_input):
            self.positionO.setPosition((rmx, rmy))
            self.out_connectionRequest = [rmx, rmy]
