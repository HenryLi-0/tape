'''
Settings

Here are the parts:
- Calculation
- Visuals
- Saving
'''


'''Calculation'''
PATH_FLOAT_ACCURACY = 3 #This is how many digits after the decimal point the intersection calculator will save for

'''Visuals'''
INTERFACE_FPS = 60 #The interface window will be called every 1/INTERFACE_FPS seconds
TICK_MS = round((1/INTERFACE_FPS)*1000)

'''Saving'''

'''Constants - Please Do Not Change'''
from PIL import Image
import os
PLACEHOLDER_IMAGE = Image.open(os.path.join("resources", "placeholder.png")).convert("RGBA")
PLACEHOLDER_IMAGE2 = Image.open(os.path.join("resources", "placeholder2.png")).convert("RGBA")