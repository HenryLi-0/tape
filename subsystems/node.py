from subsystems.point import *
from subsystems.pathing import *
import random, uuid
from PIL import Image



class ActiveError:
    def __init__(self, error = None):
        self.error = error

class Node:
    def __init__(self):
        self.id = uuid.uuid4()
        self.error = ActiveError()
    def getError(self):
        return self.error.error
    def get(self):
        return None



'''Simple'''

class Number(Node):
    '''
        A number.
    '''
    def __init__(self, start = None):
        super().__init__()
        self.number = start
    def get(self) -> int|float:
        return self.number
    
class Boolean(Node):
    '''
        A boolean.
    '''
    def __init__(self, boolean):
        super().__init__()
        self.boolean = boolean
    def get(self) -> bool:
        return self.boolean
    
class String(Node):
    '''
        A string.
    '''
    def __init__(self, string):
        super().__init__()
        self.string = string
    def get(self) -> str:
        return self.string

class Random(Node):
    '''
        A random number, with range [a,b], includes both end points

        Requires:
        - `lowerLimit` defines the minimum possible output
        - `upperLimit` defines the maximum possible output
        - `onlyIntegers` defines whether or not only integers are returned`
        
    '''
    def __init__(self, lowerLimit:Number = Number(0), upperLimit:Number = Number(1), onlyIntegers:Boolean = Boolean(False)):
        super().__init__()
        self.lowerLimit = lowerLimit.get()
        self.upperLimit = upperLimit.get()
        self.onlyIntegers = onlyIntegers.get()
    def get(self) -> Number:
        try:
            if self.lowerLimit == self.upperLimit: return self.lowerLimit
            elif self.onlyIntegers: return random.randint(self.lowerLimit, self.upperLimit)
            else: return random.random()*(self.upperLimit-self.lowerLimit)+self.lowerLimit
        except:
            self.error.error = "Random number failed to generate!"

class FileLocation(Node):
    '''
        A file location 

        Requires:
        - `` file location
    '''
    def __init__(self, fileLocation:String = String("C:/")):
        super().__init__() 
        index = fileLocation.get().rfind(".")
        if index == -1:
            self.error.error = "File extension missing!"
        else:
            fileType = fileLocation.get()[index:]
            if fileType in [".txt", ".png", ".jpg", ".jpeg"]:
                self.fileLocation = fileLocation
            else:
                self.error.error = f"File extension {fileType} invalid! (for safety reasons)"
    def get(self):
        # TO-DO: finish 
        pass

class Coordinate(Node):
    '''
        A coordinate representing a location on a 2D plane

        Requires:
        - `x` represents the x coordinate
        - `y` represents the y coordinate
    '''
    def __init__(self, x:Number = Number(0), y:Number = Number(0)):
        super().__init__()
        self.coordinate = [x,y]
    def get(self):
        return self.coordinate



'''Units'''

class Unit(Node):
    pass
    # i have no clue what to do here


class Angle(Unit):
    pass

class Degrees(Angle):
    pass

class Radians(Angle):
    pass


class Pixel(Unit):
    pass


class Time(Unit):
    pass

class Milliseconds(Time):
    pass

class Seconds(Time):
    pass

class Minutes(Time):
    pass

class Hours(Time):
    pass

class Days(Time):
    pass



'''Operations'''