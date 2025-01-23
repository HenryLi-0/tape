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
                Pixel, 
            # Time
                Milliseconds, Seconds, Minutes, Hours, Days,
            # IO
                ImageWrapper, ImageImport, FolderImport,
            # Logic
                Reroute, 
                LessThan, GreaterThan, EqualTo,
                And, Or, Not,
                If,
    # Pathing
        Coordinate, Frame,
        # PathType
            LinearPathType, BezierPathType, SmoothApproachesPathType, SmoothFullPathType,
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
    UNKNOWN     = (255,255,255,255)
    YELLOW      = (168,152, 37,255)
    ORANGE      = (233,135, 39,255)

NODE_THEMES_ASSGINMENT = {
    Number          : NodeThemes.YELLOW,
    Boolean         : NodeThemes.YELLOW,
    String          : NodeThemes.YELLOW, 

    FileLocation    : NodeThemes.ORANGE, 
}
NODE_THEMES_TRIANGLES = {getattr(NodeThemes,x):fill(NODE_IO_TRIANGLE, [255,255,255,255], getattr(NodeThemes,x)) for x in dir(NodeThemes) if x[0:2] != "__"}




