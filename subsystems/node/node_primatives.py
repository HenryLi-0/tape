from subsystems.node.node_functional import *

from subsystems.point import *
from subsystems.pathing import *
import random, uuid, os, math
from PIL import Image


'''NODE'''

class Node:
    def __init__(self):
        self.__id = uuid.uuid4()
        self.__error = ActiveError()
    def addError(self, error):
        self.__error.addError(f"{self.id}\n   {error}")
    def set(self):
        pass
    def update(self):
        return None
    
    @property
    def id(self): return self.__id
    @property
    def error(self): return self.__error
    

'''SIMPLE/BASIC'''
@Input()
@Display("Value", True, None)
@Output("Value", -1, lambda self: self)
class Number(Node):
    '''
        A number.
    '''
    def __init__(self, start:int|float = None):
        super().__init__()
        self.__value = None
        self.set(start)
    def set(self, start:int|float = None):
        self.__value = start

    @property
    def value(self) -> int|float: return self.__value

@Input()
@Display("Value", True, None)
@Output("Value", -1, lambda self: self)
class Boolean(Node):
    '''
        A boolean.
    '''
    def __init__(self, boolean:bool):
        super().__init__()
        self.__value = None
        self.set(boolean)
    def set(self, boolean:bool):
        self.__value = boolean
    
    @property
    def value(self) -> bool: return self.__value

@Input()
@Display("Value", True, None)
@Output("Value", -1, lambda self: self)
class String(Node):
    '''
        A string.
    '''
    def __init__(self, string:str):
        super().__init__()
        self.__value = None
        self.set(string)
    def set(self, string:str):
        self.__value = string
    
    @property
    def value(self) -> str: return self.__value
    
    

@Input("Lower Limit", [Number], False)
@Input("Upper Limit", [Number], False)
@Input("Only Integers", [Boolean], False)
@Display("Range", False, lambda self: f"[{self.__lowerLimit.value}, {self.__upperLimit.value}]")
@Display("Only Integers", False, lambda self: self.__onlyIntegers.value)
@Display("Random Number", False, lambda self: self.output.value)
@Output("Random Number", Number, lambda self: self.output)
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
        self.__output = Number(0)
        self.set(lowerLimit, upperLimit, onlyIntegers)
    def set(self, lowerLimit:Number = Number(0), upperLimit:Number = Number(1), onlyIntegers:Boolean = Boolean(False)):
        self.__lowerLimit = lowerLimit
        self.__upperLimit = upperLimit
        self.__onlyIntegers = onlyIntegers
        self.update()
    def update(self):
        try:
            if self.__lowerLimit.value == self.__upperLimit.value:
                self.__output.set(self.__lowerLimit.value)
            elif self.__onlyIntegers.value:
                self.__output.set(random.randint(self.__lowerLimit.value, self.__upperLimit.value))
            else:
                self.__output.set(random.random()*(self.__upperLimit.value-self.__lowerLimit.value)+self.__lowerLimit.value)
        except:
            self.addError("Random number failed to generate!")
    
    @property
    def output(self) -> Number: 
        return self.__output


@Input("File Location", [String], True)
@Display("Valid File", False, lambda self: self.fileLocation)
@Output("Valid File", String, lambda self: self.fileLocation)
class FileLocation(Node):
    '''
        A file or directory location.

        Requires:
        - `location` represents the file location
    '''
    def __init__(self, location:String):
        super().__init__()
        self.__fileLocation = None
        self.__extension = None
        self.__output = String(None)
        self.set(location)
    def set(self, location:String): # TO-DO: CONSIDER MOVING THIS, MAYBE, MAYBE NOT (SAFE FILE HANDLING IS IMPORTANT)
        index = location.value.rfind(".")
        if index == -1:
            if os.path.exists(location.value):
                self.__fileLocation = location.value
                self.__extension = "/folder"
            else:
                self.addError(f"Directory {location.value} doesn't exist!")
        else:
            fileType = location.value[index:]
            if fileType in [".txt", ".png", ".jpg", ".jpeg"]:
                if os.path.exists(location.value):
                    self.__fileLocation = location
                    self.__extension = fileType
                else:
                    self.addError(f"File {location.value} doesn't exist!")
            else:
                self.addError(f"File extension {fileType} invalid! (for safety reasons)")
        self.update()
    def update(self):
        if self.__fileLocation != None:
            self.__output.set(self.__fileLocation)
    
    @property
    def fileLocation(self) -> String: return self.__fileLocation


