from subsystems.node.node_primatives import *
from subsystems.node.node_pathing import *
from subsystems.settings import *

'''OPERATIONS'''

class Addition(Node):
    '''
        A node that adds two nodes together, if logical. The node interprets addition as adding the second input to the first input.
        Requires:
        - `inputA` represents the first input, which addition is operated on.
        - `inputB` represents the second input, which is added to `inputA`.
    '''
    def __init__(self, inputA, inputB):
        super().__init__()
        if type(inputA) == Number and type(inputB) == Number:
            self.value = Number(inputA.get()+inputB.get())
        elif issubclass(type(inputA), Unit) and type(inputA) == type(inputB):
            self.value = inputA.__class__(inputA.get()+inputB.get())
        elif type(inputA) == Coordinate and type(inputB) == Coordinate:
            self.value = Coordinate(Number(inputA.x+inputB.x), Number(inputA.y+inputB.y))
        elif type(inputA) == Frame and type(inputB) == Time:
            self.value = Frame(inputA.value, Addition(inputA.time, inputB))
        elif type(inputA) == Frame and inputA.type == type(inputB):
            self.value = Frame(Addition(inputA.value, inputB), inputA.time)
        elif type(inputA) == Path and type(inputB) == Path:
            pass # TO-DO: FINISH PATH LOGIC
        else:
            self.addError(f"Addition between {type(inputA)} and {type(inputB)} not supported!")
    def get(self):
        return self.value

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


