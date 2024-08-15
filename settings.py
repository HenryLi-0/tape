'''
Settings

Here are the parts:
- Calculation
- Visuals
- Saving
- Keybinds
- Constants (Please do not change!)
'''


'''Calculation'''
PATH_FLOAT_ACCURACY = 3 #This is how many digits after the decimal point the intersection calculator will save for
RENDER_FPS = 30 #This is the rendering FPS, also used for steps per second in path calculations

'''Visuals'''
INTERFACE_FPS = 60 # The interface window will be called every 1/INTERFACE_FPS seconds
TICK_MS = 1 #round((1/INTERFACE_FPS)*1000)
OCCASIONAL_TICK_MS = 5000 # Highly recommended to keep above 1 second, as it runs processes that do not need updates every tick

KEYBIND_DIFFERENCE = 0.2 # Minimum allowed differance in time between keybinds

hexColorToRGBA = lambda hexcolor: tuple(int(hexcolor[i:i+2], 16) for i in (1, 3, 5)) + (255,)

BACKGROUND_COLOR = "#241530" #Background color
FRAME_COLOR = "#381f4d" #Borders and Frame color
SELECTED_COLOR = "#9e6cc9" #Selected Element color
TIMELINE_COLOR = "#6d3999" #Timeline color
SPECIAL_COLOR = "#ab570e" #Special color
SELECTED_SPECIAL_COLOR = "#db6d0d" #Selected special color

BACKGROUND_COLOR_RGBA       = hexColorToRGBA(BACKGROUND_COLOR      )
FRAME_COLOR_RGBA            = hexColorToRGBA(FRAME_COLOR           )
SELECTED_COLOR_RGBA         = hexColorToRGBA(SELECTED_COLOR        )
TIMELINE_COLOR_RGBA         = hexColorToRGBA(TIMELINE_COLOR        )
SPECIAL_COLOR_RGBA          = hexColorToRGBA(SPECIAL_COLOR         )
SELECTED_SPECIAL_COLOR_RGBA = hexColorToRGBA(SELECTED_SPECIAL_COLOR)

'''Saving'''
import os, time
PATH_SAVE_DEFAULT = os.path.join("tapes")
EXPORT_IMAGE_DATA = True
CLEAR_ON_OPEN = True

FORMAT_TIME = lambda x: time.strftime("%I:%M:%S %p %m/%d/%Y", time.localtime(x))
DEFAULT_PROJECT_NAME = "Untitled Project"

'''Keybinds'''
KB_IGNORE = ["Win_L"]
KB_EV_PROPERTY = {
    1 : "C",
    2 : "R",
    3 : "A",
    4 : "S",
    5 : "H",
    6 : "T",
    7 : "B",
    8 : "W"
}
KB_CREATE                = lambda keys: (len(keys) == 1) and ("A" in keys or "a" in keys)
KB_DELETE                = lambda keys: (len(keys) == 1) and ("S" in keys or "s" in keys)
KB_EV_LINEAR_CONNECTION  = lambda keys: (len(keys) == 1) and ("Q" in keys or "q" in keys)
KB_EV_SMOOTH_CONNECTION  = lambda keys: (len(keys) == 1) and ("W" in keys or "w" in keys)
KB_EV_OFFSET_LEFT        = lambda keys: (len(keys) == 1) and ("Z" in keys or "z" in keys)
KB_EV_OFFSET_RIGHT       = lambda keys: (len(keys) == 1) and ("X" in keys or "x" in keys)
KB_A_POINT_POSITION_EDIT = lambda keys: (len(keys) == 1) and ("D" in keys or "d" in keys)
KB_T_OFFSET_LEFT         = lambda keys: (len(keys) == 1) and ("Left"  in keys)
KB_T_OFFSET_RIGHT        = lambda keys: (len(keys) == 1) and ("Right" in keys)
KB_S_LIST_OFFSET_UP      = lambda keys: (len(keys) == 1) and ("Up"    in keys)
KB_S_LIST_OFFSET_DOWN    = lambda keys: (len(keys) == 1) and ("Down"  in keys)

'''Constants - DO NOT CHANGE!!!'''
'''Do not change these constants. Some are probably important. Some are used for testing purposes. 
   Editing certain constants will break things! You have been warned!'''
