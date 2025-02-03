'''This file imports all node files to be easily imported by other files in one import, instead of multiple.'''
from subsystems.node.node_functional import *
from subsystems.node.node_primatives import *
from subsystems.node.node_pathing import *
from subsystems.node.node_operations import *
from subsystems.node.node_render import *

# Add any plug-ins here!
# TO-DO: Alternatively, you can also add plug-ins through the Tape UI!




# Additionally, update this master nodes list!

NODES = [
    # Primatives
        Number, Boolean, String,
        Random, FileLocation,
        # Units
            # Angle 
                Degrees, Radians, 
            # Distance 
                Pixels, 
            # Time
                Milliseconds, Seconds, Minutes, Hours, Days,
            # IO
                ImageImport, FolderImport,
            # Logic
                Reroute, 
                LessThan, GreaterThan, EqualTo,
                And, Or, Not,
                If,
    # Pathing
        Coordinate, Frame,
        # PathType
            LinearPath, BezierPath, SmoothApproachPath, SmoothFullPath,
        # Paths
            Path, PathAxisMerger, PathAtTime, PathMerger,
    # Operations
        Addition, Multiplication,

    # Render
        AnimationTime,
        RenderInstructions, Sprite, Camera, Render,
]

from subsystems.fancy import fill
from settings import NODE_IO_TRIANGLE

class NodeThemes:
    UNKNOWN             = (255,255,255,255)
    YELLOW              = (168,152, 37,255)
    BLUE                = ( 37,127,168,255)
    ORANGE              = (233,135, 39,255)
    LIGHT_ORANGE        = (241,181, 88,255)
    PURPLE              = (109, 57,153,255)
    RED                 = (204, 54, 54,255)
    DARK_GREEN          = ( 58,145, 56,255)


NODE_THEMES_ASSGINMENT = {
    "default"           : NodeThemes.UNKNOWN,
    Node                : NodeThemes.UNKNOWN,
    
    # Primatives
    Number              : NodeThemes.YELLOW,
    Boolean             : NodeThemes.YELLOW,
    String              : NodeThemes.YELLOW, 

    Random              : NodeThemes.ORANGE, 
    FileLocation        : NodeThemes.ORANGE, 

    # Units
    Unit                : NodeThemes.BLUE,
    RawUnit             : NodeThemes.BLUE,
    Angle               : NodeThemes.BLUE,
    Degrees             : NodeThemes.BLUE,
    Radians             : NodeThemes.BLUE,
    Distance            : NodeThemes.BLUE,
    Pixels              : NodeThemes.BLUE,
    Time                : NodeThemes.BLUE,
    Milliseconds        : NodeThemes.BLUE,
    Seconds             : NodeThemes.BLUE,
    Minutes             : NodeThemes.BLUE,
    Hours               : NodeThemes.BLUE,
    Days                : NodeThemes.BLUE,

    # IO
    ImageWrapper        : NodeThemes.ORANGE,
    ImageImport         : NodeThemes.ORANGE,
    FolderImport        : NodeThemes.ORANGE,

    # Logic
    LogicalOperation    : NodeThemes.LIGHT_ORANGE,
    Reroute             : NodeThemes.LIGHT_ORANGE,
    LessThan            : NodeThemes.LIGHT_ORANGE,
    GreaterThan         : NodeThemes.LIGHT_ORANGE,
    EqualTo             : NodeThemes.LIGHT_ORANGE,
    And                 : NodeThemes.LIGHT_ORANGE,
    Or                  : NodeThemes.LIGHT_ORANGE,
    Not                 : NodeThemes.LIGHT_ORANGE,
    If                  : NodeThemes.LIGHT_ORANGE,

    # Pathing
    Coordinate          : NodeThemes.PURPLE,
    Frame               : NodeThemes.PURPLE,
    Path                : NodeThemes.PURPLE,
    PathCalculator      : NodeThemes.PURPLE,
    LinearPath          : NodeThemes.PURPLE,
    BezierPath          : NodeThemes.PURPLE,
    SmoothApproachPath  : NodeThemes.PURPLE,
    SmoothFullPath      : NodeThemes.PURPLE,
    PathAxisMerger      : NodeThemes.PURPLE,
    PathAtTime          : NodeThemes.PURPLE,
    PathMerger          : NodeThemes.PURPLE,

    # Operations
    Addition            : NodeThemes.RED,
    Multiplication      : NodeThemes.RED,

    # Render
    AnimationTime       : NodeThemes.DARK_GREEN,
    RenderInstructions  : NodeThemes.DARK_GREEN,
    Sprite              : NodeThemes.DARK_GREEN,
    Camera              : NodeThemes.DARK_GREEN,
    Render              : NodeThemes.DARK_GREEN,
}
NODE_THEMES_TRIANGLES = {getattr(NodeThemes,x):fill(NODE_IO_TRIANGLE.copy(), [255,255,255,255], getattr(NodeThemes,x)) for x in dir(NodeThemes) if x[0:2] != "__"}




