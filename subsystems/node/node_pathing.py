from subsystems.node.node_primatives import *
from subsystems.settings import *

'''Location'''

class Coordinate(Node):
    '''
        A coordinate representing a location on a 2D plane.

        Requires:
        - `x` represents the x coordinate.
        - `y` represents the y coordinate.
    '''
    IN = [[[Number, Pixel], True], [[Number, Pixel], True]]
    OUT = [None]
    def __init__(self, x:Number|Pixel, y:Number|Pixel):
        super().__init__()
        self.output = None
        self.x = 0
        self.y = 0
        self.set(x, y)
    def set(self, x:Number|Pixel, y:Number|Pixel):
        self.xNode = x
        self.yNode = y
    def get(self):
        if type(self.xNode) == Number: xcoord = self.xNode*ANIMATION_WIDTH.get()
        elif type(self.xNode) == Pixel: xcoord = self.xNode
        else: self.addError("Invalid x!")
        if type(self.yNode) == Number: ycoord = self.yNode*ANIMATION_HEIGHT.get()
        elif type(self.yNode) == Pixel: ycoord = self.yNode
        else: self.addError("Invalid y!")
        self.x = xcoord
        self.y = ycoord
        return None


'''PATHING''' # TO-DO: REFACTOR EVERYTHING BELOW HERE!!!

class Frame(Node):
    '''
        A frame, representing a coordinate or value at a set period in time.

        Requires:
        - `value` represents a value or coordinate.
        - `time` represents the time after the start.
    '''
    IN = [[[Coordinate, Number, Angle, Pixel], True], [[Time], True]]
    OUT = None
    def __init__(self, value:Coordinate|Number|Angle|Pixel, time:Time):
        super().__init__()
        self.value = None
        self.time = None
    def set(self, value:Coordinate|Number|Angle|Pixel, time:Time):
        if issubclass(type(time), Time):
            self.type = type(value)
            self.value = value
            self.time = time
        else:
            self.addError("Inputted Time is not a Time!")
    def get(self):
        pass

class PathType(Node):
    '''
        A class that consists of all types of Paths for Pathing that does the calculations without storing/linking Node data.
    '''
    IN = [[[None], False]]
    OUT = [None]
    def __init__(self):
        super().__init__()
    def path(self, *frames:Frame):
        pass
    def get(self, *frames:Frame) -> list[Frame]:
        for frame in frames:
            if frame.type != frames[0].type:
                self.addError("Frames are not of consistent type!")
                break
        return self.path(*frames)

class LinearPathType(PathType):
    def path(self, *frames:Frame):
        pass # TO-DO: FINISH

class BezierPathType(PathType):
    def path(self, *frames:Frame):
        pass # TO-DO: FINISH

class SmoothApproachesPathType(PathType):
    def path(self, *frames:Frame):
        pass # TO-DO: FINISH

class SmoothFullPathType(PathType):
    def path(self, *frames:Frame):
        pass # TO-DO: FINISH

class Path(Node):
    '''
        A path is the interpolated information of any number of frames, given an approach of calculation.
        
        Requires:
        - `pathType` is a PathType that represents the method used to calculate to Path.
        - `frames` is any number of Frames of the type.
    '''
    IN = [[[PathType], True], [[Frame], -1]]
    OUT = None # TO-DO: FINISH
    def __init__(self, pathType:PathType, *frames:Frame):
        super().__init__()
        output = None
        self.set(pathType, *frames)
    def set(self, pathType:PathType, *frames:Frame):
        self.pathType = pathType
        self.frames = [*frames]
    def get(self):
        self.path = self.pathType(*self.frames)
        return self.path

class PathAxisMerger(Node):
    '''
        Merges two paths together, one representing the x axis and one representing the y axis, into a single path of coordinates.

        Requires:
        - `xAxisPath` is a Path representing the x axis.
        - `yAxisPath` is a Path representing the y axis.
    '''
    IN = [[[Path], True], [[Path], True]]
    OUT = [Path]
    def __init__(self, xAxisPath:Path, yAxisPath:Path):
        super().__init__()
        self.output = Path()
        
        self.xAxisPath = xAxisPath
        self.yAxisPath = yAxisPath
        # TO-DO: FINISH PATH LOGIC
    def get(self) -> Path:
        pass # TO-DO: FINISH PATH LOGIC

class PathAtTime(Node):
    '''
        Gets the value of a path at a given time.

        Requires:
        - `path` is a Path of any type.
        - `time` is a Time, representing the time of which when is a desired value.
    '''
    IN = [[[Path], True], [[Time], True]]
    OUT = [Node] # TO-DO: FINISH
    def __init__(self, path:Path, time:Time):
        super().__init__()
        self.path = path
        self.time = time
        # TO-DO: FINISH PATH LOGIC
    def get(self):
        pass # TO-DO: FINISH PATH LOGIC

class PathMerger(Node):
    '''
        Merges any number of paths of the same type into one.
    '''
    IN = [[[Path], -1]]
    OUT = [Path]
    def __init__(self, *paths):
        super().__init__()
        for path in paths:
            pass
        # TO-DO: FINISH PATH LOGIC
    def get(self) -> Path:
        pass # TO-DO: FINISH PATH LOGIC

