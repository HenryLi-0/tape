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
    def getError(self):
        return self.errors
        
class Node:
    IN = None   # FORMAT: IN = [[[type, types, etc], required], etc] (-1 for required = infinite inputs of that type)
    OUT = None  # FORMAT: OUT = [type, types, etc]
    def __init__(self):
        self.id = uuid.uuid4()
        self.error = ActiveError()
    def addError(self, error):
        self.error.addError(f"{self.id}\n   {error}")
    def getError(self):
        return self.error
    def set(self):
        pass
    def get(self):
        return None

'''SIMPLE/BASIC'''

class Number(Node):
    '''
        A number.
    '''
    def __init__(self, start:int|float = None):
        super().__init__()
        self.number = None
        self.set(start)
    def set(self, start:int|float = None):
        self.number = start
    def get(self) -> int|float:
        return self.number

class Boolean(Node):
    '''
        A boolean.
    '''
    def __init__(self, boolean:bool):
        super().__init__()
        self.boolean = None
        self.set(boolean)
    def set(self, boolean:bool):
        self.boolean = boolean
    def get(self) -> bool:
        return self.boolean
    
class String(Node):
    '''
        A string.
    '''
    def __init__(self, string:str):
        super().__init__()
        self.string = None
        self.set(string)
    def set(self, string:str):
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
    IN = [[[Number], False], [[Number], False], [[Boolean], False]]
    OUT = [Number]
    def __init__(self, lowerLimit:Number = Number(0), upperLimit:Number = Number(1), onlyIntegers:Boolean = Boolean(False)):
        super().__init__()
        self.output = Number(0)
        self.set(lowerLimit, upperLimit, onlyIntegers)
    def set(self, lowerLimit:Number = Number(0), upperLimit:Number = Number(1), onlyIntegers:Boolean = Boolean(False)):
        self.lowerLimit = lowerLimit
        self.upperLimit = upperLimit
        self.onlyIntegers = onlyIntegers
    def get(self) -> Number:
        try:
            if self.lowerLimit.get() == self.upperLimit.get():
                self.output.set(self.lowerLimit.get())
            elif self.onlyIntegers.get():
                self.output.set(random.randint(self.lowerLimit.get(), self.upperLimit.get()))
            else:
                self.output.set(random.random()*(self.upperLimit.get()-self.lowerLimit.get())+self.lowerLimit.get())
            return self.output
        except:
            self.addError("Random number failed to generate!")

class FileLocation(Node):
    '''
        A file or directory location.

        Requires:
        - `location` represents the file location
    '''
    IN = [[[String], True]]
    OUT = [String]
    def __init__(self, location:String):
        super().__init__()
        self.fileLocation = None
        self.extension = None
        self.output = String(None)
        self.set(location)
    def set(self, location:String): # TO-DO: CONSIDER MOVING THIS, MAYBE, MAYBE NOT (SAFE FILE HANDLING IS IMPORTANT)
        index = location.get().rfind(".")
        if index == -1:
            if os.path.exists(location.get()):
                self.fileLocation = location.get()
                self.extension = "/folder"
            else:
                self.addError(f"Directory {location.get()} doesn't exist!")
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
    def get(self) -> String:
        if self.fileLocation != None:
            self.output.set(self.fileLocation)
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
    IN = [[[Number, Angle], True]]
    OUT = [Number]
    def __init__(self, angle:Angle|Number = Number(0)):
        super().__init__()
        self.output = Number(0)
        self.set(angle)
    def set(self, angle:Angle|Number = Number(0)):
        self.angle = angle
    def get(self) -> Number:
        if type(self.angle) == Number:      self.output.set(self.angle.get())
        elif type(self.angle) == Degrees:   self.output.set(self.angle.get().get())
        elif type(self.angle) == Radians:   self.output.set(self.angle.get().get()/math.pi*180)
        else: self.addError("Invalid input!")
        return self.output

class Radians(Angle):
    '''
        A unit of angle, where 2*PI radians represents a complete circle.

        Requires:
        - `angle` is either a Time type or a Number type object. Angle types will be converted, while Numbers will be in radians.
    '''
    IN = [[[Number, Angle], True]]
    OUT = [Number]
    def __init__(self, angle:Angle|Number = Number(0)):
        super().__init__()
        self.output = Number(0)
        self.set(angle)
    def set(self, angle:Angle|Number = Number(0)):
        self.angle = angle
    def get(self) -> Number:
        if type(self.angle) == Number:      self.output.set(self.angle.get())
        elif type(self.angle) == Degrees:   self.output.set(self.angle.get().get()/180*math.pi)
        elif type(self.angle) == Radians:   self.output.set(self.angle.get().get())
        else: self.addError("Invalid input!")
        return self.output

class Distance(Unit):
    '''
        A class for all types of Distance units to inherit from.
    '''
    def simplify(unit):
        return Pixel(unit)

