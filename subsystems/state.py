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
        self.nodes = {
            # "aaa" : Random(),
            # "bbb" : Number(100)
        }
        # self.nodeConnections = [["bbb", 0, "aaa", 0]]
        self.nodesIDs = list(self.nodes.keys())
        self.nodeConnections = []
        self.nodeConnectors = []

        '''TEMPORARY TESTING'''
        # for id in self.nodesIDs:
        #     self.ivos[id] = ["w", VisualNode("test", (random.randint(0,500),random.randint(0,500)), self.nodes[id])]
        # self.ivos["test"] = ["w", VisualNodeConnection("test", self.ivos["bbb"][1], 0, self.ivos["aaa"][1], 0)]
        
        # for connection in self.nodeConnections:
        #     outputs = self.nodes[connection[0]].Output
        #     getter = outputs[connection[1]][2]
        #     inputs = self.nodes[connection[2]].Input
        #     newInputs = self.nodes[connection[2]].get()
        #     newInputs[connection[3]] = getter(self.nodes[connection[0]])
        #     self.nodes[connection[2]].set(*newInputs)
        
        # self.ivos["text"] = ["w",NodeEditableTextBoxVisualObject("test", self.ivos["bbb"][1], 0, "sus")]

        # self.ivos["a1"] = ["w",NodeConnectionPoint("test", "aaa", self.ivos["aaa"][1], 0,  True)]
        # self.ivos["a2"] = ["w",NodeConnectionPoint("test", "aaa", self.ivos["aaa"][1], 1,  True)]
        # self.ivos["a3"] = ["w",NodeConnectionPoint("test", "aaa", self.ivos["aaa"][1], 2,  True)]
        # self.ivos["b1"] = ["w",NodeConnectionPoint("test", "aaa", self.ivos["aaa"][1], 0, False)]
        # self.ivos["c1"] = ["w",NodeConnectionPoint("test", "bbb", self.ivos["bbb"][1], 0, False)]
        # self.nodeConnectors = ["a1", "a2", "a3", "b1", "c1"]

        self.summonNode(Number(), (0, 0))
        self.summonNode(Number(), (0, 100))
        self.summonNode(Boolean(), (0, 200))

        self.summonNode(Random(), (250, 0))


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
                here = self.ivos[self.previousInteracting][1].out_connectionRequest
                nodeSpace = []
                for connectorID in self.nodeConnectors:
                    if self.ivos[connectorID][1].n_input:
                        nodeSpace.append(distanceP(self.ivos[connectorID][1].positionO.getNodeSpacePosition(), here))
                    else:
                        nodeSpace.append(100)
                closest = self.nodeConnectors[nodeSpace.index(min(nodeSpace))]
                if distanceP(self.ivos[closest][1].positionO.getNodeSpacePosition(), here) < 25:
                    if self.ivos[self.previousInteracting][1].n_type in self.ivos[closest][1].n_type:
                        connection = [
                            self.ivos[self.previousInteracting][1].n_nodeID,
                            self.ivos[self.previousInteracting][1].n_index,
                            self.ivos[closest][1].n_nodeID,
                            self.ivos[closest][1].n_index
                        ]
                        self.nodeConnections.append(connection)
                        self.ivos[str(uuid.uuid4())] = ["w", VisualNodeConnection(
                            "test",
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
                    else: pass
                else:
                    print("clear")

                self.ivos[self.previousInteracting][1].out_connectionRequest = None

    def summonNode(self, node:Node, coord:tuple|list):
        id = str(uuid.uuid4())
        self.nodes[id] = node
        self.nodesIDs = list(self.nodes.keys())

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