from subsystems.node.node_primatives import *
from subsystems.node.node_pathing import *
from subsystems.settings import *

'''OPERATIONS''' # TO-DO: REFACTOR EVERYTHING BELOW HERE!!!

class Addition(Node): # TO-DO: OPTIMIZE THIS MORE
    '''
        A node that adds two nodes together, if logical. The node interprets addition as adding the second input to the first input.
        
        Requires:
        - `inputA` represents the first input, which addition is operated on.
        - `inputB` represents the second input, which is added to `inputA`.
    '''
    def __init__(self, inputA:Node, inputB:Node):
        super().__init__()
        self.output = None
        self.set(inputA, inputB)
    def set(self, inputA:Node, inputB:Node):
        self.inputA = inputA
        self.inputB = inputB
        if type(inputA) == Number and type(inputB) == Number:
            self.output = Number(inputA.get()+inputB.get())
        elif issubclass(type(inputA), Unit) and type(inputA) == type(inputB): # TO-DO: ADD UNIT CONVERSION
            self.output = inputA.__class__(inputA.get()+inputB.get())
        elif type(inputA) == Coordinate and type(inputB) == Coordinate:
            self.output = Coordinate(Number(inputA.x+inputB.x), Number(inputA.y+inputB.y))
        elif type(inputA) == Frame and type(inputB) == Time:
            self.output = Frame(inputA.value, Addition(inputA.time, inputB))
        elif type(inputA) == Frame and inputA.type == type(inputB):
            self.output = Frame(Addition(inputA.value, inputB), inputA.time)
        elif type(inputA) == Path and type(inputB) == Path:
            pass # TO-DO: FINISH PATH LOGIC
        else:
            self.addError(f"Addition between {type(inputA)} and {type(inputB)} not supported!")
    def get(self):
        if type(self.inputA) == Number and type(self.inputB) == Number:
            self.output.set(self.inputA.get()+self.inputB.get())
        elif issubclass(type(self.inputA), Unit) and type(self.inputA) == type(self.inputB): # TO-DO: ADD UNIT CONVERSION
            self.output.set(self.inputA.get()+self.inputB.get())
        elif type(self.inputA) == Coordinate and type(self.inputB) == Coordinate:
            self.output.set(Number(self.inputA.x+self.inputB.x), Number(self.inputA.y+self.inputB.y))
        elif type(self.inputA) == Frame and type(self.inputB) == Time:
            self.output.set(self.inputA.value, Addition(self.inputA.time, self.inputB))
        elif type(self.inputA) == Frame and self.inputA.type == type(self.inputB):
            self.output.set(Addition(self.inputA.value, self.inputB), self.inputA.time)
        elif type(self.inputA) == Path and type(self.inputB) == Path:
            pass # TO-DO: FINISH PATH LOGIC
        else:
            self.addError(f"Addition between {type(self.inputA)} and {type(self.inputB)} not supported!")
        return self.output

class Multiplication(Node):
    '''
        A node that multiplies two nodes together, if logical. The node interprets multiplication as multiplying the first input by the second input.
        
        Requires:
        - `inputA` represents the first input, which multiplication is operated on.
        - `inputB` represents the second input, which `inputA` is multiplied by.
    '''
    def __init__(self, inputA, inputB):
        super().__init__()
        if type(inputA) == Number and type(inputB) == Number:
            self.value = Number(inputA.get()*inputB.get())
        elif issubclass(type(inputA), Unit) and type(inputB) == Number:
            self.value = inputA.__class__(inputA.get()*inputB.get())
        elif type(inputA) == Coordinate and type(inputB) == Number:
            self.value = Coordinate(Number(inputA.x*inputB.get()), Number(inputA.y*inputB.get()))
        else:
            self.addError(f"Multiplication between {type(inputA)} and {type(inputB)} not supported!")
        # TO-DO: ADD MORE VALID MULTIPLICATION CASES
    def get(self):
        return self.value