'''UNITS'''

class Unit(Node):
    '''
        A class for all types of Units to inherit from.
    '''
    def __init__(self):
        super().__init__()
        self.__output = None
    def simplify(unit): # TO-DO: COMPLETE, BUT MAKE IT MORE EFFICIENT!
        '''
            Turns a unit to its simpliest form, consist with all other simplified version.
        '''
        pass

    @property
    def output(self) -> Number: 
        return self.__output

class Angle(Unit):
    '''
        A class for all types of Angle units to inherit from.
    '''
    def __init__(self):
        super().__init__()
    def simplify(unit):
        return Degrees(unit)

@Input("Angle", [Number, Angle], True)
@Display("Value", False, lambda self: self.output.value)
@Output("Angle", Number, lambda self: self.output)
class Degrees(Angle):
    '''
        A unit of angle, representing 1/360th of a circle.

        Requires:
        - `angle` is either a Angle type or a Number type object. Angle types will be converted, while Numbers will be in degrees.
    '''
    def __init__(self, angle:Angle|Number = Number(0)):
        super().__init__()
        self.__output = Number(0)
        self.set(angle)
    def set(self, angle:Angle|Number = Number(0)):
        self.__angle = angle
        self.update()
    def update(self):
        if type(self.__angle) == Number:      self.__output.set(self.__angle.value)
        elif type(self.__angle) == Degrees:   self.__output.set(self.__angle.output.value)
        elif type(self.__angle) == Radians:   self.__output.set(self.__angle.output.value/math.pi*180)
        else: self.addError("Invalid input!")

@Input("Angle", [Number, Angle], True)
@Display("Value", False, lambda self: self.output.value)
@Output("Angle", Number, lambda self: self.output)
class Radians(Angle):
    '''
        A unit of angle, where 2*PI radians represents a complete circle.

        Requires:
        - `angle` is either a Time type or a Number type object. Angle types will be converted, while Numbers will be in radians.
    '''
    def __init__(self, angle:Angle|Number = Number(0)):
        super().__init__()
        self.__output = Number(0)
        self.set(angle)
    def set(self, angle:Angle|Number = Number(0)):
        self.__angle = angle
        self.update()
    def update(self):
        if type(self.__angle) == Number:      self.__output.set(self.__angle.value)
        elif type(self.__angle) == Degrees:   self.__output.set(self.__angle.output.value/180*math.pi)
        elif type(self.__angle) == Radians:   self.__output.set(self.__angle.output.value)
        else: self.addError("Invalid input!")
        return self.__output

class Distance(Unit):
    '''
        A class for all types of Distance units to inherit from.
    '''
    def __init__(self):
        super().__init__()
    def simplify(unit):
        return Pixel(unit)

@Input("Distance", [Number, Distance], True)
@Display("Value", False, lambda self: self.output.value)
@Output("Distance", Number, lambda self: self.output)
class Pixel(Distance):
    '''
        A unit of measurement, where one pixel represents one screen pixel.

        Requires:
        - `angle` is either a Time type or a Number type object. Angle types will be converted, while Numbers will be in radians.
    '''
    def __init__(self, distance:Distance|Number = Number(0)):
        super().__init__()
        self.__output = Number(0)
        self.set(distance)
    def set(self, distance:Distance|Number = Number(0)):
        self.__distance = distance
        self.update()
    def update(self):
        if type(self.__distance) == Number:   self.__output.set(self.__distance.value)
        elif type(self.__distance) == Pixel:  self.__output.set(self.__distance.output.value)
        else: self.addError("Invalid input!")

