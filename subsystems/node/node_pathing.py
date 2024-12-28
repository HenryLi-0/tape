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
    def __init__(self, x:Number|Pixel = Number(0), y:Number|Pixel = Number(0)):
        super().__init__()
        if type(x) == Number: xcoord = x*ANIMATION_WIDTH.get()
        elif type(x) == Pixel: xcoord = x
        else: self.addError("Invalid x!")
        if type(y) == Number: ycoord = y*ANIMATION_HEIGHT.get()
        elif type(y) == Pixel: ycoord = y
        else: self.addError("Invalid y!")
        self.x = xcoord
        self.y = ycoord
    def get(self):
        return self


'''PATHING'''

class Frame(Node):
    '''
        A frame, representing a coordinate or value at a set period in time.
        Requires:
        - `value` represents a value or coordinate.
        - `time` represents the time after the start.
    '''
    def __init__(self, value:Coordinate|Number|Angle|Pixel = Coordinate(Number(0),Number(0)), time:Time = Seconds(0)):
        super().__init__()
        if issubclass(type(time), Time):
            self.type = type(value)
            self.value = value
            self.time = time
        else:
            self.addError("Inputted Time is not a Time!")
    def get(self):
        pass # TO-DO: FINISH



class PathType(Node):
    '''
        A class that consists of all types of Paths for Pathing.
    '''
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
    def __init__(self, pathType:PathType, *frames:Frame):
        super().__init__()
        self.path = pathType(*frames)
    def get(self):
        return self.path