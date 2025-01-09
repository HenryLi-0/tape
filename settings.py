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
FLOAT_ACCURACY = 3 #This is how many digits after the decimal point some calculations will save for
RENDER_FPS = 30 #This is the rendering FPS, also used for steps per second in path calculations

'''Visuals'''
INTERFACE_FPS = 60 # The interface window will be called every 1/INTERFACE_FPS seconds
FPS_DAMPENING = 1 # The number of seconds between FPS calculations
TICK_MS = 1 # Extra delay between frames, must be 1 or greater
OCCASIONAL_TICK_MS = 5000 # Should keep above 1 second, as it runs processes that do not need updates every tick

SHOW_CROSSHAIR = False # Shows a crosshair for the mouse's position
LAST_INTERACTION_KEY_TIME = 1 # Amount of seconds for last interaction to be active after key activation

hexColorToRGBA = lambda hexcolor: tuple(int(hexcolor[i:i+2], 16) for i in (1, 3, 5)) + (255,)

BACKGROUND_COLOR = "#241530" #Background color
FRAME_COLOR = "#381f4d" #Borders and Frame color
SELECTED_COLOR = "#9e6cc9" #Selected Element color
TIMELINE_COLOR = "#6d3999" #Timeline color

BACKGROUND_COLOR_RGBA       = hexColorToRGBA(BACKGROUND_COLOR      )
FRAME_COLOR_RGBA            = hexColorToRGBA(FRAME_COLOR           )
SELECTED_COLOR_RGBA         = hexColorToRGBA(SELECTED_COLOR        )
TIMELINE_COLOR_RGBA         = hexColorToRGBA(TIMELINE_COLOR        )

'''Saving'''
import os, time
PATH_SAVE_DEFAULT = os.path.join("tapes")

FORMAT_TIME = lambda x: time.strftime("%I:%M:%S %p %m/%d/%Y", time.localtime(x))
DEFAULT_PROJECT_NAME = "Untitled Project"

'''Keybinds'''
KEYBIND_DIFFERENCE = 0.2
KB_IGNORE       = ["Win_L"]                                                                             # Keys to ignore
KB_CONFIRM      = ["Return", "Alt_L"]                                                                   # Keys to confirm
KB_ACTIVATE     = ["space", "Return"]                                                                   # Keys to activate/trigger
KB_TAB_ANIMATION= lambda keys: (len(keys) == 2) and ("Control_L" in keys) and ("1" in keys)
KB_TAB_NODES    = lambda keys: (len(keys) == 2) and ("Control_L" in keys) and ("2" in keys)
KB_TAB_DEBUG    = lambda keys: (len(keys) == 2) and ("Control_L" in keys) and ("3" in keys)
KB_TAB_EXPORT   = lambda keys: (len(keys) == 2) and ("Control_L" in keys) and ("4" in keys)
KB_TAB_SETTINGS = lambda keys: (len(keys) == 2) and ("Control_L" in keys) and ("5" in keys)
KB_WS_NAV_N     = lambda keys: (len(keys) == 1) and ("Up" in keys)
KB_WS_NAV_NE    = lambda keys: (len(keys) == 2) and ("Up" in keys) and ("Right" in keys)
KB_WS_NAV_E     = lambda keys: (len(keys) == 1) and ("Right" in keys)
KB_WS_NAV_SE    = lambda keys: (len(keys) == 2) and ("Right" in keys) and ("Down" in keys)
KB_WS_NAV_S     = lambda keys: (len(keys) == 1) and ("Down" in keys)
KB_WS_NAV_SW    = lambda keys: (len(keys) == 2) and ("Down" in keys) and ("Left" in keys)
KB_WS_NAV_W     = lambda keys: (len(keys) == 1) and ("Left" in keys)
KB_WS_NAV_NW    = lambda keys: (len(keys) == 2) and ("Left" in keys) and ("Up" in keys)

'''Constants - DO NOT CHANGE!!!'''
'''Do not change these constants. Some are probably important. Some are used for testing purposes. 
   Editing certain constants will break things! You have been warned!'''
