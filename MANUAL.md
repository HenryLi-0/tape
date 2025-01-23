# Tape v2.x - Usage Manual

---

Welcome to the Usage Manual for Tape v2.x! Tape v2.x is an overly unnecessary way to animate an image to move across your screen. Tape v2.x is a full rewrite of Tape v1.x, and approaches the idea in a different way!

Tape v2.x, unlike Tape v1.x, is a node based animation editor using node structures to define the animation. This means that there is a node work area, where nodes, drag-and-drop-able boxes can be placed. Most nodes have inputs and outputs, while some may only have one. Additionally, some may have fields that the user can type into or select. 


## Layout:
*This section describes the UI and possibly how to navigate to certain areas!*

- TO-DO: layout docs



## Nodes:
*This section details what each node does and what inputs/outputs/fields it uses!*

**TO-DO NEEDS TO BE UPDATED WITH NEW STUFF (EX. MUSIC, ADVANCED MUSIC, CALCULATION, ETC.)**

**Simple**
- Numbers: a number FILL IN, or removes units
  - IN:
    - Unit(Number)
    - FILL IN
  - Representation: (n)
- Random: a random number
  - IN: Number, Number (range) (optional, default 0-1)
  - OUT: a random number within range
- File Location: a file location, can be directory or file path
  - Representation: ("C:/...")
- Unit: a number with a unit, can does convert units reasonably
  - Representation: Unit(Number)
  - Varitents:
    - Angles
    - Pixels
    - Time
- Coordinate: two numbers
  - In: 
    - Number, Number (will act as percent of the screen)
    - Pixels, Pixels (will act as a precise coordinate)
    - FILL IN (will act as percent of the screen)
  - Out: (x,y) (exact coordinate)
  - Representation: (x,y)

**Operations**
- Addition:
  - In/Out: oh god
    - Number, Number -> Number+Number
    - Unit(Number), Unit(Number) -> Unit(Number)
    - Coordinate, Coordinate -> Coordinate+Coordinate
    - Frame(Number, Time), Time -> Frame(Number, Time+Time)
    - Frame(Number, Time), Number -> Frame(Number+Number, Time)
    - Frame(Angle, Time), Time -> Frame(Angle, Time+Time)
    - Frame(Angle, Time), Angle -> Frame(Angle+Angle, Time)
    - Frame(Pixel, Time), Time -> Frame(Pixel, Time+Time)
    - Frame(Pixel, Time), Pixel -> Frame(Pixel+Pixel, Time)
    - Frame(Coordinate, Time), Time -> Frame(Coordinate, Time+Time)
    - Frame(Coordinate, Time), Coordinate -> Frame(Coordinate+Coordinate, Time)
    - Path(...) + Path(...) -> Path(...) (when times overlap, values will be added)
  - Representation: +
- Multiplication:
  - In/Out: oh god
    - Number, Number -> Number*Number
    - Unit(Number), Number -> Unit(Number*Number)
    - Coordinate, Number -> Coordinate*Number
  - Representation: *

**Pathing**
- Frame: a value and time grouped
  - In: value and time
  - Out: a frame
  - Varients (for clarity):
    - Frame(Number, Time)
    - Frame(Coordinate, Time)
- Path:
  - In: n frames, same frame type, approach
    - Ex. Type, Frame(Coordinate, Time), ... -> Path(Frame(Coordinate, Time), ...) (calculated with approach)
    - Type: bezier (smooth connections through all), smooth slide ends (start slow, speed up, approach end slow), smooth slide all (smooth slide ends but its for all of them), linear (just boop boop boop, lines)
  - Optional In: Number (starting offset (default: 0)), Path(Frame(Number, Time)) (speed path (default: x1))
  - Out: a path, timed!
  - Varients:
    - Path(Frame(Number, Time), ...) (calculated with approach)
    - Path(Frame(Angle, Time), ...) (calculated with approach)
    - Path(Frame(Pixel, Time), ...) (calculated with approach)
    - Path(Frame(Coordinate, Time), ...) (calculated with approach)
