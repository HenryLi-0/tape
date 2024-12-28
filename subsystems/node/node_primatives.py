from subsystems.point import *
from subsystems.pathing import *
import random, uuid, os, math, time
from PIL import Image

'''NODE'''

class ActiveError:
    def __init__(self, error = None):
        self.errors = []
        self.addError(error)
    def addError(self, error):
        self.errors.append(f"{time.time()} - {error}")
        
class Node:
    def __init__(self):
        self.id = uuid.uuid4()
        self.error = ActiveError()
    def addError(self, error):
        self.error(f"{self.id}\n   {error}")
    def getError(self):
        return self.error
    def get(self):
        return None

'''SIMPLE/BASIC'''

class Number(Node):
    '''
        A number.
    '''
    def __init__(self, start:int|float = None):
        super().__init__()
        self.number = start
    def get(self) -> int|float:
        return self.number
    
class Boolean(Node):
    '''
        A boolean.
    '''
    def __init__(self, boolean:bool):
        super().__init__()
        self.boolean = boolean
    def get(self) -> bool:
        return self.boolean
    
class String(Node):
    '''
        A string.
    '''
    def __init__(self, string:str):
        super().__init__()
        self.string = string
    def get(self) -> str:
        return self.string

class Random(Node):
    '''
        A random number, with range [a,b], includes both end points.

        Requires:
        - `lowerLimit` defines the minimum possible output.
        - `upperLimit` defines the maximum possible output.
        - `onlyIntegers` defines whether or not only integers are returned.
        
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
        A file or directory location.

        Requires:
        - `location` represents the file location
    '''
    def __init__(self, location:String):
        super().__init__() 
        index = location.get().rfind(".")
        if index == -1:
            if os.path.exists(location.get()):
                self.fileLocation = location
                self.extension = "/folder"
            else:
                self.addError(f"Directory {location.get} doesn't exist!")
        else:
            fileType = location.get()[index:]
            if fileType in [".txt", ".png", ".jpg", ".jpeg"]:
                if os.path.exists(location.get()):
                    self.fileLocation = location
                    self.extension = fileType
                else:
                    self.addError(f"File {location.get()} doesn't exist!")
            else:
                self.addError(f"File extension {fileType} invalid! (for safety reasons)")
        return None
    def get(self) -> str:
        return self.fileLocation

'''UNITS'''

class Unit(Node):
    '''
        A class for all types of Units to inherit from.
    '''
    def simplify(unit): # TO-DO: COMPLETE, BUT MAKE IT MORE EFFICIENT!
        '''
            Turns a unit to its simpliest form, consist with all other simplified version.
        '''
        pass
        


class Angle(Unit):
    '''
        A class for all types of Angle units to inherit from.
    '''
    def simplify(unit):
        return Degrees(unit)

class Degrees(Angle):
    '''
        A unit of angle, representing 1/360th of a circle.
        Requires:
        - `angle` is either a Angle type or a Number type object. Angle types will be converted, while Numbers will be in degrees.
    '''
    def __init__(self, angle:Angle|Number = Number(0)):
        super().__init__()
        if type(angle) == Number:       self.value = angle
        elif type(angle) == Degrees:    self.value = Number(angle.get().get())
        elif type(angle) == Radians:    self.value = Number(angle.get().get()/math.pi*180)
        else: self.addError("Invalid input!")
    def get(self) -> Angle:
        return self.value

class Radians(Angle):
    '''
        A unit of angle, where 2*PI radians represents a complete circle.
        Requires:
        - `angle` is either a Time type or a Number type object. Angle types will be converted, while Numbers will be in radians.
    '''
    def __init__(self, angle:Angle|Number = Number(0)):
        super().__init__()
        if type(angle) == Number:       self.value = angle
        elif type(angle) == Degrees:    self.value = Number(angle.get().get()/180*math.pi)
        elif type(angle) == Radians:    self.value = Number(angle.get().get())
        else: self.addError("Invalid input!")
    def get(self) -> Angle:
        return self.value


