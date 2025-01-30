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

            -99 : ["w",ButtonVisualObject("sprites",(7,450),RECTANGULAR_RED_BUTTON,RECTANGULAR_GREEN_BUTTON)],
            -98 : ["w",ButtonVisualObject("visuals",(134,450),RECTANGULAR_RED_BUTTON,RECTANGULAR_GREEN_BUTTON)],
            -97 : ["w",ButtonVisualObject("project",(7,450),RECTANGULAR_RED_BUTTON,RECTANGULAR_GREEN_BUTTON)],
            -96 : ["w",IconVisualObject("Settings",(323,450), GEAR, (52,52))],
            -95 : ["w",OrbVisualObject("what",(323,450))],
            -94 : ["w",EditableTextBoxVisualObject("test", (50,50), "test")],

            -89 : ["t",IconVisualObject("Animation", (9,3), ANIMATION_TAB, outline = False)],
            -88 : ["t",IconVisualObject("Nodes", (49,3), NODES_TAB, outline = False)],
            -87 : ["t",IconVisualObject("Debug", (89,3), DEBUG_TAB, outline = False)],
            -86 : ["t",IconVisualObject("Export", (129,3), EXPORT_TAB, outline = False)],
            -85 : ["t",IconVisualObject("Settings", (169,3), SETTINGS_TAB, outline = False)],
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
            "aaa" : Random(),
            "bbb" : Number(100)
        }
        self.nodeConnections = [["bbb", "Value", "aaa", "Lower Limit"]]
        self.nodesIDs = list(self.nodes.keys())

        '''TEMPORARY TESTING'''
        for id in self.nodesIDs:
            self.ivos[id] = ["w", VisualNode("test", (random.randint(0,500),random.randint(0,500)), self.nodes[id])]
        self.ivos["test"] = ["w", VisualNodeConnection("test", self.ivos["bbb"][1], 0, self.ivos["aaa"][1], 0)]
        
        for connection in self.nodeConnections:
            outputs = self.nodes[connection[0]].Output
            getter = outputs[[x[0] for x in outputs].index(connection[1])][2]
            inputs = self.nodes[connection[2]].Input
            newInputs = self.nodes[connection[2]].get()
            newInputs[[x[0] for x in inputs].index(connection[3])] = getter(self.nodes[connection[0]])
            self.nodes[connection[2]].set(*newInputs)


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
        if self.interacting in [-89, -88, -87, -86, -85]:
            self.tab = self.ivos[self.interacting][1].name[0].lower()

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