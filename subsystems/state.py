'''This file is used for transfering information from interface tick and image rendering processes'''

from subsystems.visuals import *
from subsystems.visuals_node import *
from subsystems.counter import Counter
from settings import *
from subsystems.node.node import *

class State:
    def __init__(self):
        self.mx = 0
        self.my = 0
        self.prevmx = 0
        self.prevmy = 0
        self.mPressed = False
        self.mRising = False
        self.fps = 0
        self.ticks = 0
        self.deltaTicks = 1
        self.activity = ""
        self.c = Counter()
        '''Interactable Visual Objects'''
        '''
        Code:
        a - animation tab
        n - nodes tab
        d - debug tab
        e - editor tab
        s - setting tab
        t - tabs
        w - workspace
        '''
        self.ivos = {
            -999 : [" ", DummyVisualObject("dummy", (0,0))], # used for not interacting with anything
            -998 : [" ", DummyVisualObject("dummy", (0,0))], # used for text boxes
            -997 : [" ", DummyVisualObject("dummy", (0,0))], # used by keybinds
            -996 : [" ", DummyVisualObject("dummy", (0,0))], # used by scrolling


            -99 : ["t",IconVisualObject("Animation", (9,3), ANIMATION_TAB, outline = False)],
            -98 : ["t",IconVisualObject("Nodes", (49,3), NODES_TAB, outline = False)],
            -97 : ["t",IconVisualObject("Debug", (89,3), DEBUG_TAB, outline = False)],
            -96 : ["t",IconVisualObject("Export", (129,3), EXPORT_TAB, outline = False)],
            -95 : ["t",IconVisualObject("Settings", (169,3), SETTINGS_TAB, outline = False)],
        }
        '''Control'''
        self.interacting = -999
        self.previousInteracting = -999
        self.lastInteraction = self.interacting
        self.mouseScroll = 0 
        self.risingKeyQueue = []
        self.previousKeyQueue = []
        self.consoleAlerts = []
        self.keybindLastUpdate = time.time()
        self.currentKeybind = [False, None]
        '''Sliders'''
        self.sliders = []
        self.slidersData = []
        '''Updating'''
        self.scheduledSectionUpdate = []
        '''Tape'''
        self.tab = "a"
        self.previousTab = None
        self.nodes = {}
        self.nodeIDs = list(self.nodes.keys())
        self.nodesConnectionData = list(self.nodes.keys())
        self.nodeErrors = []
        self.nodeConnections = []
        self.nodeConnectors = []

        self.summonNode(Number(), (0, 0))
        self.summonNode(Number(), (0, 100))
        self.summonNode(Boolean(), (0, 200))

        self.summonNode(Random(), (250, 0))
        self.summonNode(Number(), (250, 200))

        self.summonNode(Pixels(), (500, 0))

        self.summonNode(Coordinate(), (750, 0))
        self.summonNode(RawUnit(), (1000, 0))


        self.workspaceX = 0
        self.workspaceY = 0
        self.workspaceZoom = 1
        self.workspaceXV = 0
        self.workspaceYV = 0


    def mouseInSection(self, section):
        return SECTIONS_DATA[section][0][0] <= self.mx and self.mx <= SECTIONS_DATA[section][1][0] and SECTIONS_DATA[section][0][1] <= self.my and self.my <= SECTIONS_DATA[section][1][1]
    def mouseWasInSection(self, section):
        return SECTIONS_DATA[section][0][0] <= self.prevmx and self.prevmx <= SECTIONS_DATA[section][1][0] and SECTIONS_DATA[section][0][1] <= self.prevmy and self.prevmy <= SECTIONS_DATA[section][1][1]

    def tick(self,mx,my,mPressed,fps,keyQueue,mouseScroll):
        '''Entire Screen: `(0,0) to (1365,697)`: size `(1366,698)`'''
        self.prevmx = self.mx
        self.prevmy = self.my
        self.mx = mx if (0<=mx and mx<=1365) and (0<=my and my<=697) else self.mx 
        self.my = my if (0<=mx and mx<=1365) and (0<=my and my<=697) else self.my
        self.mPressed = mPressed > 0
        self.mRising = mPressed==2
        self.fps = fps
        self.deltaTicks = 1 if self.fps==0 else round(INTERFACE_FPS/self.fps)
        self.ticks += self.deltaTicks
        
        self.mouseInAnimationTab =  self.mouseInSection("a")
        self.mouseInNodesTab =      self.mouseInSection("n")
        self.mouseInDebugTab =      self.mouseInSection("d")
        self.mouseInExportTab =     self.mouseInSection("e")
        self.mouseInSettingsTab =   self.mouseInSection("s")
        self.mouseInTabs =          self.mouseInSection("t")
        self.mouseInWorkspace =     self.mouseInSection("w")

        '''tape'''
        if self.interacting in [-99, -98, -97, -96, -95]:
            self.tab = self.ivos[self.interacting][1].name[0].lower()

        # node connection creation logic
        if self.ivos[self.previousInteracting][1].type == "node connection point" and self.interacting != self.previousInteracting:
            if self.ivos[self.previousInteracting][1].out_connectionRequest != None:
                here = addP(self.ivos[self.previousInteracting][1].out_connectionRequest, (self.workspaceX, self.workspaceY))
                nodeSpace = []
                for connectorID in self.nodeConnectors:
                    if self.ivos[connectorID][1].n_input:
                        nodeSpace.append(distanceP(self.ivos[connectorID][1].positionO.getNodeSpacePosition(), here))
                    else:
                        nodeSpace.append(math.inf)
                closest = self.nodeConnectors[nodeSpace.index(min(nodeSpace))]
                if distanceP(self.ivos[closest][1].positionO.getNodeSpacePosition(), here) < 25:
                    # test if types match
                    valid = False
                    for parent in self.ivos[self.previousInteracting][1].n_type.__bases__:
                        if parent in self.ivos[closest][1].n_type:
                            valid = True
                    print(self.ivos[closest][1].n_type)
                    print(self.ivos[self.previousInteracting][1].n_type.__bases__)
                    if self.ivos[self.previousInteracting][1].n_type in self.ivos[closest][1].n_type or valid:
                        # check if input is taken and is not infinite
                        valid = True
                        for connection in self.nodeConnections:
                            if connection[2] == self.ivos[closest][1].n_nodeID and connection[3] == self.ivos[closest][1].n_index:
                                if not(self.ivos[closest][1].n_node.Input[self.ivos[closest][1].n_index][3]):
                                    valid = False
                        if valid:
                            # form a connection
                            connection = [
                                self.ivos[self.previousInteracting][1].n_nodeID,
                                self.ivos[self.previousInteracting][1].n_index,
                                self.ivos[closest][1].n_nodeID,
                                self.ivos[closest][1].n_index
                            ]
                            self.nodeConnections.append(connection)

                            id = str(uuid.uuid4())
                            self.nodesConnectionData.append([id, self.ivos[self.previousInteracting][1].n_nodeID, self.ivos[self.previousInteracting][1].n_index])
                            self.ivos[id] = ["w", VisualNodeConnection(
                                "connection",
                                self.ivos[self.ivos[self.previousInteracting][1].n_nodeID][1],
                                connection[1],
                                self.ivos[self.ivos[closest][1].n_nodeID][1],
                                connection[3])
                            ]
                            outputs = self.nodes[connection[0]].Output
                            getter = outputs[connection[1]][2]
                            newInputs = self.nodes[connection[2]].get()
                            newInputs[connection[3]] = getter(self.nodes[connection[0]])
                            self.nodes[connection[2]].set(*newInputs)
                            self.updateAllNodes()
                        else: pass # not valid (taken)
                    else: pass # not valid (wrong type)
                else:
                    for connection in self.nodeConnections:
                        if connection[0] == self.ivos[self.previousInteracting][1].n_nodeID and connection[1] == self.ivos[self.previousInteracting][1].n_index:
                            self.nodeConnections.remove(connection)
                            newInputs = self.nodes[connection[2]].get()
                            newInputs[connection[3]] = None
                            self.nodes[connection[2]].set(*newInputs)
                    for connection in self.nodesConnectionData:
                        if connection[1] == self.ivos[self.previousInteracting][1].n_nodeID and connection[2] == self.ivos[self.previousInteracting][1].n_index:
                            self.ivos.pop(connection[0])
                            self.nodesConnectionData.remove(connection)
                    self.updateAllNodes()
                self.ivos[self.previousInteracting][1].out_connectionRequest = None
        # node updating logic 
        # TO-DO: optimize
        if self.ivos[self.previousInteracting][1].type == "node textbox" and self.interacting != self.previousInteracting:
            self.updateAllNodes()

    def summonNode(self, node:Node, coord:tuple|list):
        id = str(uuid.uuid4())
        self.nodes[id] = node
        self.nodeIDs = list(self.nodes.keys())

        self.ivos[id] = ["w", VisualNode("test", coord, self.nodes[id])]
        
        for i in range(len(node.Input)):
            name = f"{id} - in - {i}"
            self.ivos[name] = ["w", NodeConnectionPoint(name, id, self.ivos[id][1], i, True)]
            self.nodeConnectors.append(name)
        for i in range(len(node.Output)):
            name = f"{id} - out - {i}"
            self.ivos[name] = ["w", NodeConnectionPoint(name, id, self.ivos[id][1], i, False)]
            self.nodeConnectors.append(name)
        for i in range(len(node.Display)):
            if node.Display[i][1]:
                name = f"{id} - display - {node.Display[i][0]}"
                self.ivos[name] = ["w",NodeEditableTextBoxVisualObject(name, self.ivos[id][1], i, "")]

    def updateAllNodes(self):
        for nodeID in self.nodeIDs:
            self.ivos[nodeID][1].node.update()
            # TO-DO: optimize



    def scheduleSectionUpdate(self, section):
        if not(section in self.scheduledSectionUpdate):
            self.scheduledSectionUpdate.append(section)
    
    def keyConversion(key):
        if key in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789":
            return ord(key)
        else:
            if key=="space":    return ord(" ")
            if key=="slash":    return ord("/")
            if key=="asterisk": return ord("*")
            if key=="equal":    return ord("=")
            if key=="at":       return ord("@")
            if key=="minus":    return ord("-")
            if key=="colon":    return ord(":")
            if key=="BackSpace":return -1
        return None