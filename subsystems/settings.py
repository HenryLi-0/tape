'''This file contains modifiable settings!'''

class Setting:
    def __init__(self, valid, value):
        self.valid = valid
        self.value = value
    def set(self, value):
        if type(value) in self.valid:
            self.value = value
    def get(self):
        return self.value
    

ANIMATION_WIDTH  = Setting([int], 1920)
ANIMATION_HEIGHT = Setting([int], 1080)

