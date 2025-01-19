'''This file imports all node files to be easily imported by other files in one import, instead of multiple.'''
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