# TO-DO: return Pixel(unit)

class Pixel(Unit):
    pass

class Time(Unit):
    '''
        A class for all types of Time units to inherit from.
    '''
    def simplify(unit):
        return Seconds(unit)

class Milliseconds(Time):
    '''
        A unit of time, representing 1/1000th of a second.
        Requires:
        - `time` is either a Time type or a Number type object. Time types will be converted, while Numbers will be in milliseconds.
    '''
    def __init__(self, time:Time|Number = Number(0)):
        super().__init__()
        if type(time) == Number:         self.value = time
        elif type(time) == Milliseconds: self.value = Number(time.get().get())
        elif type(time) == Seconds:      self.value = Number(time.get().get()*1000)
        elif type(time) == Minutes:      self.value = Number(time.get().get()*1000*60)
        elif type(time) == Hours:        self.value = Number(time.get().get()*1000*60*60)
        elif type(time) == Days:         self.value = Number(time.get().get()*1000*60*60*24)
        else: self.addError("Invalid input!")
    def get(self) -> Time:
        return self.value

class Seconds(Time):
    '''
        A unit of time, representing a second.
        Requires:
        - `time` is either a Time type or a Number type object. Time types will be converted, while Numbers will be in seconds.
    '''
    def __init__(self, time:Time|Number = Number(0)):
        super().__init__()
        if type(time) == Number:         self.value = time
        elif type(time) == Milliseconds: self.value = Number(time.get().get()/1000)
        elif type(time) == Seconds:      self.value = Number(time.get().get())
        elif type(time) == Minutes:      self.value = Number(time.get().get()*60)
        elif type(time) == Hours:        self.value = Number(time.get().get()*60*60)
        elif type(time) == Days:         self.value = Number(time.get().get()*60*60*24)
        else: self.addError("Invalid input!")
    def get(self) -> Time:
        return self.value

class Minutes(Time):
    '''
        A unit of time, representing a minute.
        Requires:
        - `time` is either a Time type or a Number type object. Time types will be converted, while Numbers will be in minutes.
    '''
    def __init__(self, time:Time|Number = Number(0)):
        super().__init__()
        if type(time) == Number:         self.value = time
        elif type(time) == Milliseconds: self.value = Number(time.get().get()/1000/60)
        elif type(time) == Seconds:      self.value = Number(time.get().get()/60)
        elif type(time) == Minutes:      self.value = Number(time.get().get())
        elif type(time) == Hours:        self.value = Number(time.get().get()*60)
        elif type(time) == Days:         self.value = Number(time.get().get()*60*24)
        else: self.addError("Invalid input!")
    def get(self) -> Time:
        return self.value

class Hours(Time):
    '''
        A unit of time, representing an hour.
        Requires:
        - `time` is either a Time type or a Number type object. Time types will be converted, while Numbers will be in hours.
    '''
    def __init__(self, time:Time|Number = Number(0)):
        super().__init__()
        if type(time) == Number:         self.value = time
        elif type(time) == Milliseconds: self.value = Number(time.get().get()/1000/60/60)
        elif type(time) == Seconds:      self.value = Number(time.get().get()/60/60)
        elif type(time) == Minutes:      self.value = Number(time.get().get()/60)
        elif type(time) == Hours:        self.value = Number(time.get().get())
        elif type(time) == Days:         self.value = Number(time.get().get()*24)
        else: self.addError("Invalid input!")
    def get(self) -> Time:
        return self.value

