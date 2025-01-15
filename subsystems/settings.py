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
    
# Defines the width of the animation.
ANIMATION_WIDTH  = Setting([int], 1920)
# Defines the height of the animation.
ANIMATION_HEIGHT = Setting([int], 1080)
# Animation time. Used for in code to control the animation's time.
ANIMATION_TIME = Setting([int], 0, hidden = True)
# The limit on how many nodes can connect for a node input set to uncapped nodes.
MAX_UNCAPPED_NODES_LIMIT = Setting([int], 64, dangerous = True)