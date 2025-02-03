from subsystems.section.section import *
from subsystems.node.node import NODES

class NodesTab(Section):
    def render(state: State, im):
        '''Nodes Interface:      `(  10,  10) to ( 478, 687)`: size `( 469, 678)`'''
        img = im.copy()
        rmx = state.mx - 10
        rmy = state.my - 10

        i = 0 
        for node in NODES:
            placeOver(img, displayText(node.__name__, "m"), (20,25 + i*30 - state.nodeListOffset))
            i += 1


        for id in state.ivos:
            if state.ivos[id][0] == "n":
                state.ivos[id][1].tick(img, state.interacting==id or ((state.lastInteraction==id) and (abs(time.time() - state.ivos[id][1].lastInteraction) < LAST_INTERACTION_KEY_TIME)), state.interacting==id)

        Section.overlayCrosshair(state, img, rmx, rmy)

        return img    
