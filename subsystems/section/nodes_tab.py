from subsystems.section.section import *

class NodesTab(Section):
    def render(state: State, im):
        '''Nodes Interface:      `(  10,  10) to ( 478, 687)`: size `( 469, 678)`'''
        img = im.copy()
        rmx = state.mx - 10
        rmy = state.my - 10

        choice = POINT_IDLE if random.random() > 0.5 else POINT_SELECTED
        for i in range(25):
            placeOver(img, choice, (math.cos((state.ticks/5+i/25))*250 + 325, math.sin((state.ticks/5+i/25))*250 + 327))
            placeOver(img, choice, (math.cos((state.ticks/2+i/25))*100 + 325, math.sin((state.ticks/2+i/25))*100 + 327))

        placeOver(img, displayText("IVO v2! - https://github.com/HenryLi-0/ivo", "s", colorTXT = (round(205+(50*-math.sin(state.ticks/25))),round(205+(50*math.sin(state.ticks/25))),round(205+(50*math.cos(state.ticks/25))),255)), (420,634))

        for id in state.ivos:
            if state.ivos[id][0] == "n":
                state.ivos[id][1].tick(img, state.interacting==id or ((state.lastInteraction==id) and (abs(time.time() - state.ivos[id][1].lastInteraction) < LAST_INTERACTION_KEY_TIME)), state.interacting==id)

        Section.overlayCrosshair(state, img, rmx, rmy)

        return img    