class Pixel(Unit):
    '''
        A unit of measurement, where one pixel represents one screen pixel.

        Requires:
        - `angle` is either a Time type or a Number type object. Angle types will be converted, while Numbers will be in radians.
    '''
    IN = [[[Number, Distance], True]]
    OUT = [Number]
    def __init__(self, distance:Distance|Number = Number(0)):
        super().__init__()
        self.output = Number(0)
        self.set(distance)
    def set(self, distance:Distance|Number = Number(0)):
        self.distance = distance
    def get(self) -> Number:
        if type(self.distance) == Number:   self.output.set(self.distance.get())
        elif type(self.distance) == Pixel:  self.output.set(self.distance.get().get())
        else: self.addError("Invalid input!")
        return self.output

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
    IN = [[[Number, Time], True]]
    OUT = [Number]
    def __init__(self, time:Time|Number = Number(0)):
        super().__init__()
        self.output = Number(0)
        self.set(time)
    def set(self, time:Time|Number = Number(0)):
        self.time = time
    def get(self) -> Number:
        if type(self.time) == Number:           self.output.set(self.time.get())
        elif type(self.time) == Milliseconds:   self.output.set(self.time.get().get())
        elif type(self.time) == Seconds:        self.output.set(self.time.get().get()*1000)
        elif type(self.time) == Minutes:        self.output.set(self.time.get().get()*1000*60)
        elif type(self.time) == Hours:          self.output.set(self.time.get().get()*1000*60*60)
        elif type(self.time) == Days:           self.output.set(self.time.get().get()*1000*60*60*24)
        else: self.addError("Invalid input!")
        return self.output

class Seconds(Time):
    '''
        A unit of time, representing a second.

        Requires:
        - `time` is either a Time type or a Number type object. Time types will be converted, while Numbers will be in seconds.
    '''
    IN = [[[Number, Time], True]]
    OUT = [Number]
    def __init__(self, time:Time|Number = Number(0)):
        super().__init__()
        self.output = Number(0)
        self.set(time)
    def set(self, time:Time|Number = Number(0)):
        self.time = time
    def get(self) -> Number:
        if type(self.time) == Number:           self.output.set(self.time.get())
        elif type(self.time) == Milliseconds:   self.output.set(self.time.get().get()/1000)
        elif type(self.time) == Seconds:        self.output.set(self.time.get().get())
        elif type(self.time) == Minutes:        self.output.set(self.time.get().get()*60)
        elif type(self.time) == Hours:          self.output.set(self.time.get().get()*60*60)
        elif type(self.time) == Days:           self.output.set(self.time.get().get()*60*60*24)
        else: self.addError("Invalid input!")
        return self.output

class Minutes(Time):
    '''
        A unit of time, representing a minute.

        Requires:
        - `time` is either a Time type or a Number type object. Time types will be converted, while Numbers will be in minutes.
    '''
    IN = [[[Number, Time], True]]
    OUT = [Number]
    def __init__(self, time:Time|Number = Number(0)):
        super().__init__()
        self.output = Number(0)
        self.set(time)
    def set(self, time:Time|Number = Number(0)):
        self.time = time
    def get(self) -> Number:
        if type(self.time) == Number:           self.output.set(self.time.get())
        elif type(self.time) == Milliseconds:   self.output.set(self.time.get().get()/1000/60)
        elif type(self.time) == Seconds:        self.output.set(self.time.get().get()/60)
        elif type(self.time) == Minutes:        self.output.set(self.time.get().get())
        elif type(self.time) == Hours:          self.output.set(self.time.get().get()*60)
        elif type(self.time) == Days:           self.output.set(self.time.get().get()*60*24)
        else: self.addError("Invalid input!")
        return self.output

class Hours(Time):
    '''
        A unit of time, representing an hour.

        Requires:
        - `time` is either a Time type or a Number type object. Time types will be converted, while Numbers will be in hours.
    '''
    IN = [[[Number, Time], True]]
    OUT = [Number]
    def __init__(self, time:Time|Number = Number(0)):
        super().__init__()
        self.output = Number(0)
        self.set(time)
    def set(self, time:Time|Number = Number(0)):
        self.time = time
    def get(self) -> Number:
        if type(self.time) == Number:           self.output.set(self.time.get())
        elif type(self.time) == Milliseconds:   self.output.set(self.time.get().get()/1000/60/60)
        elif type(self.time) == Seconds:        self.output.set(self.time.get().get()/60/60)
        elif type(self.time) == Minutes:        self.output.set(self.time.get().get()/60)
        elif type(self.time) == Hours:          self.output.set(self.time.get().get())
        elif type(self.time) == Days:           self.output.set(self.time.get().get()*24)
        else: self.addError("Invalid input!")
        return self.output

