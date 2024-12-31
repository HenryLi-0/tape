from subsystems.section.section import *

class Workspace(Section):
    def render(state: State, im):
        '''Workspace Interface:  `( 485,  10) to (1355, 687)`: size `( 871, 678)`'''
        img = im.copy()
        rmx = state.mx - 485
        rmy = state.my - 10

        placeOver(img, displayText(f"FPS: {state.fps}", "m"), (20,20))

        for id in state.ivos:
            if state.ivos[id][0] == "w":
                state.ivos[id][1].tick(img, state.interacting==id or ((state.lastInteraction==id) and (abs(time.time() - state.ivos[id][1].lastInteraction) < LAST_INTERACTION_KEY_TIME)), state.interacting==id)

        Section.overlayCrosshair(state, img, rmx, rmy)

        return img    