class Days(Time):
    '''
        A unit of time, representing a day.
        Requires:
        - `time` is either a Time type or a Number type object. Time types will be converted, while Numbers will be in days.
    '''
    def __init__(self, time:Time|Number = Number(0)):
        super().__init__()
        if type(time) == Number:         self.value = time
        elif type(time) == Milliseconds: self.value = Number(time.get().get()/1000/60/60/24)
        elif type(time) == Seconds:      self.value = Number(time.get().get()/60/60/24)
        elif type(time) == Minutes:      self.value = Number(time.get().get()/60/24)
        elif type(time) == Hours:        self.value = Number(time.get().get()/24)
        elif type(time) == Days:         self.value = Number(time.get().get())
        else: self.addError("Invalid input!")
    def get(self) -> Time:
        return self.value

'''IO'''

class ImageImport(Node):
    '''
        Imports an image file at the given file location/path.
        Requires:
        - `location` represents the image's file location.
    '''
    def __init__(self, location:FileLocation):
        super().__init__()
        file = location.get()
        if location.extension in [".png", ".jpg", ".jpeg"]:
            self.file = Image.open(file).convert("RGBA")
        else:
            self.addError(f"File extension {location.extension} is not a supported image file type!")
    def get(self) -> Image:
        return self.file

class FolderImport(Node):
    '''
        Imports an iterable series of images, given a folder location/path.
        Requires:
        - `location` represents the folder containing the image files.
    '''
    def __init__(self, location:FileLocation):
        super().__init__()
        if location.extension == "/folder":
            directory = location.get()
            # TO-DO: finish, and make sure its safe
        else:
            self.addError(f"The file location isn't a folder/directory!")

'''LOGIC'''

class Reroute(Node):
    '''
        Returns the same node that was given in.
        Requires:
        - `inputNode` represents any node type.
    '''
    def __init__(self, inputNode:Node):
        super().__init__()
        self.inputNode = inputNode
    def get(self):
        return self.inputNode

class Comparison(Node):
    '''
        A class for all types of logical operations related with booleans.
    '''
    pass

class LessThan(Comparison):
    def __init__(self, inputA:Number|Unit, inputB:Number|Unit):
        super().__init__()
        if type(inputA) == type(inputB):
            if type(inputA) == Number:
                self.output = Boolean(inputA.get() < inputB.get())
            elif type(inputA) == Unit:
                a = inputA.simplify()
                b = inputB.simplify()
                if type(a) == type(b):
                    self.output = Boolean(a.get() < b.get())
                else:
                    self.addError(f"Inconsistent Unit dimensions {type(a)} and {type(b)}!")
                # TO-DO: COMPLETE, BUT MAKE IT MORE EFFICIENT!
        else:
            self.addError("Inconsistent type for comparison!")
    def get(self):
        return self.output

class GreaterThan(Comparison):
    def __init__(self, inputA:Number|Unit, inputB:Number|Unit):
        super().__init__()
        if type(inputA) == type(inputB):
            if type(inputA) == Number:
                self.output = Boolean(inputA.get() > inputB.get())
            elif type(inputA) == Unit:
                a = inputA.simplify()
                b = inputB.simplify()
                if type(a) == type(b):
                    self.output = Boolean(a.get() > b.get())
                else:
                    self.addError(f"Inconsistent Unit dimensions {type(a)} and {type(b)}!")
                # TO-DO: COMPLETE, BUT MAKE IT MORE EFFICIENT!
        else:
            self.addError("Inconsistent type for comparison!")
    def get(self):
        return self.output

class EqualTo(Comparison):
    def __init__(self, inputA:Number|Unit, inputB:Number|Unit):
        super().__init__()
        if type(inputA) == type(inputB):
            if type(inputA) == Number:
                self.output = Boolean(inputA.get() == inputB.get())
            elif type(inputA) == Unit:
                a = inputA.simplify()
                b = inputB.simplify()
                if type(a) == type(b):
                    self.output = Boolean(a.get() == b.get())
                else:
                    self.addError(f"Inconsistent Unit dimensions {type(a)} and {type(b)}!")
                # TO-DO: COMPLETE, BUT MAKE IT MORE EFFICIENT!
        else:
            self.addError("Inconsistent type for comparison!")
    def get(self):
        return self.output