from PIL import Image, ImageFont
import numpy
from subsystems.simplefancy import *
from subsystems.render import *

# Version
VERSION = "pre-v2.0.0"
SYS_IVOS = [-999,-998,-997,-996]

ROTATE_AROUND_ORIGIN = lambda x,y,d: [(x/abs(x))*math.cos(math.atan(y/x)+(d*math.pi/50))*math.sqrt(x*x+y*y), (x/abs(x))*math.sin(math.atan(y/x)+(d*math.pi/50))*math.sqrt(x*x+y*y)]

# Sections
'''
- Animation Interface:  `(  10,  10) to ( 478, 643)`: size `( 469, 634)`
- Nodes Interface:      `(  10,  10) to ( 478, 643)`: size `( 469, 634)`
- Debug Interface:      `(  10,  10) to ( 478, 643)`: size `( 469, 634)`
- Export Interface:     `(  10,  10) to ( 478, 643)`: size `( 469, 634)`
- Settings Interface:   `(  10,  10) to ( 478, 643)`: size `( 469, 634)`
- Tabs Interface:       `(  10, 650) to ( 478, 687)`: size `( 469,  38)`
- Workspace Interface:  `( 485,  10) to (1355, 687)`: size `( 871, 678)`
- Entire Screen:        `(  0,    0) to (1365, 697)`: size `(1366, 698)`

Region ID : Top Left, Bottom Right, Size, Keep In Relative Top Left, Keep In Relative Bottom Right
'''
SECTIONS_DATA = {
    " ": [(   0,   0),(1366, 698),(1366, 698),(   0,   0),(1366, 698)],
    "a": [(  10,  10),( 478, 643),( 469, 634),(   0,   0),( 469, 634)],
    "n": [(  10,  10),( 478, 643),( 469, 634),(   0,   0),( 469, 634)],
    "d": [(  10,  10),( 478, 643),( 469, 634),(   0,   0),( 469, 634)],
    "e": [(  10,  10),( 478, 643),( 469, 634),(   0,   0),( 469, 634)],
    "s": [(  10,  10),( 478, 643),( 469, 634),(   0,   0),( 469, 634)],
    "t": [(  10, 650),( 478, 687),( 469,  38),(   0,   0),( 469,  38)],
    "w": [( 485,  10),(1355, 687),( 871, 678),(   0,   0),( 871, 678)],
}
FULL_BACKGROUND = setBrightnessEffect(getImageRGBAFromPath(os.path.join("resources", "loading.png")), -10)
SECTIONS_FRAME_INSTRUCTIONS = {
    " ": [[FULL_BACKGROUND, (0,0)]],
    "a": generateThemedBorderRectangleInstructions(( 469, 678), hexColorToRGBA(FRAME_COLOR), setBrightnessEffect(FULL_BACKGROUND,-25),(  -10,  -10)),
    "n": generateThemedBorderRectangleInstructions(( 469, 678), hexColorToRGBA(FRAME_COLOR), setBrightnessEffect(FULL_BACKGROUND,-25),(  -10,  -10)),
    "d": generateThemedBorderRectangleInstructions(( 469, 678), hexColorToRGBA(FRAME_COLOR), setBrightnessEffect(FULL_BACKGROUND,-25),(  -10,  -10)),
    "e": generateThemedBorderRectangleInstructions(( 469, 678), hexColorToRGBA(FRAME_COLOR), setBrightnessEffect(FULL_BACKGROUND,-25),(  -10,  -10)),
    "s": generateThemedBorderRectangleInstructions(( 469, 678), hexColorToRGBA(FRAME_COLOR), setBrightnessEffect(FULL_BACKGROUND,-25),(  -10,  -10)),
    "t": generateThemedBorderRectangleInstructions(( 469,  38), hexColorToRGBA(FRAME_COLOR), setBrightnessEffect(FULL_BACKGROUND,-25),(  -10, -650)),
    "w": generateThemedBorderRectangleInstructions(( 871, 678), hexColorToRGBA(FRAME_COLOR), setBrightnessEffect(FULL_BACKGROUND,-25),( -485,  -10)),
}
SECTIONS = list(SECTIONS_DATA.keys())

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
EMPTY_IMAGE = Image.fromarray(numpy.zeros((1, 1, 4), dtype=numpy.uint8), "RGBA")
EMPTY_IMAGE_ARRAY = numpy.array(EMPTY_IMAGE)