class Time(Unit):
    '''
        A class for all types of Time units to inherit from.
    '''
    def simplify(unit):
        return Seconds(unit)

@Input("Time", [Number, Time], True)
@Display("Value", False, lambda self: self.output.value)
@Output("Time", Number, lambda self: self.output)
class Milliseconds(Time):
    '''
        A unit of time, representing 1/1000th of a second.

        Requires:
        - `time` is either a Time type or a Number type object. Time types will be converted, while Numbers will be in milliseconds.
    '''
    def __init__(self, time:Time|Number = Number(0)):
        super().__init__()
        self.__output = Number(0)
        self.set(time)
    def set(self, time:Time|Number = Number(0)):
        self.time = time
        self.update()
    def update(self):
        if type(self.time) == Number:           self.__output.set(self.time.value)
        elif type(self.time) == Milliseconds:   self.__output.set(self.time.output.value)
        elif type(self.time) == Seconds:        self.__output.set(self.time.output.value*1000)
        elif type(self.time) == Minutes:        self.__output.set(self.time.output.value*1000*60)
        elif type(self.time) == Hours:          self.__output.set(self.time.output.value*1000*60*60)
        elif type(self.time) == Days:           self.__output.set(self.time.output.value*1000*60*60*24)
        else: self.addError("Invalid input!")

@Input("Time", [Number, Time], True)
@Display("Value", False, lambda self: self.output.value)
@Output("Time", Number, lambda self: self.output)
class Seconds(Time):
    '''
        A unit of time, representing a second.

        Requires:
        - `time` is either a Time type or a Number type object. Time types will be converted, while Numbers will be in seconds.
    '''
    def __init__(self, time:Time|Number = Number(0)):
        super().__init__()
        self.__output = Number(0)
        self.set(time)
    def set(self, time:Time|Number = Number(0)):
        self.time = time
        self.update()
    def update(self):
        if type(self.time) == Number:           self.__output.set(self.time.value)
        elif type(self.time) == Milliseconds:   self.__output.set(self.time.output.value/1000)
        elif type(self.time) == Seconds:        self.__output.set(self.time.output.value)
        elif type(self.time) == Minutes:        self.__output.set(self.time.output.value*60)
        elif type(self.time) == Hours:          self.__output.set(self.time.output.value*60*60)
        elif type(self.time) == Days:           self.__output.set(self.time.output.value*60*60*24)
        else: self.addError("Invalid input!")

@Input("Time", [Number, Time], True)
@Display("Value", False, lambda self: self.output.value)
@Output("Time", Number, lambda self: self.output)
class Minutes(Time):
    '''
        A unit of time, representing a minute.

        Requires:
        - `time` is either a Time type or a Number type object. Time types will be converted, while Numbers will be in minutes.
    '''
    def __init__(self, time:Time|Number = Number(0)):
        super().__init__()
        self.__output = Number(0)
        self.set(time)
    def set(self, time:Time|Number = Number(0)):
        self.time = time
        self.update()
    def update(self):
        if type(self.time) == Number:           self.__output.set(self.time.value)
        elif type(self.time) == Milliseconds:   self.__output.set(self.time.output.value/1000/60)
        elif type(self.time) == Seconds:        self.__output.set(self.time.output.value/60)
        elif type(self.time) == Minutes:        self.__output.set(self.time.output.value)
        elif type(self.time) == Hours:          self.__output.set(self.time.output.value*60)
        elif type(self.time) == Days:           self.__output.set(self.time.output.value*60*24)
        else: self.addError("Invalid input!")

