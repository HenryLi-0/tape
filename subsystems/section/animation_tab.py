from subsystems.section.section import *

class AnimationTab(Section):
    def render(state: State, im):
        '''Animation Interface:  `(  10,  10) to ( 478, 687)`: size `( 469, 678)``'''
        img = im.copy()
        rmx = state.mx - 10
        rmy = state.my - 10

        placeOver(img, displayText(f"hi i am animations", "m"), (20,20))
        placeOver(img, displayText(f"i will come in a future update", "m"), (20,50))
        placeOver(img, displayText(f"(probably the next one)", "m"), (20,80))

        for id in state.ivos:
            if state.ivos[id][0] == "a":
                state.ivos[id][1].tick(img, state.interacting==id or ((state.lastInteraction==id) and (abs(time.time() - state.ivos[id][1].lastInteraction) < LAST_INTERACTION_KEY_TIME)), state.interacting==id)

        Section.overlayCrosshair(state, img, rmx, rmy)

        return img    