class Days(Time):
    '''
        A unit of time, representing a day.

        Requires:
        - `time` is either a Time type or a Number type object. Time types will be converted, while Numbers will be in days.
    '''
    IN = [[[Number, Time], True]]
    OUT = [Number]
    def __init__(self, time:Time|Number = Number(0)):
        super().__init__()
        self.output = Number(0)
        self.set(time)
    def set(self, time:Time|Number = Number(0)):
        self.time = time
    def get(self) -> Number:
        if type(self.time) == Number:           self.output.set(self.time.get())
        elif type(self.time) == Milliseconds:   self.output.set(self.time.get().get()/1000/60/60/24)
        elif type(self.time) == Seconds:        self.output.set(self.time.get().get()/60/60/24)
        elif type(self.time) == Minutes:        self.output.set(self.time.get().get()/60/24)
        elif type(self.time) == Hours:          self.output.set(self.time.get().get()/24)
        elif type(self.time) == Days:           self.output.set(self.time.get().get())
        else: self.addError("Invalid input!")
        return self.output

'''IO'''

class ImageWrapper:
    '''
        A wrapper for a PIL image.
    '''
    def __init__(self, img:Image = None):
        if img != None:
            self.set(img)
    def set(self, img:Image):
        self.image = img
    def get(self):
        return self.image

class ImageImport(Node):
    '''
        Imports an image file at the given file location/path.

        Requires:
        - `location` represents the image's file location.
    '''
    IN = [[[FileLocation], True]]
    OUT = [ImageWrapper]
    def __init__(self, location:FileLocation):
        super().__init__()
        self.img = ImageWrapper()
        self.set(location)
    def set(self, location:FileLocation):
        self.location = location
    def get(self) -> ImageWrapper:
        if self.location.extension in [".png", ".jpg", ".jpeg"]:
            self.img.set(Image.open(self.location.get()).convert("RGBA"))
        else:
            self.addError(f"File extension {self.location.extension} is not a supported image file type!")
        return self.img

class FolderImport(Node):
    '''
        Imports an iterable series of images, given a folder location/path.

        Requires:
        - `location` represents the folder containing the image files.
    '''
    IN = [[[FileLocation], True]]
    OUT = None # TO-DO: FINISH
    def __init__(self, location:FileLocation):
        super().__init__()
        
        self.set(location)
    def set(self, location:FileLocation):
        if location.extension == "/folder":
            directory = location.get()
            # TO-DO: finish, and make sure its safe
        else:
            self.addError(f"The file location isn't a folder/directory!")
    def get(self) -> Image:
        pass # TO-DO: FINISH


'''LOGIC'''

class Reroute(Node):
    '''
        Returns the same node that was given in.

        Requires:
        - `inputNode` represents any node type.
    '''
    IN = [[[Node], True]]
    OUT = [Node]
    def __init__(self, inputNode:Node):
        super().__init__()
        self.inputNode = None
        self.set(self, inputNode)
    def set(self, inputNode:Node):
        self.inputNode = inputNode
    def get(self):
        return self.inputNode

class LogicalOperation(Node):
    '''
        A class for all types of logical operations related with booleans.
    '''
    def get(self) -> Boolean:
        pass

class LessThan(LogicalOperation):
    '''
        Compares two values and outputs a Boolean with the truth value of `inputA` being less than `inputB`.

        Requires:
        - `inputA` represents the first value to be compared.
        - `inputB` represents the second value to be compared.
    '''
    IN = [[[Number, Unit], True], [[Number, Unit], True]]
    OUT = [Boolean]
    def __init__(self, inputA:Number|Unit, inputB:Number|Unit):
        super().__init__()
        self.output = Boolean(False)
        self.set(inputA, inputB)
    def set(self, inputA:Number|Unit, inputB:Number|Unit):
        self.inputA = inputA
        self.inputB = inputB
    def get(self) -> Boolean:
        if type(self.inputA) == type(self.inputB):
            if type(self.inputA) == Number:
                self.output.set(self.inputA.get() < self.inputB.get())
            elif type(self.inputA) == Unit:
                a = self.inputA.simplify()
                b = self.inputB.simplify()
                if type(a) == type(b):
                    self.output.set(a.get() < b.get())
                else:
                    self.addError(f"Inconsistent Unit dimensions {type(a)} and {type(b)}!")
        else:
            self.addError("Inconsistent type for comparison!")
        return self.output

