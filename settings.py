'''
Settings

Here are the parts:
- Calculation
- Visuals
- Saving
- Constants (Please do not change)
'''


'''Calculation'''
PATH_FLOAT_ACCURACY = 3 #This is how many digits after the decimal point the intersection calculator will save for

'''Visuals'''
INTERFACE_FPS = 60 #The interface window will be called every 1/INTERFACE_FPS seconds
TICK_MS = round((1/INTERFACE_FPS)*1000)
OCCASIONAL_TICK_MS = 3000 # Highly recommended to keep above 1 second, as it runs processes that do not need updates every tick

BACKGROUND_COLOR = "#241530" #Background color
FRAME_COLOR = "#381f4d" #Borders and Frame color
SELECTED_COLOR = "#9e6cc9" #Selected Element color
TIMELINE_COLOR = "#6d3999" #Timeline color

hexColorToRGB = lambda hexcolor: tuple(int(hexcolor[i:i+2], 16) for i in (1, 3, 5)) + (255,)

'''Saving'''

'''Constants - Do Not Change'''
'''Do not change these constants. Some are probably important. Some are used for testing purposes. 
   Editing certain constants will break things! You have been warned!'''
from PIL import Image, ImageFont
import os, numpy

# Imagery
LOADING_IMAGE = Image.open(os.path.join("resources", "loading.png")).convert("RGBA") # 1366x697, Solid, Loading Screen
LOADING_IMAGE_ARRAY = numpy.array(LOADING_IMAGE)
PLACEHOLDER_IMAGE = Image.open(os.path.join("resources", "placeholder.png")).convert("RGBA")    # 512x512, Solid, [black, white, grey]
PLACEHOLDER_IMAGE_ARRAY = numpy.array(PLACEHOLDER_IMAGE)
PLACEHOLDER_IMAGE_2 = Image.open(os.path.join("resources", "placeholder2.png")).convert("RGBA")  # 100x100, Transparent Background [black, white, grey]
PLACEHOLDER_IMAGE_2_ARRAY = numpy.array(PLACEHOLDER_IMAGE_2)
PLACEHOLDER_IMAGE_3 = Image.open(os.path.join("resources", "placeholder3.png")).convert("RGBA")  # 128x128, Solid Background [black, white, grey]
PLACEHOLDER_IMAGE_3_ARRAY = numpy.array(PLACEHOLDER_IMAGE_3)
PLACEHOLDER_IMAGE_4 = Image.open(os.path.join("resources", "placeholder4.png")).convert("RGBA")  # 16x16, Transparent Background [black, white]
PLACEHOLDER_IMAGE_4_ARRAY = numpy.array(PLACEHOLDER_IMAGE_4)
PLACEHOLDER_IMAGE_5 = Image.open(os.path.join("resources", "placeholder5.png")).convert("RGBA")  # 32x32, Solid Background [rainbow]
PLACEHOLDER_IMAGE_5_ARRAY = numpy.array(PLACEHOLDER_IMAGE_5)
MISSING_IMAGE = Image.open(os.path.join("resources", "missing.png")).convert("RGBA")
MISSING_IMAGE_ARRAY = numpy.array(MISSING_IMAGE)

# Fonts
FONT_LARGE = ImageFont.truetype(os.path.join("resources", "Comfortaa-Medium.ttf"), 32)
FONT_MEDIUM = ImageFont.truetype(os.path.join("resources", "Comfortaa-Medium.ttf"), 15)
FONT_SMALL = ImageFont.truetype(os.path.join("resources", "Comfortaa-Medium.ttf"), 10)

# Blank Interface Sections
'''
- Animation Interface: `(23,36) to (925,542)`: size `(903,507)`
- Timeline Interface: `(23,558) to (925,680)`: size `(903,123)`
- Editor Interface: `(953,36) to (1340,542)`: size `(388,507)`
- Options Interface: `(953,558) to (1340,680)`: size `(388,123)`
- Entire Screen: `(0,0) to (1365,697)`: size `(1366,698)`
'''

D_FRAME_ANIMATION_PATH = os.path.join("resources", "themed", "frame_animation.png")
D_FRAME_TIMELINE_PATH = os.path.join("resources", "themed", "frame_timeline.png")
D_FRAME_EDITOR_PATH = os.path.join("resources", "themed", "frame_editor.png")
D_FRAME_OPTIONS_PATH = os.path.join("resources", "themed", "frame_options.png")

FRAME_ANIMATION = Image.open(os.path.join("resources", "themed", "u_frame_animation.png")).convert("RGBA")
FRAME_ANIMATION_ARRAY = numpy.array(FRAME_ANIMATION)
FRAME_TIMELINE = Image.open(os.path.join("resources", "themed", "u_frame_timeline.png")).convert("RGBA")
FRAME_TIMELINE_ARRAY = numpy.array(FRAME_TIMELINE)
FRAME_EDITOR = Image.open(os.path.join("resources", "themed", "u_frame_editor.png")).convert("RGBA")
FRAME_EDITOR_ARRAY = numpy.array(FRAME_EDITOR)
FRAME_OPTIONS = Image.open(os.path.join("resources", "themed", "u_frame_options.png")).convert("RGBA")
FRAME_OPTIONS_ARRAY = numpy.array(FRAME_OPTIONS)    

CURSOR = Image.open(os.path.join("resources", "cursor.png")).convert("RGBA")
CURSOR_ARRAY = numpy.array(CURSOR)