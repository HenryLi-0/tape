'''This file contains modifiable settings!'''

SETTINGS = {
    "ANIMATION_WIDTH" : [[int], 1920],
    "ANIMATION_HEIGHT": [[int], 1080],
}

def setSetting(key, value):
    if (key in SETTINGS) and (type(value) in SETTINGS[key][0]):
        SETTINGS[key][1] = value

def getSetting(key):
    if key in SETTINGS:
        return SETTINGS[key]
    else:
        return None
