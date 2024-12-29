from subsystems.section.section import *

class DebugTab(Section):
    def render(state: State, im):
        '''Debug Interface:      `(  10,  10) to ( 478, 687)`: size `( 469, 678)`'''
        img = im.copy()
        rmx = state.mx - 10
        rmy = state.my - 10

        placeOver(img, displayText(f"FPS: {state.fps}", "m"), (20,20))
        placeOver(img, displayText(f"Interacting With: {state.interacting}", "m"), (20,55))
        placeOver(img, displayText(f"Last Interaction: {state.lastInteraction}", "m"), (20,90))
        placeOver(img, displayText(f"length of IVO: {len(state.ivos)}", "m"), (200,20))
        placeOver(img, displayText(f"Mouse Pos: ({state.mx}, {state.my})", "m"), (200,55))
        placeOver(img, displayText(f"Mouse Press: {state.mPressed}", "m", colorTXT=(100,255,100,255) if state.mPressed else (255,100,100,255)), (200,90))
        placeOver(img, displayText(f"Key Queue: {state.risingKeyQueue}", "m"), (20,125))

        for id in state.ivos:
            if state.ivos[id][0] == "d":
                state.ivos[id][1].tick(img, state.interacting==id or ((state.lastInteraction==id) and (abs(time.time() - state.ivos[id][1].lastInteraction) < LAST_INTERACTION_KEY_TIME)), state.interacting==id)

        Section.overlayCrosshair(state, img, rmx, rmy)

        return img    