@Input("Time", [Number, Time], True)
@Display("Value", False, lambda self: self.output.value)
@Output("Time", Number, lambda self: self.output)
class Hours(Time):
    '''
        A unit of time, representing an hour.

        Requires:
        - `time` is either a Time type or a Number type object. Time types will be converted, while Numbers will be in hours.
    '''
    def __init__(self, time:Time|Number = Number(0)):
        super().__init__()
        self.__output = Number(0)
        self.set(time)
    def set(self, time:Time|Number = Number(0)):
        self.time = time
        self.update()
    def update(self):
        if type(self.time) == Number:           self.__output.set(self.time.value)
        elif type(self.time) == Milliseconds:   self.__output.set(self.time.output.value/1000/60/60)
        elif type(self.time) == Seconds:        self.__output.set(self.time.output.value/60/60)
        elif type(self.time) == Minutes:        self.__output.set(self.time.output.value/60)
        elif type(self.time) == Hours:          self.__output.set(self.time.output.value)
        elif type(self.time) == Days:           self.__output.set(self.time.output.value*24)
        else: self.addError("Invalid input!")

@Input("Time", [Number, Time], True)
@Display("Value", False, lambda self: self.output.value)
@Output("Time", Number, lambda self: self.output)
class Days(Time):
    '''
        A unit of time, representing a day.

        Requires:
        - `time` is either a Time type or a Number type object. Time types will be converted, while Numbers will be in days.
    '''
    def __init__(self, time:Time|Number = Number(0)):
        super().__init__()
        self.__output = Number(0)
        self.set(time)
    def set(self, time:Time|Number = Number(0)):
        self.time = time
        self.update()
    def update(self):
        if type(self.time) == Number:           self.__output.set(self.time.value)
        elif type(self.time) == Milliseconds:   self.__output.set(self.time.output.value/1000/60/60/24)
        elif type(self.time) == Seconds:        self.__output.set(self.time.output.value/60/60/24)
        elif type(self.time) == Minutes:        self.__output.set(self.time.output.value/60/24)
        elif type(self.time) == Hours:          self.__output.set(self.time.output.value/24)
        elif type(self.time) == Days:           self.__output.set(self.time.output.value)
        else: self.addError("Invalid input!")

'''IO'''

class ImageWrapper:
    '''
        A wrapper for a PIL image.
    '''
    def __init__(self, img:Image = None):
        if img != None:
            self.set(img)
    def set(self, img:Image):
        self.__image = img

    @property
    def image(self) -> Image: return self.__image

@Input("File Location", [FileLocation], True)
@Display("Image", False, lambda self: self.__valid)
@Output("Image", ImageWrapper, lambda self: self.image)
class ImageImport(Node):
    '''
        Imports an image file at the given file location/path.

        Requires:
        - `location` represents the image's file location.
    '''
    def __init__(self, location:FileLocation):
        super().__init__()
        self.__img = ImageWrapper()
        self.__valid = False
        self.set(location)
    def set(self, location:FileLocation):
        self.__location = location
        self.update()
    def update(self):
        if self.__location.__extension in [".png", ".jpg", ".jpeg"]:
            self.__img.set(Image.open(self.__location.fileLocation).convert("RGBA"))
            self.__valid = True
        else:
            self.addError(f"File extension {self.__location.__extension} is not a supported image file type!")
            self.__valid = False
    
    @property
    def image(self) -> ImageWrapper:
        self.update()
        return self.__img
    @property
    def valid(self) -> bool:
        self.update()
        return self.__valid

@Input("Directory", [FileLocation], True)
# @Display("Items", False, lambda self: None)
# @Output(None, None) #TO-DO: FINISH
class FolderImport(Node):
    '''
        Imports an iterable series of images, given a folder location/path.

        Requires:
        - `location` represents the folder containing the image files.
    '''
    def __init__(self, location:FileLocation):
        super().__init__()
        
        self.set(location)
    def set(self, location:FileLocation):
        if location.__extension == "/folder":
            directory = location.fileLocation
            # TO-DO: finish, and make sure its safe
        else:
            self.addError(f"The file location isn't a folder/directory!")
    def update(self):
        pass # TO-DO: FINISH


'''LOGIC'''

@Input("Node", [Node], True)
@Display()
@Output("Node", Node, lambda self: self.node)
class Reroute(Node):
    '''
        Returns the same node that was given in.

        Requires:
        - `inputNode` represents any node type.
    '''
    def __init__(self, inputNode:Node):
        super().__init__()
        self.__inputNode = None
        self.set(self, inputNode)
    def set(self, inputNode:Node):
        self.__inputNode = inputNode

    @property
    def node(self) -> Node: return self.__inputNode

