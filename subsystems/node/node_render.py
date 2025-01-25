from subsystems.node.node_functional import *
from subsystems.node.node_primatives import *
from subsystems.node.node_pathing import *
from subsystems.node.node_operations import *

from subsystems.settings import *

# TO-DO: FINISH REFACTORING

@Output("Animation Time", Seconds, lambda self: self.output)
class AnimationTime(Node):
    '''
        Provides the animation time in a Unit of Seconds.
    '''
    def __init__(self):
        super().__init__()
        self.__time = Number(0)
        self.__output = Seconds(self.__time)
    def update(self):
        self.__time.set(ANIMATION_TIME.get())
        self.__output.update()

    @property
    def output(self): return self.__output

class RenderInstructions:
    def __init__(self):
        self.c = None
        self.r = None
        self.a = None
        self.s = None
        self.h = None
        self.t = None
        self.b = None
        self.w = None

@Input("Coordinate",    [Coordinate],   True)
@Input("Rotation",      [Number, Angle],True)
@Input("Apperance",     [ImageImport],  True)
@Input("Size",          [Number],       True)
@Input("Hue",           [Number],       True)
@Input("Transparency",  [Number],       True)
@Input("Brightness",    [Number],       True)
@Input("Weird/Blur",    [Number],       True)
@Display("Coordinate",  Coordinate,     lambda self: f"({self.coordinate.x.value}, {self.coordinate.y.value})")
@Display("Rotation",    Angle,          lambda self: f"{self.rotation.__class__}({self.rotation.output.value})")
@Display("Apperance",   ImageImport,    lambda self: self.appearance.valid)
@Display("Size",        Number,         lambda self: self.size.value)
@Display("Hue",         Number,         lambda self: self.hue.value)
@Display("Transparency",Number,         lambda self: self.transparency.value)
@Display("Brightness",  Number,         lambda self: self.brightness.value)
@Display("Weird/Blur",  Number,         lambda self: self.weird.value)
@Output("Coordinate",   Coordinate,     lambda self: self.coordinate)
@Output("Rotation",     Angle,          lambda self: self.rotation)
@Output("Apperance",    ImageImport,    lambda self: self.appearance)
@Output("Size",         Number,         lambda self: self.size)
@Output("Hue",          Number,         lambda self: self.hue)
@Output("Transparency", Number,         lambda self: self.transparency)
@Output("Brightness",   Number,         lambda self: self.brightness)
@Output("Weird/Blur",   Number,         lambda self: self.weird)
@Output("Render Instructions", RenderInstructions, lambda self: self.output)
class RenderedObject(Node):
    '''
        A rendered object, representing a set of data on the screen.

        Requires:
        - `CRASHTBW` values. Refer to `MANUAL.md` for more information.
    '''
    def __init__(self, coord:Coordinate, rotation:Number|Angle, appearance:ImageImport, size:Number, hue:Number, transparency:Number, brightness:Number, weird:Number):
        super().__init__()
        self.__output = RenderInstructions()
        self.set(coord, rotation, appearance, size, hue, transparency, brightness, weird)
    def set(self, coord:Coordinate, rotation:Number|Angle, appearance:ImageImport, size:Number, hue:Number, transparency:Number, brightness:Number, weird:Number):
        self.__coordNode = coord
        self.__rotationNode = rotation
        self.__appearanceNode = appearance
        self.__sizeNode = size
        self.__hueNode = hue
        self.__transparencyNode = transparency
        self.__brightnessNode = brightness
        self.__weirdNode = weird
        self.update()
    def update(self):
        pass

    @property
    def coordinate(self) -> Coordinate: return self.__coordNode
    @property
    def rotation(self) -> Number|Angle: return self.__rotationNode
    @property
    def appearance(self) -> ImageImport: return self.__appearanceNode
    @property
    def size(self) -> Number: return self.__sizeNode
    @property
    def hue(self) -> Number: return self.__hueNode
    @property
    def transparency(self) -> Number: return self.__transparencyNode
    @property
    def brightness(self) -> Number: return self.__brightnessNode
    @property
    def weird(self) -> Number: return self.__weirdNode
    @property
    def output(self): return self.__output

class Sprite(RenderedObject): pass

class Camera(RenderedObject): pass

@Input("Render Instructions", [RenderInstructions], True, True)
@Display("Given Instructions", False, lambda self: self.givenInstructions)
class Render(Node):
    '''
        Renders a sprite, given render instructions.
    '''
    def __init__(self, instructions:RenderInstructions):
        super().__init__()
        self.__givenInstructions = False
        self.set(instructions)
    def set(self, instructions:RenderInstructions):
        self.__instruction = instructions
        self.__givenInstructions = True
        self.update()
    def update(self):
        pass

    @property
    def instructions(self): return self.__instructions
    @property
    def givenInstructions(self): return self.__givenInstructions
    # TO-DO: TO BE ACCESSED BY ACTUAL RENDERER FOR INSTRUCTIONS