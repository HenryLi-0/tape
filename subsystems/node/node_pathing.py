from subsystems.node.node_primatives import *
from subsystems.settings import *

'''Location'''

@Input("x", [Number, Pixel], True)
@Input("y", [Number, Pixel], True)
@Display("Value", False, lambda self: f"({self.x.value})")
@Output("x", Pixel, lambda self: self.x)
@Output("y", Pixel, lambda self: self.y)
@Output("Coordinate", -1, lambda self: self.output)
class Coordinate(Node):
    '''
        A coordinate representing a location on a 2D plane.

        Requires:
        - `x` represents the x coordinate.
        - `y` represents the y coordinate.
    '''
    def __init__(self, x:Number|Pixel, y:Number|Pixel):
        super().__init__()
        self.__output = None
        self.__x = Pixel(0)
        self.__y = Pixel(0)
        self.set(x, y)
    def set(self, x:Number|Pixel, y:Number|Pixel):
        self.__xNode = x
        self.__yNode = y
        self.update()
    def update(self):
        if type(self.__xNode) == Number: self.__x.set(self.__xNode.value*ANIMATION_WIDTH.get())
        elif type(self.__xNode) == Pixel: self.__x.set(self.__xNode)
        else: self.addError("Invalid x!")
        if type(self.__yNode) == Number: self.__y.set(Number(self.__yNode.value*ANIMATION_HEIGHT.get()))
        elif type(self.__yNode) == Pixel: self.__y.set(self.__yNode)
        else: self.addError("Invalid y!")

    @property
    def x(self): return self.__x
    @property
    def y(self): return self.__y
    @property
    def output(self): return self

'''PATHING''' # TO-DO: REFACTOR EVERYTHING BELOW HERE!!!

@Input("Value", [Coordinate, Number, Angle, Pixel], True)
@Input("Time", [Time], True)
@Output("Frame", -1, lambda self: self.output)
class Frame(Node):
    '''
        A frame, representing a coordinate or value at a set period in time.

        Requires:
        - `value` represents a value or coordinate.
        - `time` represents the time after the start.
    '''
    def __init__(self, value:Coordinate|Number|Angle|Pixel, time:Time):
        super().__init__()
        self.__output = None
        self.__time = None
    def set(self, value:Coordinate|Number|Angle|Pixel, time:Time):
        if issubclass(type(time), Time):
            self.__output = value
            self.__time = time
        else:
            self.addError("Inputted Time is not a Time!")

    @property
    def output(self): return self

# No inputs or outputs.
class PathType(Node):
    '''
        A class that consists of all types of Paths for Pathing that does the calculations without storing/linking Node data.
    '''
    def __init__(self):
        super().__init__()
    def path(self, *frames:Frame):
        pass
    def update(self, *frames:Frame) -> list[Frame]:
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

@Input("Path Type", [PathType], True)
@Input("Frames", [Frame], True, MAX_UNCAPPED_NODES_LIMIT.get())
@Output("Path", -1, lambda self: self.output)
class Path(Node):
    '''
        A path is the interpolated information of any number of frames, given an approach of calculation.
        
        Requires:
        - `pathType` is a PathType that represents the method used to calculate to Path.
        - `frames` is any number of Frames of the type.
    '''
    def __init__(self, pathType:PathType, *frames:Frame):
        super().__init__()
        self.set(pathType, *frames)
    def set(self, pathType:PathType, *frames:Frame):
        self.pathType = pathType
        self.frames = [*frames]
    
    @property
    def output(self): return self

@Input("X Axis Path", [Path], True)
@Input("Y Axis Path", [Path], True)
@Output("Coordinate Path", Path, lambda self: self.output)
class PathAxisMerger(Node):
    '''
        Merges two paths together, one representing the x axis and one representing the y axis, into a single path of coordinates.

        Requires:
        - `xAxisPath` is a Path representing the x axis.
        - `yAxisPath` is a Path representing the y axis.
    '''
    def __init__(self, xAxisPath:Path, yAxisPath:Path):
        super().__init__()
        self.__output = Path()
        self.set(xAxisPath, yAxisPath)
    def set(self, xAxisPath:Path, yAxisPath:Path):
        self.__xAxisPath = xAxisPath
        self.__yAxisPath = yAxisPath
        self.update()
    def update(self):
        pass # TO-DO: FINISH PATH LOGIC
    
    @property
    def output(self): return self.__output

@Input("Path", [Path], True)
@Input("At Time", [Time], True)
@Output("Frame", Frame, lambda self: self.output)
class PathAtTime(Node):
    '''
        Gets the value of a path at a given time.

        Requires:
        - `path` is a Path of any type.
        - `time` is a Time, representing the time of which when is a desired value.
    '''
    def __init__(self, path:Path, time:Time):
        super().__init__()
        self.__output = None
        self.set(path, time)
    def set(self, path:Path, time:Time):
        self.__path = path
        self.__time = time
        frameClass = self.__path.frames[0].__value.__class__
        if frameClass == Coordinate:
            self.__output = Coordinate(Number(0), Number(0))
        elif frameClass == Unit:
            self.__output = self.__path.frames[0].__value.__class__(Number(0))
        else:
            self.addError(f"Unexpected frame data type {frameClass}!")
        self.update()
    def update(self):
        pass # TO-DO: FINISH PATH LOGIC
    
    @property
    def output(self): return self.__output

@Input("Path(s)", [Path], False, MAX_UNCAPPED_NODES_LIMIT.get())
@Output("Output Path", Path, lambda self: self.output)
class PathMerger(Node):
    '''
        Merges any number of paths of the same type into one.
    '''
    def __init__(self, *paths):
        super().__init__()
        self.__output = Path()
        for path in paths:
            pass
        # TO-DO: FINISH PATH LOGIC
    def set():
        pass
    def update(self):
        pass # TO-DO: FINISH PATH LOGIC

    @property
    def output(self): return self.__output

