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
KB_IGNORE   = ["Win_L"]                                                                     # Keys to ignore
KB_CONFIRM  = ["Return", "Control_L"]                                                       # Keys to confirm
KB_ACTIVATE = ["space", "Return"]                                                           # Keys to activate/trigger
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
from subsystems.render import *

# Version
VERSION = "v1.0.0"
SYS_IVOS = [-999,-998,-997,-996]

ROTATE_AROUND_ORIGIN = lambda x,y,d: [(x/abs(x))*math.cos(math.atan(y/x)+(d*math.pi/50))*math.sqrt(x*x+y*y), (x/abs(x))*math.sin(math.atan(y/x)+(d*math.pi/50))*math.sqrt(x*x+y*y)]

# Sections
'''
- Example A Area: `(  22,  22) to ( 671, 675)` : size `( 650, 654)`
- Example B Area: `( 694,  22) to (1343, 675)` : size `( 650, 654)`

Region ID : Top Left, Bottom Right, Size, Keep In Relative Top Left, Keep In Relative Bottom Right
'''
SECTIONS_DATA = {
    " ": [(   0,   0),(1366, 698),(1366, 698),(   0,   0),(1366, 698)],
    "a": [(  22,  22),( 671, 675),( 650, 654),(   0,   0),( 650, 654)],
    "b": [( 694,  22),(1343, 675),( 650, 654),(   0,   0),( 650, 654)],
}
FULL_BACKGROUND = setBrightnessEffect(getImageRGBAFromPath(os.path.join("resources", "backgrounds", "sample_full_background.png")), 10)
SECTIONS_FRAME_INSTRUCTIONS = {
    " ": [[FULL_BACKGROUND, (0,0)]],
    "a": generateThemedBorderRectangleInstructions(( 650, 654), hexColorToRGBA(FRAME_COLOR), setBrightnessEffect(FULL_BACKGROUND,10), ( -22,-22)),
    "b": generateThemedBorderRectangleInstructions(( 650, 654), hexColorToRGBA(FRAME_COLOR), setBrightnessEffect(FULL_BACKGROUND,10), (-694,-22)),
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
FONTS_ALL = ["Comfortaa-Medium.ttf", "Orbitron-VariableFont_wght.ttf", "Tiny5-Regular.ttf", "TurretRoad-Medium.ttf", "ZenDots-Regular.ttf"]
FONT_PATH = os.path.join("resources", "fonts", FONTS_ALL[0])
FONT_LARGE = ImageFont.truetype(FONT_PATH, 24)
FONT_MEDIUM = ImageFont.truetype(FONT_PATH, 15)
FONT_SMALL_MEDIUM = ImageFont.truetype(FONT_PATH, 12)
FONT_SMALL = ImageFont.truetype(FONT_PATH, 10)
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
FRAME_TIMELINE_INSTRUCTIONS  = generateSpecificThemedBorderRectangleInstructions("timeline", FRAME_COLOR_RGBA)
FRAME_EDITOR_INSTRUCTIONS    = generateThemedBorderRectangleInstructions(( 388, 507), FRAME_COLOR_RGBA)
FRAME_EDITOR_V_INSTRUCTIONS  = generateSpecificThemedBorderRectangleInstructions(  "editor", FRAME_COLOR_RGBA)
FRAME_OPTIONS_INSTRUCTIONS   = generateSpecificThemedBorderRectangleInstructions( "options", FRAME_COLOR_RGBA)
FRAME_TIMELINE_READER_ARRAY = generateColorBox((3,117), SELECTED_COLOR_RGBA)
FRAME_EDITOR_VISUALS_GRAPH_ARRAY = generateSpecificThemedBorderRectangleInstructions( "graph", SELECTED_COLOR_RGBA)
FRAME_EDITOR_VISUALS_GRAPH_BAR_ARRAY = generateColorBox((3,236), FRAME_COLOR_RGBA)
FRAME_OPTIONS_BUTTON_ON_ARRAY  = generateInwardsBorderBox((120, 59), 3, SELECTED_COLOR_RGBA, BACKGROUND_COLOR_RGBA)
FRAME_OPTIONS_BUTTON_OFF_ARRAY = generateInwardsBorderBox((120, 59), 3,    FRAME_COLOR_RGBA, BACKGROUND_COLOR_RGBA)

GEAR = Image.open(os.path.join("resources", "gear.png")).convert("RGBA")
GEAR_ARRAY = numpy.array(GEAR)
PLAY_BUTTON = Image.open(os.path.join("resources", "play.png")).convert("RGBA")
PLAY_BUTTON_ARRAY = numpy.array(PLAY_BUTTON)
PAUSE_BUTTON = Image.open(os.path.join("resources", "pause.png")).convert("RGBA")
PAUSE_BUTTON_ARRAY = numpy.array(PAUSE_BUTTON)

# Cursors

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