class LogicalOperation(Node):
    '''
        A class for all types of logical operations related with booleans.
    '''
    def update(self):
        pass

@Input("A", [Number, Unit], True)
@Input("B", [Number, Unit], True)
@Display("Value", False, lambda self: self.output.value)
@Output("Logic", Boolean, lambda self: self.output)
class LessThan(LogicalOperation):
    '''
        Compares two values and outputs a Boolean with the truth value of `inputA` being less than `inputB`.

        Requires:
        - `inputA` represents the first value to be compared.
        - `inputB` represents the second value to be compared.
    '''
    def __init__(self, inputA:Number|Unit, inputB:Number|Unit):
        super().__init__()
        self.__output = Boolean(False)
        self.set(inputA, inputB)
    def set(self, inputA:Number|Unit, inputB:Number|Unit):
        self.__inputA = inputA
        self.__inputB = inputB
        self.update()
    def update(self):
        if type(self.__inputA) == type(self.__inputB):
            if type(self.__inputA) == Number:
                self.__output.set(self.__inputA.value < self.__inputB.value)
            elif type(self.__inputA) == Unit:
                a = self.__inputA.simplify()
                b = self.__inputB.simplify()
                if type(a) == type(b):
                    self.__output.set(a.get() < b.get())
                else:
                    self.addError(f"Inconsistent Unit dimensions {type(a)} and {type(b)}!")
        else:
            self.addError("Inconsistent type for comparison!")
    
    @property
    def output(self) -> Boolean:
        self.update()
        return self.__output

@Input("A", [Number, Unit], True)
@Input("B", [Number, Unit], True)
@Display("Value", False, lambda self: self.output.value)
@Output("Logic", Boolean, lambda self: self.output)
class GreaterThan(LogicalOperation):
    '''
        Compares two values and outputs a Boolean with the truth value of `inputA` being greater than `inputB`.

        Requires:
        - `inputA` represents the first value to be compared.
        - `inputB` represents the second value to be compared.
    '''
    def __init__(self, inputA:Number|Unit, inputB:Number|Unit):
        super().__init__()
        self.__output = Boolean(False)
        self.set(inputA, inputB)
    def set(self, inputA:Number|Unit, inputB:Number|Unit):
        self.__inputA = inputA
        self.__inputB = inputB
        self.update()
    def update(self):
        if type(self.__inputA) == type(self.__inputB):
            if type(self.__inputA) == Number:
                self.__output.set(self.__inputA.value > self.__inputB.value)
            elif type(self.__inputA) == Unit:
                a = self.__inputA.simplify()
                b = self.__inputB.simplify()
                if type(a) == type(b):
                    self.__output.set(a.get() > b.get())
                else:
                    self.addError(f"Inconsistent Unit dimensions {type(a)} and {type(b)}!")
        else:
            self.addError("Inconsistent type for comparison!")

    @property
    def output(self) -> Boolean:
        self.update()
        return self.__output

@Input("A", [Number, Unit], True)
@Input("B", [Number, Unit], True)
@Display("Value", False, lambda self: self.output.value)
@Output("Logic", Boolean, lambda self: self.output)
class EqualTo(LogicalOperation):
    '''
        Compares two values and outputs a Boolean with the truth value of `inputA` being equal to `inputB`.

        Requires:
        - `inputA` represents the first value to be compared.
        - `inputB` represents the second value to be compared.
    '''
    def __init__(self, inputA:Number|Unit, inputB:Number|Unit):
        super().__init__()
        self.__output = Boolean(False)
        self.set(inputA, inputB)
    def set(self, inputA:Number|Unit, inputB:Number|Unit):
        self.__inputA = inputA
        self.__inputB = inputB
        self.update()
    def update(self):
        if type(self.__inputA) == type(self.__inputB):
            if type(self.__inputA) == Number:
                self.__output = Boolean(self.__inputA.value == self.__inputB.value)
            elif type(self.__inputA) == Unit:
                a = self.__inputA.simplify()
                b = self.__inputB.simplify()
                if type(a) == type(b):
                    self.__output = Boolean(a.output.value == b.output.value)
                else:
                    self.addError(f"Inconsistent Unit dimensions {type(a)} and {type(b)}!")
        else:
            self.addError("Inconsistent type for comparison!")
    
    @property
    def output(self) -> Boolean:
        self.update()
        return self.__output

