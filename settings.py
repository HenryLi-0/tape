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
TICK_MS = round((1/INTERFACE_FPS)*1000)
OCCASIONAL_TICK_MS = 5000 # Highly recommended to keep above 1 second, as it runs processes that do not need updates every tick

BACKGROUND_COLOR = "#241530" #Background color
FRAME_COLOR = "#381f4d" #Borders and Frame color
SELECTED_COLOR = "#9e6cc9" #Selected Element color
TIMELINE_COLOR = "#6d3999" #Timeline color
SPECIAL_COLOR = "#ab570e" #Special color
SELECTED_SPECIAL_COLOR = "#db6d0d" #Selected special color

hexColorToRGBA = lambda hexcolor: tuple(int(hexcolor[i:i+2], 16) for i in (1, 3, 5)) + (255,)

'''Saving'''
import os, time
PATH_SAVE_DEFAULT = os.path.join("tapes")
EXPORT_IMAGE_DATA = True
CLEAR_ON_OPEN = True

FORMAT_TIME = lambda x: time.strftime("%I:%M:%S %p %m/%d/%Y", time.localtime(x))
DEFAULT_PROJECT_NAME = "Untitled Project"

'''Keybinds'''
EDITOR_VISUAL_KEYBINDS = {
    1 : "C",
    2 : "R",
    3 : "A",
    4 : "S",
    5 : "H",
    6 : "T",
    7 : "B",
    8 : "W"
}
KB_EDITOR_VISUAL_LINEAR_CONNECTION = ["Q", "q"]
KB_EDITOR_VISUAL_SMOOTH_CONNECTION = ["W", "w"]
KB_CREATE = ["A", "a"]
KB_DELETE = ["S", "s"]
KB_EDITOR_VISUAL_OFFSET_LEFT = ["Z", "z"]
KB_EDITOR_VISUAL_OFFSET_RIGHT = ["X", "x"]
KB_TIMELINE_OFFSET_LEFT = ["Left"]
KB_TIMELINE_OFFSET_RIGHT = ["Right"]
KB_ANIMATION_POINT_POSITION_EDIT = ["D", "d"]
KB_SPRITE_LIST_OFFSET_UP = ["Up"]
KB_SPRITE_LIST_OFFSET_DOWN = ["Down"]

'''Constants - DO NOT CHANGE!!!'''
'''Do not change these constants. Some are probably important. Some are used for testing purposes. 
   Editing certain constants will break things! You have been warned!'''
from PIL import Image, ImageFont
import numpy

# Version
VERSION = "v0.0.1"

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

D_FRAME_ANIMATION_PATH = os.path.join("resources", "themed", "frame_animation.png")
D_FRAME_TIMELINE_PATH = os.path.join("resources", "themed", "frame_timeline.png")
D_FRAME_TIMELINE_READER_PATH = os.path.join("resources", "themed", "frame_timeline_reader.png")
D_FRAME_EDITOR_PATH = os.path.join("resources", "themed", "frame_editor.png")
D_FRAME_EDITOR_VISUALS_PATH = os.path.join("resources", "themed", "frame_editor_visuals.png")
D_FRAME_EDITOR_VISUALS_GRAPH_PATH = os.path.join("resources", "themed", "frame_editor_visuals_graph.png")
D_FRAME_EDITOR_VISUALS_GRAPH_BAR_PATH = os.path.join("resources", "themed", "frame_editor_visuals_graph_bar.png")
D_FRAME_OPTIONS_PATH = os.path.join("resources", "themed", "frame_options.png")
D_FRAME_OPTIONS_BUTTON_PATH = os.path.join("resources", "themed", "frame_options_button.png")

FRAME_ANIMATION = Image.open(os.path.join("resources", "themed", "u_frame_animation.png")).convert("RGBA")
FRAME_ANIMATION_ARRAY = numpy.array(FRAME_ANIMATION)
FRAME_TIMELINE = Image.open(os.path.join("resources", "themed", "u_frame_timeline.png")).convert("RGBA")
FRAME_TIMELINE_ARRAY = numpy.array(FRAME_TIMELINE)
FRAME_TIMELINE_READER = Image.open(os.path.join("resources", "themed", "u_frame_timeline_reader.png")).convert("RGBA")
FRAME_TIMELINE_READER_ARRAY = numpy.array(FRAME_TIMELINE_READER)
FRAME_EDITOR = Image.open(os.path.join("resources", "themed", "u_frame_editor.png")).convert("RGBA")
FRAME_EDITOR_ARRAY = numpy.array(FRAME_EDITOR)
FRAME_EDITOR_VISUALS = Image.open(os.path.join("resources", "themed", "u_frame_editor_visuals.png")).convert("RGBA")
FRAME_EDITOR_VISUALS_ARRAY = numpy.array(FRAME_EDITOR_VISUALS)    
FRAME_EDITOR_VISUALS_GRAPH = Image.open(os.path.join("resources", "themed", "u_frame_editor_visuals_graph.png")).convert("RGBA")
FRAME_EDITOR_VISUALS_GRAPH_ARRAY = numpy.array(FRAME_EDITOR_VISUALS_GRAPH)
FRAME_EDITOR_VISUALS_GRAPH_BAR = Image.open(os.path.join("resources", "themed", "u_frame_editor_visuals_graph_bar.png")).convert("RGBA")
FRAME_EDITOR_VISUALS_GRAPH_BAR_ARRAY = numpy.array(FRAME_EDITOR_VISUALS_GRAPH_BAR)
FRAME_OPTIONS = Image.open(os.path.join("resources", "themed", "u_frame_options.png")).convert("RGBA")
FRAME_OPTIONS_ARRAY = numpy.array(FRAME_OPTIONS) 
FRAME_OPTIONS_BUTTON_ON = Image.open(os.path.join("resources", "themed", "u_frame_options_button_on.png")).convert("RGBA")
FRAME_OPTIONS_BUTTON_ON_ARRAY = numpy.array(FRAME_OPTIONS_BUTTON_ON)
FRAME_OPTIONS_BUTTON_OFF = Image.open(os.path.join("resources", "themed", "u_frame_options_button_off.png")).convert("RGBA")
FRAME_OPTIONS_BUTTON_OFF_ARRAY = numpy.array(FRAME_OPTIONS_BUTTON_OFF)
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
