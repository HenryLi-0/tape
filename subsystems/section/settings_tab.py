from subsystems.section.section import *

class SettingsTab(Section):
    def render(state: State, im):
        '''Settings Interface:   `(  10,  10) to ( 478, 687)`: size `( 469, 678)`'''
        img = im.copy()
        rmx = state.mx - 10
        rmy = state.my - 10

        placeOver(img, displayText(f"hi i am settings", "m"), (20,20))

        for id in state.ivos:
            if state.ivos[id][0] == "s":
                state.ivos[id][1].tick(img, state.interacting==id or ((state.lastInteraction==id) and (abs(time.time() - state.ivos[id][1].lastInteraction) < LAST_INTERACTION_KEY_TIME)), state.interacting==id)

        Section.overlayCrosshair(state, img, rmx, rmy)

        return img    