@Input("A", [Boolean], True)
@Input("B", [Boolean], True)
@Display("Value", False, lambda self: self.output.value)
@Output("Logic", Boolean, lambda self: self.output)
class And(LogicalOperation):
    '''
        Compares two Booleans and outputs a Boolean if both `inputA` and `inputB` are True.

        Requires:
        - `inputA` represents the first boolean.
        - `inputB` represents the second boolean.
    '''
    def __init__(self, inputA:Boolean, inputB:Boolean):
        super().__init__()
        self.__output = Boolean(False)
        self.set(inputA, inputB)
    def set(self, inputA:Boolean, inputB:Boolean):
        self.__inputA = inputA
        self.__inputB = inputB
        self.update()
    def update(self):
        self.__output.set(self.__inputA.value and self.__inputB.value)
    
    @property
    def output(self) -> Boolean:
        self.update()
        return self.__output

@Input("A", [Boolean], True)
@Input("B", [Boolean], True)
@Display("Value", False, lambda self: self.output.value)
@Output("Logic", Boolean, lambda self: self.output)
class Or(LogicalOperation):
    '''
        Compares two Booleans and outputs a Boolean if at least one `inputA` and `inputB` are True.

        Requires:
        - `inputA` represents the first boolean.
        - `inputB` represents the second boolean.
    '''
    def __init__(self, inputA:Boolean, inputB:Boolean):
        super().__init__()
        self.__output = Boolean(False)
        self.set(inputA, inputB)
    def set(self, inputA:Boolean, inputB:Boolean):
        self.__inputA = inputA
        self.__inputB = inputB
        self.update()
    def update(self):
        self.__output.set(self.__inputA.value or self.__inputB.value)

    @property
    def output(self) -> Boolean:
        self.update()
        return self.__output

@Input("A", [Boolean], True)
@Display("Value", False, lambda self: self.output.value)
@Output("Logic", Boolean, lambda self: self.output)
class Not(LogicalOperation):
    '''
        Returns the inverted truth value of the given Boolean.

        Requires:
        - `inputNode` represents a boolean.
    '''
    def __init__(self, inputNode:Boolean):
        super().__init__()
        self.__output = Boolean(True)
        self.set(inputNode)
    def set(self, inputNode:Boolean):
        self.__inputNode = inputNode
        self.update()
    def update(self):
        self.__output.set(not(self.__inputNode.value))

    @property
    def output(self) -> Boolean:
        self.update()
        return self.__output

@Input("A", [Node], True)
@Input("B", [Node], True)
@Display("Boolean Value", False, lambda self: self.__boolean.value)
@Display("Choice", False, lambda self: "A" if self.__boolean.value else "B")
@Input("Logic", [Boolean], True)
@Output("Node", Node, lambda self: self.output)
class If(LogicalOperation):
    '''
        Returns `inputTrue` if `boolean` is true, otherwise returns `inputFalse`.
        
        Requires:
        - `inputTrue` represents the first node.
        - `inputFalse` represents the second node.
        - `boolean` represents a Boolean.
    '''
    def __init__(self, inputTrue:Node, inputFalse:Node, boolean:Boolean):
        super().__init__()
        self.__output = None
        self.set(inputTrue, inputFalse, boolean)
    def set(self, inputTrue:Node, inputFalse:Node, boolean:Boolean):
        self.__inputTrue = inputTrue
        self.__inputFalse = inputFalse
        self.__boolean = boolean
        self.update()
    def update(self):
        if self.__boolean.value: self.__output = self.__inputTrue
        else: self.__output = self.__inputFalse
    
    @property
    def output(self) -> Node: return self.__output
    