- Axis Merge: converts axis paths to a single coordinate path
  - In: Path(Frame(Pixel, Time), ...), Path(Frame(Pixel, Time), ...)
  - Out: Path(Frame(Coordinate, Time), ...)
- Path At Time:
  - In: Path(Any, Time)
  - Out: Any, the value of Path(Any, Time) at Time Time
- Path Merger:
  - In: n number of paths (Path(Any, Time), ...)
  - Out: a single combined path (Path(Any, Time))

**IO**
- Image Import:
  - In: 
    - File Location (should be a single image of an image type, ex. *.PNG)
    - FILL IN
  - Out: image for use
- Folder Import:
  - In:
    - File Location (should be a directory with at least one image of an image type, ex. DIRECTORY/*.PNG)
    - Number (image index)
    - FILL IN
  - Out: image for use

**Logic**
- Time:
  - Out: Time, which is Seconds(animation time), which is of type Unit(Number)
- Reroute (all 4 rotation configs):
  - In: ANY
  - Out: IN
- Less Than:
  - In:
    - Number, Number
    - Unit(Number), Unit(Number)
  - Out:
    - truth value if input 1 is less than input 2
- Greater Than:
  - In:
    - Number, Number
    - Unit(Number), Unit(Number)
  - Out:
    - truth value if input 1 is greater than input 2
- Equal:
  - In:
    - Number, Number
    - Unit(Number), Unit(Number)
    - above, with optional tolerance (Number OR Unit(Number)) (default 0)
  - Out:
    - truth value, if input 1 is within tolerance to input 2
- And: 
  - In:
    - Boolean, Boolean
  - Out:
    - truth value of if both booleans in are True
- Or:
  - In:
    - Boolean, Boolean
  - Out:
    - truth value of if at least one of the booleans are True
- Not:
  - In:
    - Boolean
  - Out:
    - the inverted truth value of the input boolean
- If:
  - In: Truth, Any (True), Any (False) 
  - Out: Any(True) if Truth True, Any(False) if Truth not True


**Displays**
- SPRITE:
  - In:
    - CRASHTBW values
      - Coordinate (Coordinate)
      - Rotation (Number) OR Angle(Number)
      - Apperance (Image)
      - Size (Number)
      - Hue (Number)
      - Transparency (Number)
      - Brightness (Number)
      - Weird/Blur (Number)
  - Out:
    - CRASHTBW values (same as above)
- CAMERA:
  - In:
    - CRASHTBW values
      - Coordinate (Coordinate)
      - Rotation (Number) OR Angle(Number)
      - Apperance (Image)
      - Size (Number)
      - Hue (Number)
      - Transparency (Number)
      - Brightness (Number)
      - Weird/Blur (Number)
  - Out:
    - CRASHTBW values (same as above)

### Adding Custom Nodes
*This bit explains how to add your own custom nodes!*

Have or want to make and add your own custom nodes! Very cool! If you already have your file, it's still recommended to read over this first bit to make sure its formatted properly!

1. First, have your file ready and this repository! If you haven't created one yet, head over to `subsystems/node/` and create your file there. Following the naming is recommended, but not necessary. Additionally, it's recommended to put the file in this directory for easy and straightforward access.
2. Next, make sure you `from subsystems.node.node_functional.py import*` and `from subsystems.node.node_primatives.py import*` to import all the basic parts of a node. Import other node files as needed, except for `node.py`, as it is used as a quick way to import all nodes, and would result in a future circular import.
3. Ok, first node time! Your file should have imports with the basic nodes! Now, that a look at one of them and their structure. Starts off with `class Example(Node)`, has `@Input`, `@Display` and `@Output` decorators, and has a quite consitent recognizable structure across nodes. (see an example such as the `Random` node!)
``` python
@Input("Lower Limit", [Number], False) # An input.
@Input("Upper Limit", [Number], False) # Another input. Notice the "name, [allowed types], required" structure!
@Input("Only Integers", [Boolean], False) # Yet another one!
@Display("Range", False, lambda self: f"[{self.__lowerLimit.value}, {self.__upperLimit.value}]") # A display.
@Display("Only Integers", False, lambda self: self.__onlyIntegers.value) # Another display! Notice the "name, modifyable, getter" structure!
@Display("Random Number", False, lambda self: self.output.value) # Yet another one!
@Output("Random Number", Number, lambda self: self.output) # An output! Notice the "name, type, getter" structure!
class Random(Node): # Notice how it inherits Node!
    '''
        A random number, with range [a,b], includes both end points.

        Requires:
        - `lowerLimit` defines the minimum possible output.
        - `upperLimit` defines the maximum possible output.
        - `onlyIntegers` defines whether or not only integers are returned. 
    ''' # A bit of documentation, pretty useful when working on the code!
    def __init__(self, lowerLimit:Number = Number(0), upperLimit:Number = Number(1), onlyIntegers:Boolean = Boolean(False)): # The initalizer on the node object!
        super().__init__()
        self.__output = Number(0)
        self.set(lowerLimit, upperLimit, onlyIntegers)
    def set(self, lowerLimit:Number = Number(0), upperLimit:Number = Number(1), onlyIntegers:Boolean = Boolean(False)):
        # The set part! Notice the lack of calculations, only storing the Node objects.
        self.__lowerLimit = lowerLimit
        self.__upperLimit = upperLimit
        self.__onlyIntegers = onlyIntegers
        self.update()
    def update(self):
        # The update part, where the calculations do occur!
        try:
            if self.__lowerLimit.value == self.__upperLimit.value:
                self.__output.set(self.__lowerLimit.value)
            elif self.__onlyIntegers.value:
                self.__output.set(random.randint(self.__lowerLimit.value, self.__upperLimit.value))
            else:
                self.__output.set(random.random()*(self.__upperLimit.value-self.__lowerLimit.value)+self.__lowerLimit.value)
        except:
            self.addError("Random number failed to generate!") # Here's what it looks like to add an error!
        # Notice how update() doesn't return anything, just updates the ouput!
    
    @property # This makes the following definition a property of the node!
    def output(self) -> Number:
        return self.__output # Here is when the output is actually taken, by any other things needing it!
```
4. Now, that said, we're almost there! You've got your file, node, and are ready to add it! Now, head over to `subsystems/node/node.py`, and import your file there. Finally, add your node to the `NODES` list, and maybe add a little comment stating the group its in! (This comment doesn't affect the end program, it's just for organization!)
5. Finally, run `main.py`, and it should show up in the Nodes Tab! If any issues or help is needed, head over to [the Tape repository](https://github.com/HenryLi-0/tape/issues) and create an issue!

TO-DO: UPDATE!

## Controls:
*This section describes general controls!*

### General:

- Mouse Scroll: Zoom or move up/down

### Default Keybinds

**All:**
- Left Mouse Click: Interact
- Control_L or Return/Enter: Submit/Finish




## Warnings:
- Tape v2.x is a full rewrite from Tape v1.x, meaning that any projects created in Tape v1.x will almost certaintly NOT work in Tape v2.x! If you want to access Tape v1.x projects, use a version of Tape v1.x to open it.
- Opening projects from past versions may crash! The opening/saving code will try to stay the same throughout versions, but there is no guarantee that the project will always open properly through different versions.
- It's highly recommended to save your project before exporting as exporting can lag the window! (It may appear stuck, but let it run, assuming it didn't crash due to a bug!)
- Report any strange bugs/unexpected behavior in issues on GitHub! The repository can be found here: https://github.com/HenryLi-0/tape

---

### Version Info:

Tape Version: pre-v2.0.0

Last Updated: 12/24/2024