class GreaterThan(LogicalOperation):
    '''
        Compares two values and outputs a Boolean with the truth value of `inputA` being greater than `inputB`.

        Requires:
        - `inputA` represents the first value to be compared.
        - `inputB` represents the second value to be compared.
    '''
    IN = [[[Number, Unit], True], [[Number, Unit], True]]
    OUT = [Boolean]
    def __init__(self, inputA:Number|Unit, inputB:Number|Unit):
        super().__init__()
        self.output = Boolean(False)
        self.set(inputA, inputB)
    def set(self, inputA:Number|Unit, inputB:Number|Unit):
        self.inputA = inputA
        self.inputB = inputB
    def get(self) -> Boolean:
        if type(self.inputA) == type(self.inputB):
            if type(self.inputA) == Number:
                self.output.set(self.inputA.get() > self.inputB.get())
            elif type(self.inputA) == Unit:
                a = self.inputA.simplify()
                b = self.inputB.simplify()
                if type(a) == type(b):
                    self.output.set(a.get() > b.get())
                else:
                    self.addError(f"Inconsistent Unit dimensions {type(a)} and {type(b)}!")
        else:
            self.addError("Inconsistent type for comparison!")
        return self.output

class EqualTo(LogicalOperation):
    '''
        Compares two values and outputs a Boolean with the truth value of `inputA` being equal to `inputB`.

        Requires:
        - `inputA` represents the first value to be compared.
        - `inputB` represents the second value to be compared.
    '''
    IN = [[[Number, Unit], True], [[Number, Unit], True]]
    OUT = [Boolean]
    def __init__(self, inputA:Number|Unit, inputB:Number|Unit):
        super().__init__()
        self.output = Boolean(False)
        self.set(inputA, inputB)
    def set(self, inputA:Number|Unit, inputB:Number|Unit):
        self.inputA = inputA
        self.inputB = inputB
    def get(self) -> Boolean:
        if type(self.inputA) == type(self.inputB):
            if type(self.inputA) == Number:
                self.output = Boolean(self.inputA.get() == self.inputB.get())
            elif type(self.inputA) == Unit:
                a = self.inputA.simplify()
                b = self.inputB.simplify()
                if type(a) == type(b):
                    self.output = Boolean(a.get() == b.get())
                else:
                    self.addError(f"Inconsistent Unit dimensions {type(a)} and {type(b)}!")
        else:
            self.addError("Inconsistent type for comparison!")
        return self.output
    
class And(LogicalOperation):
    '''
        Compares two Booleans and outputs a Boolean if both `inputA` and `inputB` are True.

        Requires:
        - `inputA` represents the first boolean.
        - `inputB` represents the second boolean.
    '''
    IN = [[[Boolean], True], [[Boolean], True]]
    OUT = [Boolean]
    def __init__(self, inputA:Boolean, inputB:Boolean):
        super().__init__()
        self.output = Boolean(False)
        self.set(inputA, inputB)
    def set(self, inputA:Boolean, inputB:Boolean):
        self.inputA = inputA
        self.inputB = inputB
    def get(self) -> Boolean:
        self.output.set(self.inputA.get() and self.inputB.get())
        return self.output

class Or(LogicalOperation):
    '''
        Compares two Booleans and outputs a Boolean if at least one `inputA` and `inputB` are True.

        Requires:
        - `inputA` represents the first boolean.
        - `inputB` represents the second boolean.
    '''
    IN = [[[Boolean], True], [[Boolean], True]]
    OUT = [Boolean]
    def __init__(self, inputA:Boolean, inputB:Boolean):
        super().__init__()
        self.output = Boolean(False)
        self.set(inputA, inputB)
    def set(self, inputA:Boolean, inputB:Boolean):
        self.inputA = inputA
        self.inputB = inputB
    def get(self) -> Boolean:
        self.output.set(self.inputA.get() or self.inputB.get())
        return self.output

class Not(LogicalOperation):
    '''
        Returns the inverted truth value of the given Boolean.

        Requires:
        - `inputNode` represents a boolean.
    '''
    IN = [[[Boolean], True]]
    OUT = [Boolean]
    def __init__(self, inputNode:Boolean):
        super().__init__()
        self.output = Boolean(True)
        self.set(inputNode)
    def set(self, inputNode:Boolean):
        self.inputNode = inputNode
    def get(self) -> Boolean:
        self.output.set(not(self.inputNode.get()))
        return self.output

class If(LogicalOperation):
    '''
        Returns `inputTrue` if `boolean` is true, otherwise returns `inputFalse`.
        
        Requires:
        - `inputTrue` represents the first node.
        - `inputFalse` represents the second node.
        - `boolean` represents a Boolean.
    '''
    IN = [[[Node], True], [[Node], True], [[Boolean], True]]
    OUT = [Node]
    def __init__(self, inputTrue:Node, inputFalse:Node, boolean:Boolean):
        super().__init__()
        self.output = None
        self.set(inputTrue, inputFalse, boolean)
    def set(self, inputTrue:Node, inputFalse:Node, boolean:Boolean):
        self.inputTrue = inputTrue
        self.inputFalse = inputFalse
        self.boolean = boolean
    def get(self):
        if self.boolean.get(): return self.inputTrue
        else: return self.inputFalse