from PIL import Image, ImageFont
import numpy
from subsystems.simplefancy import *

# Version
VERSION = "v1.0.0"

# Imagery
LOADING_IMAGE = Image.open(os.path.join("resources", "loading.png")).convert("RGBA") # 1366x697, Solid, Loading Screen
LOADING_IMAGE_ARRAY = numpy.array(LOADING_IMAGE)
PLACEHOLDER_IMAGE = Image.open(os.path.join("resources", "placeholder", "placeholder.png")).convert("RGBA")    # 512x512, Solid, [black, white, grey]
PLACEHOLDER_IMAGE_ARRAY = numpy.array(PLACEHOLDER_IMAGE)
PLACEHOLDER_IMAGE_2 = Image.open(os.path.join("resources", "placeholder", "placeholder2.png")).convert("RGBA")  # 100x100, Transparent Background [black, white, grey]
PLACEHOLDER_IMAGE_2_ARRAY = numpy.array(PLACEHOLDER_IMAGE_2)
PLACEHOLDER_IMAGE_3 = Image.open(os.path.join("resources", "placeholder", "placeholder3.png")).convert("RGBA")  # 128x128, Solid Background [black, white, grey]
PLACEHOLDER_IMAGE_3_ARRAY = numpy.array(PLACEHOLDER_IMAGE_3)
PLACEHOLDER_IMAGE_4 = Image.open(os.path.join("resources", "placeholder", "placeholder4.png")).convert("RGBA")  # 16x16, Transparent Background [black, white]
PLACEHOLDER_IMAGE_4_ARRAY = numpy.array(PLACEHOLDER_IMAGE_4)
PLACEHOLDER_IMAGE_5 = Image.open(os.path.join("resources", "placeholder", "placeholder5.png")).convert("RGBA")  # 32x32, Solid Background [rainbow]
PLACEHOLDER_IMAGE_5_ARRAY = numpy.array(PLACEHOLDER_IMAGE_5)
MISSING_IMAGE_PATH = os.path.join("resources", "missing.png")
MISSING_IMAGE = Image.open(os.path.join("resources", "missing.png")).convert("RGBA")
MISSING_IMAGE_ARRAY = numpy.array(MISSING_IMAGE)

# Fonts
FONT_LARGE = ImageFont.truetype(os.path.join("resources", "Comfortaa-Medium.ttf"), 24)
FONT_MEDIUM = ImageFont.truetype(os.path.join("resources", "Comfortaa-Medium.ttf"), 15)
FONT_SMALL = ImageFont.truetype(os.path.join("resources", "Comfortaa-Medium.ttf"), 10)
EDITOR_SPACING = lambda x: x*20+15

# Blank Interface Sections
'''
- Animation Interface: `(23,36) to (925,542)`: size `(903,507)`
- Timeline Interface: `(23,558) to (925,680)`: size `(903,123)`
- Editor Interface: `(953,36) to (1340,542)`: size `(388,507)`
- Options Interface: `(953,558) to (1340,680)`: size `(388,123)`
- Entire Screen: `(0,0) to (1365,697)`: size `(1366,698)`
'''

FRAME_ANIMATION_INSTRUCTIONS = generateThemedBorderRectangleInstructions(( 903, 507), FRAME_COLOR_RGBA)
FRAME_TIMELINE_INSTRUCTIONS  = genereateSpecificThemedBorderRectangleInstructions("timeline", FRAME_COLOR_RGBA)
FRAME_EDITOR_INSTRUCTIONS    = generateThemedBorderRectangleInstructions(( 388, 507), FRAME_COLOR_RGBA)
FRAME_EDITOR_V_INSTRUCTIONS  = genereateSpecificThemedBorderRectangleInstructions(  "editor", FRAME_COLOR_RGBA)
FRAME_OPTIONS_INSTRUCTIONS   = genereateSpecificThemedBorderRectangleInstructions( "options", FRAME_COLOR_RGBA)
FRAME_TIMELINE_READER_ARRAY = generateColorBox((3,117), SELECTED_COLOR_RGBA)
FRAME_EDITOR_VISUALS_GRAPH_ARRAY = genereateSpecificThemedBorderRectangleInstructions( "graph", SELECTED_COLOR_RGBA)
FRAME_EDITOR_VISUALS_GRAPH_BAR_ARRAY = generateColorBox((3,236), FRAME_COLOR_RGBA)
FRAME_OPTIONS_BUTTON_ON_ARRAY  = generateInwardsBorderBox((120, 59), 3, SELECTED_COLOR_RGBA, BACKGROUND_COLOR_RGBA)
FRAME_OPTIONS_BUTTON_OFF_ARRAY = generateInwardsBorderBox((120, 59), 3,    FRAME_COLOR_RGBA, BACKGROUND_COLOR_RGBA)

