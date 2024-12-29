'''This file is all about managing what the user sees'''

from settings import *
from PIL import ImageTk, Image
from tkinter import filedialog
import time, random, ast
from subsystems.render import *
from subsystems.fancy import *
from subsystems.simplefancy import *
from subsystems.visuals import *
from subsystems.point import *
from subsystems.bay import *
from subsystems.state import *

from subsystems.section.animation_tab   import AnimationTab
from subsystems.section.nodes_tab       import NodesTab
from subsystems.section.debug_tab       import DebugTab
from subsystems.section.export_tab      import ExportTab
from subsystems.section.settings_tab    import SettingsTab
# from subsystems.section.tabs            import Tabs
from subsystems.section.workspace       import Workspace

class Interface:
    def __init__(self):
        self.s = State()

    def tick(self,mx,my,mPressed,fps,keyQueue,mouseScroll):
        '''Entire Screen: `(0,0) to (1365,697)`: size `(1366,698)`'''
        self.s.tick(mx,my,mPressed,fps,keyQueue,mouseScroll)

        '''Copy State Interaction Info'''
        interacting = self.s.interacting

        '''Keyboard'''
        self.s.risingKeyQueue = []
        for key in keyQueue:
            if not (key in self.s.previousKeyQueue):
                if key in KB_CONFIRM:
                    interacting = -998
                    break
                temp = State.keyConversion(key)
                if temp != None:
                    self.s.risingKeyQueue.append(temp)
        self.s.previousKeyQueue = keyQueue.copy()

        keybind = None
        if (interacting == -999 or interacting == -997) and (time.time() - self.s.keybindLastUpdate > KEYBIND_DIFFERENCE):
            if KB_CREATE(keyQueue):
                '''description'''
                self.s.keybindLastUpdate = time.time()
                print("example")
                keybind = "example"

        if self.s.currentKeybind[1] != keybind and keybind != None:
            keybind = [True, keybind]
        else:
            keybind = [False, keybind]
        self.s.currentKeybind = keybind

        '''Mouse Scroll'''
        self.s.mouseScroll = mouseScroll
        if abs(self.s.mouseScroll) > 0:
            if interacting == -999: interacting = -996
            if interacting == -996:
                print("scrolling!")
        else:
            if interacting == -996: interacting = -999
        pass

        '''Interacting With...'''
        self.s.previousInteracting = interacting
        previousInteracting = self.s.previousInteracting
        if not(self.s.mPressed) and len(keyQueue) == 0:
            interacting = -999
        for key in keyQueue:
            if key in KB_ACTIVATE:
                interacting = self.s.lastInteraction

        if interacting == -999 and self.s.mPressed and self.s.mRising:
            processed = False
            for id in self.s.ivos:
                for section in SECTIONS:
                    if self.s.ivos[id][0] == section:
                        if self.s.ivos[id][1].getInteractable(self.s.mx - SECTIONS_DATA[section][0][0], self.s.my - SECTIONS_DATA[section][0][1]):
                            interacting = id
                            processed = True
                            break
                if processed: break
        if not(interacting in SYS_IVOS):
            section = self.s.ivos[interacting][0]
            self.s.ivos[interacting][1].updatePos(self.s.mx - SECTIONS_DATA[section][0][0], self.s.my - SECTIONS_DATA[section][0][1])
            self.s.ivos[interacting][1].keepInFrame(SECTIONS_DATA[section][3][0],SECTIONS_DATA[section][3][1],SECTIONS_DATA[section][4][0],SECTIONS_DATA[section][4][1])

        if not(interacting in SYS_IVOS):
            self.s.lastInteraction = interacting
        
        if len(keyQueue) > 0:
            self.s.ivos[self.s.lastInteraction][1].keyAction(self.s.risingKeyQueue)

        '''Update State Interaction Info'''
        self.s.interacting = interacting
        self.s.previousInteracting = previousInteracting

        '''Schedule Section Updates'''
        if not(self.s.interacting in SYS_IVOS):
            self.s.scheduleSectionUpdate(self.s.ivos[self.s.interacting][0])
        self.s.scheduleSectionUpdate("a")
        self.s.scheduleSectionUpdate("n")
        self.s.scheduleSectionUpdate("d")
        self.s.scheduleSectionUpdate("e")
        self.s.scheduleSectionUpdate("s")
        # self.s.scheduleSectionUpdate("t")
        self.s.scheduleSectionUpdate("w")

        '''Crosshair'''
        if SHOW_CROSSHAIR:
            for section in SECTIONS:
                if self.s.mouseInSection(section) or self.s.mouseWasInSection(section):
                    self.s.scheduleSectionUpdate(section)



    def processNone(self, im):
        return im
        # placeOver(img, displayText(f"FPS: {self.fps}", "m"), (55,15))
        # placeOver(img, displayText(f"Relative (animation) Mouse Position: ({self.mx-23}, {self.my-36})", "m"), (455,55))
        # placeOver(img, displayText(f"Mouse Pressed: {self.mPressed}", "m", colorTXT = (0,255,0,255) if self.mPressed else (255,0,0,255)), (55,55))
        # placeOver(img, displayText(f"Rising Edge: {self.mRising}", "m", colorTXT = (0,255,0,255) if self.mRising else (255,0,0,255)), (55,95))
        # placeOver(img, displayText(f"Interacting With Element: {self.interacting}", "m"), (455,15))
        # placeOver(img, displayText(f"stringKeyQueue: {self.stringKeyQueue}", "m"), (455,95))

    def processAnimationTab(self, im):
        return AnimationTab.render(self.s, im)
    
    def processNodesTab(self, im):
        return NodesTab.render(self.s, im)
    
    def processDebugTab(self, im):
        return DebugTab.render(self.s, im)
    
    def processExportTab(self, im):
        return ExportTab.render(self.s, im)
    
    def processSettingsTab(self, im):
        return SettingsTab.render(self.s, im)
    
    # def processTabs(self, im):
    #     return Tabs.render(self.s, im)

    def processWorkspace(self, im):
        return Workspace.render(self.s, im)


    def renderGIF(self):
        pass
        # path = filedialog.asksaveasfilename(initialdir=PATH_SAVE_DEFAULT, defaultextension=".gif", filetypes=[("GIF", "*.gif")])
        # if path != "":
        #     farthest = 0
        #     for sprite in self.sprites:
        #         for prop in ["c","r","a","s","t","b","w"]:
        #             data = sprite.getData(prop)
        #             for i in range(round(len(data)/3)):
        #                 if data[i*3] > farthest: farthest = data[i*3]
        #     bg = generateColorBox((903,507), (0,0,0,255))
        #     images = []
        #     for i in range(math.ceil(farthest * RENDER_FPS)):
        #         img = bg.copy()
        #         for sprite in self.sprites:
        #             frame = sprite.getFullStateAt(i/RENDER_FPS)
        #             placeOver(img, readImgSingleFullState(frame, self.cache.getImage(sprite.imageUUIDs[frame[1]]), True), (frame[0][0],frame[0][1]), True)
        #         images.append(Image.fromarray(img))  
        #     images[0].save(path, format='gif', append_images=images[1:], save_all=True, duration=1000/RENDER_FPS, loop=0)
        
    def renderMP4(self):
        pass
        # path = filedialog.asksaveasfilename(initialdir=PATH_SAVE_DEFAULT, defaultextension=".mp4", filetypes=[("MP4", "*.mp4")])
        # if path != "":
        #     import cv2
        #     farthest = 0
        #     for sprite in self.sprites:
        #         for prop in ["c","r","a","s","t","b","w"]:
        #             data = sprite.getData(prop)
        #             for i in range(round(len(data)/3)):
        #                 if data[i*3] > farthest: farthest = data[i*3]
        #     bg = generateColorBox((903,507), (0,0,0,255))
        #     y, x = bg.shape[:2]
        #     video = cv2.VideoWriter(path, cv2.VideoWriter_fourcc(*'mp4v'), RENDER_FPS, (x, y))
        #     for i in range(math.ceil(farthest * RENDER_FPS)):
        #         img = bg.copy()
        #         for sprite in self.sprites:
        #             frame = sprite.getFullStateAt(i/RENDER_FPS)
        #             placeOver(img, readImgSingleFullState(frame, self.cache.getImage(sprite.imageUUIDs[frame[1]]), True), (frame[0][0],frame[0][1]), True)
        #         video.write(cv2.cvtColor(img[:,:,:3], cv2.COLOR_RGB2BGR))
        #     video.release()    


    def saveState(self):
        return self.s

    def close(self):
        self.s = State()
        pass
