from subsystems.point import *
from subsystems.pathing import *
import random, uuid, os, math
from PIL import Image



class ActiveError:
    def __init__(self, error = None):
        self.error = error
    def addError(self, error):
        pass # TO-DO: error manager of sorts

class Node:
    def __init__(self):
        self.id = uuid.uuid4()
        self.error = ActiveError()
    def addError(self, error):
        self.error(error)
    def getError(self):
        return self.error
    def get(self):
        return None





'''SIMPLE/BASIC'''

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
        A file location 

        Requires:
        - `` file location
    '''
    def __init__(self, fileLocation:String = String("C:/")):
        super().__init__() 
        index = fileLocation.get().rfind(".")
        if index == -1:
            self.addError("File extension missing!")
        else:
            fileType = fileLocation.get()[index:]
            if fileType in [".txt", ".png", ".jpg", ".jpeg"]:
                if os.path.exists(fileLocation.get()):
                    self.fileLocation = fileLocation
                else:
                    self.addError(f"File {fileLocation.get()} doesn't exist!")
            else:
                self.addError(f"File extension {fileType} invalid! (for safety reasons)")
        return None
    def get(self):
        # TO-DO: finish 
        pass



'''Units'''

class Unit(Node):
    '''
        A class for all types of Units to inherit from.
    '''
    pass


class Angle(Unit):
    '''
        A class for all types of Angle units to inherit from.
    '''
    pass

class Degrees(Angle):
    '''
        A unit of angle, representing 1/360th of a circle.
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


class Pixel(Unit):
    pass


class Time(Unit):
    '''
        A class for all types of Time units to inherit from.
    '''
    pass

class Milliseconds(Time):
    '''
        A unit of time, representing 1/1000th of a second.
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