GEAR = Image.open(os.path.join("resources", "gear.png")).convert("RGBA")
GEAR_ARRAY = numpy.array(GEAR)
PLAY_BUTTON = Image.open(os.path.join("resources", "play.png")).convert("RGBA")
PLAY_BUTTON_ARRAY = numpy.array(PLAY_BUTTON)
PAUSE_BUTTON = Image.open(os.path.join("resources", "pause.png")).convert("RGBA")
PAUSE_BUTTON_ARRAY = numpy.array(PAUSE_BUTTON)

CURSOR_ARROW = Image.open(os.path.join("resources", "cursor_arrow.png")).convert("RGBA")
CURSOR_ARROW_ARRAY = numpy.array(CURSOR_ARROW)
CURSOR_SELECT = Image.open(os.path.join("resources", "cursor_select.png")).convert("RGBA")
CURSOR_SELECT_ARRAY = numpy.array(CURSOR_SELECT)

ORB_IDLE = Image.open(os.path.join("resources", "orb_idle.png")).convert("RGBA")
ORB_IDLE_ARRAY = numpy.array(ORB_IDLE)
ORB_SELECTED = Image.open(os.path.join("resources", "orb_selected.png")).convert("RGBA")
ORB_SELECTED_ARRAY = numpy.array(ORB_SELECTED)
POINT_IDLE = Image.open(os.path.join("resources", "point_idle.png")).convert("RGBA")
POINT_IDLE_ARRAY = numpy.array(POINT_IDLE)
POINT_SELECTED = Image.open(os.path.join("resources", "point_selected.png")).convert("RGBA")
POINT_SELECTED_ARRAY = numpy.array(POINT_SELECTED)
RECTANGULAR_RED_BUTTON_ARRAY = numpy.array(Image.open(os.path.join("resources", "rectangular_red_button.png")).convert("RGBA"))
RECTANGULAR_GREEN_BUTTON_ARRAY = numpy.array(Image.open(os.path.join("resources", "rectangular_green_button.png")).convert("RGBA"))
UP_ARROW_ARRAY = numpy.array(Image.open(os.path.join("resources", "up_arrow.png")).convert("RGBA"))
PATH_POINT_IDLE_ARRAY = numpy.array(Image.open(os.path.join("resources", "path_point_idle.png")).convert("RGBA"))
PATH_POINT_SELECTED_ARRAY = numpy.array(Image.open(os.path.join("resources", "path_point_selected.png")).convert("RGBA"))
PLUS_SIGN_ARRAY = numpy.array(Image.open(os.path.join("resources", "plus.png")).convert("RGBA"))
TRASHCAN_ARRAY = numpy.array(Image.open(os.path.join("resources", "trashcan.png")).convert("RGBA"))
IMPORT_ARRAY = numpy.array(Image.open(os.path.join("resources", "import.png")).convert("RGBA"))
SAVE_ICON_ARRAY = numpy.array(Image.open(os.path.join("resources", "save.png")).convert("RGBA"))
LOAD_ICON_ARRAY = numpy.array(Image.open(os.path.join("resources", "load.png")).convert("RGBA"))
RENDER_GIF_ICON_ARRAY = numpy.array(Image.open(os.path.join("resources", "render_gif.png")).convert("RGBA"))
RENDER_MP4_ICON_ARRAY = numpy.array(Image.open(os.path.join("resources", "render_mp4.png")).convert("RGBA"))

PROPERTY_DISPLAY_NAMES = ["Coordinates","Rotational","Apperance","Size","Hue","Transparency","Brightness","Blur"]
