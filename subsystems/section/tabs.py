from subsystems.section.section import *

class Tabs(Section):
    def render(state: State, im):
        '''Tabs Interface:       `(  10, 650) to ( 478, 687)`: size `( 469,  38)`'''
        img = im.copy()
        rmx = state.mx - 10
        rmy = state.my - 10

        placeOver(img, displayText(f"{state.ticks}", "m"), (400,10))

        for id in state.ivos:
            if state.ivos[id][0] == "t":
                state.ivos[id][1].tick(img, state.interacting==id or ((state.lastInteraction==id) and (abs(time.time() - state.ivos[id][1].lastInteraction) < LAST_INTERACTION_KEY_TIME)) or (state.ivos[id][1].name[0].lower() == state.tab), state.interacting==id)

        Section.overlayCrosshair(state, img, rmx, rmy)

        return img    