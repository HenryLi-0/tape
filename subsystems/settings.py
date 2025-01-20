'''This file contains modifiable settings!'''

class Setting:
    def __init__(self, valid, value, dangerous = False, hidden = False):
        self.valid = valid
        self.value = value
        self.dangerous = dangerous
        self.hidden = hidden
    def set(self, value):
        if type(value) in self.valid:
            self.value = value
    def get(self):
        return self.value

'''Animation'''
# Defines the width of the animation.
ANIMATION_WIDTH  = Setting([int], 1920)
# Defines the height of the animation.
ANIMATION_HEIGHT = Setting([int], 1080)
# Animation time. Used for in code to control the animation's time.
ANIMATION_TIME = Setting([int], 0, hidden = True)

'''Nodes'''
# The RGBA values for color of the text of normal inputs and outputs 
NODE_IO_NORMAL_RGBA = Setting([tuple], (255,255,255,255), hidden = True)
# The RGBA values for color of the text of uncapped inputs 
NODE_IO_UNCAPPED_RGBA = Setting([tuple], (190,0,250,255), hidden = True)
# The RGBA values for background color of input and output text
NODE_IO_BACKGROUND_RGBA = Setting([tuple], (0,0,0,150), hidden = True)
# Node width (does not include outlines)
NODE_WIDTH = Setting([int], 120, hidden = True)
# Node section height
NODE_SECTION_HEIGHT = Setting([int], 30, hidden = True)
# Node section divider height
NODE_SECTION_DIVIDER_HEIGHT = Setting([int], 3, hidden = True)
