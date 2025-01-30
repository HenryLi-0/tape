from subsystems.node.node_functional import *
from subsystems.node.node_primatives import *

from subsystems.settings import *

# TO-DO: FINISH REFACTORING

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
        self.__output = self
        self.__x = Pixel(0)
        self.__y = Pixel(0)
        self.set(x, y)
    def set(self, x:Number|Pixel, y:Number|Pixel):
        self.__xNode = x
        self.__yNode = y
        self.update()
    def get(self):
        return [self.__xNode, self.__yNode]
    def update(self):
        if validate(self.__xNode, self.__yNode):
            if type(self.__xNode) == Number: self.__x.set(self.__xNode.value*ANIMATION_WIDTH.get())
            elif type(self.__xNode) == Pixel: self.__x.set(self.__xNode)
            else: self.addError("Invalid x!")
            if type(self.__yNode) == Number: self.__y.set(Number(self.__yNode.value*ANIMATION_HEIGHT.get()))
            elif type(self.__yNode) == Pixel: self.__y.set(self.__yNode)
            else: self.addError("Invalid y!")
        else: self.addError("Input(s) missing or contain errors!")

    @property
    def x(self): return self.__x
    @property
    def y(self): return self.__y
    @property
    def output(self): return self

'''PATHING''' # TO-DO: REFACTOR EVERYTHING BELOW HERE!!!

@Input("Value", [Coordinate, Number, Angle, Pixel], True)
@Input("Time", [Time], True)
@Display()
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
        self.update()
    def get(self):
        return [self.__output, self.__time]
    def update(self):
        pass # TO-DO: finish!

    @property
    def value(self): return self.__output

    @property
    def time(self): return self.__time

    @property
    def output(self): return self

@Input("Frames", [Frame], True, True)
@Display("Frames", False, lambda self: self.framesLength)
@Output("Path", -1, lambda self: self)
class Path(Node):
    '''
        A path is the stores information of any number of frames, to be interpolated.
        
        Requires:
        - `frames` is any number of Frames of the type.
    '''
    def __init__(self, *frames:Frame):
        super().__init__()
        self.set(*frames)
    def set(self, *frames:Frame):
        self.__allFrames = [*frames]
        self.update()
    def get(self):
        return self.__allFrames
    def update(self):
        if validate(*self.__allFrames):
            for frame in self.__allFrames:
                if frame.type != self.__allFrames[0].type:
                    self.addError("Frames are not of consistent type!")
                    break
        else: self.addError("Input(s) missing or contain errors!")

    @property
    def framesLength(self): return len(self.__allFrames)

    @property
    def frames(self): return self.__allFrames

    @property
    def output(self): return self

class PathCalculator(Node):
    '''
        Gets the value of a path at a given time, with a specific calculation method.

        Requires:
        - `path` is a Path of any type.
        - `time` is a Time, representing the time of which when is a desired value.
    '''
    def __init__(self):
        super().__init__()
        self.__output = None
    def set(self, path:Path, time:Time):
        self.__path = path
        self.__time = time
        self.update()
    def get(self):
        return [self.__path, self.__time]
    def calculate(self):
        pass
    def update(self):
        if validate(self.__path, self.__time):
            self.__path.update()
            self.__time.update()

        else: self.addError("Input(s) missing or contain errors!")
    @property
    def calculatePath(self):
        return self.calculate(self.__allFrames) # TO-DO: MAKE MORE EFFICIENT

@Output("Linear Path Type", -1, lambda self: self)
class LinearPathType(PathCalculator):
    def calculate(self, *frames:Frame):
        pass # TO-DO: FINISH

@Output("Bezier Path Type", -1, lambda self: self)
class BezierPathType(PathCalculator):
    def calculate(self, *frames:Frame):
        pass # TO-DO: FINISH

@Output("Smooth Approach Path Type", -1, lambda self: self)
class SmoothApproachesPathType(PathCalculator):
    def calculate(self, *frames:Frame):
        pass # TO-DO: FINISH

@Output("Smooth Full Path Type", -1, lambda self: self)
class SmoothFullPathType(PathCalculator):
    def calculate(self, *frames:Frame):
        pass # TO-DO: FINISH


@Input("X Axis Path", [Path], True)
@Input("Y Axis Path", [Path], True)
@Display()
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
@Display()
@Output("Frame", Frame, lambda self: self.output)
class PathAtTime(Node):
    '''

    '''
    def __init__(self, path:Path, time:Time):
        super().__init__()
        self.__output = None
        self.__temp = None
        self.__mode = None
        self.set(path, time)
    def set(self, path:Path, time:Time):
        self.__path = path
        self.__time = time
        frameClass = self.__path.__allFrames[0].value.__class__
        if frameClass == Coordinate:
            self.__temp = [Number(0), Number(0)]
            self.__output = Coordinate()
            self.__output.set(*self.__temp)
            self.__mode = "coords"
        elif frameClass == Unit:
            self.__temp = [Number(0)]
            self.__output = self.__path.__allFrames[0].value.__class__()
            self.__output.set(*self.__temp)
            self.__mode = "unit"
        else:
            self.addError(f"Unexpected frame data type {frameClass}!")
        self.update()
    def update(self):
        self.__output.update()
        pass # TO-DO: FINISH PATH LOGIC
    
    @property
    def output(self): return self.__output

@Input("Path(s)", [Path], False, True)
@Display()
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