# Fonts
FONTS_ALL = ["Comfortaa-Medium.ttf", "Orbitron-VariableFont_wght.ttf", "Tiny5-Regular.ttf"]
FONT_PATH = os.path.join("resources", "fonts", FONTS_ALL[0])
FONT_LARGE = ImageFont.truetype(FONT_PATH, 24)
FONT_MEDIUM = ImageFont.truetype(FONT_PATH, 15)
FONT_SMALL_MEDIUM = ImageFont.truetype(FONT_PATH, 12)
FONT_SMALL = ImageFont.truetype(FONT_PATH, 10)
EDITOR_SPACING = lambda x: x*20+15


# Cursors
CURSOR_ARROW =  getImageRGBAFromPath(os.path.join("resources", "cursor_arrow.png"))
CURSOR_SELECT = getImageRGBAFromPath(os.path.join("resources", "cursor_select.png"))

ORB_IDLE =                  getImageRGBAFromPath(os.path.join("resources", "orb_idle.png"))
ORB_SELECTED =              getImageRGBAFromPath(os.path.join("resources", "orb_selected.png"))
POINT_IDLE =                getImageRGBAFromPath(os.path.join("resources", "point_idle.png"))
POINT_SELECTED =            getImageRGBAFromPath(os.path.join("resources", "point_selected.png"))
RECTANGULAR_RED_BUTTON =    getImageRGBAFromPath(os.path.join("resources", "rectangular_red_button.png"))
RECTANGULAR_GREEN_BUTTON =  getImageRGBAFromPath(os.path.join("resources", "rectangular_green_button.png"))

# Icons
GEAR =                  getImageRGBAFromPath(os.path.join("resources", "icon", "gear.png"))
PLAY_BUTTON =           getImageRGBAFromPath(os.path.join("resources", "icon", "play.png"))
PAUSE_BUTTON =          getImageRGBAFromPath(os.path.join("resources", "icon", "pause.png"))
UP_ARROW =              getImageRGBAFromPath(os.path.join("resources", "up_arrow.png"))
PATH_POINT_IDLE =       getImageRGBAFromPath(os.path.join("resources", "path_point_idle.png"))
PATH_POINT_SELECTED =   getImageRGBAFromPath(os.path.join("resources", "path_point_selected.png"))
PLUS_SIGN =             getImageRGBAFromPath(os.path.join("resources", "icon", "plus.png"))
TRASHCAN =              getImageRGBAFromPath(os.path.join("resources", "icon", "trashcan.png"))
IMPORT =                getImageRGBAFromPath(os.path.join("resources", "icon", "import.png"))
SAVE_ICON =             getImageRGBAFromPath(os.path.join("resources", "icon", "save.png"))
LOAD_ICON =             getImageRGBAFromPath(os.path.join("resources", "icon", "load.png"))
RENDER_GIF_ICON =       getImageRGBAFromPath(os.path.join("resources", "icon", "render_gif.png"))
RENDER_MP4_ICON =       getImageRGBAFromPath(os.path.join("resources", "icon", "render_mp4.png"))

# Tab Icons (Templates)
ANIMATION_TAB =    getImageRGBAFromPath(os.path.join("resources", "icon", "animation_tab.png"))
NODES_TAB =        getImageRGBAFromPath(os.path.join("resources", "icon", "nodes_tab.png"))
DEBUG_TAB =        getImageRGBAFromPath(os.path.join("resources", "icon", "debug_tab.png"))
EXPORT_TAB =       getImageRGBAFromPath(os.path.join("resources", "icon", "export_tab.png"))
SETTINGS_TAB =     getImageRGBAFromPath(os.path.join("resources", "icon", "settings_tab.png"))