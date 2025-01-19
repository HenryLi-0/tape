from subsystems.node.node_primatives import *
from subsystems.node.node_pathing import *
from subsystems.settings import *

'''OPERATIONS''' # TO-DO: REFACTOR EVERYTHING BELOW HERE!!! ALSO MAKE IT MAKE SENSE!

@Input("Node A", [Node], True)
@Input("Node B", [Node], True)
@Input("Sum", [Node], True)
class Addition(Node): # TO-DO: OPTIMIZE THIS MORE, FINISH UPDATING
    '''
        A node that adds two nodes together, if logical. The node interprets addition as adding the second input to the first input.
        
        Requires:
        - `inputA` represents the first input, which addition is operated on.
        - `inputB` represents the second input, which is added to `inputA`.
    '''
    def __init__(self, inputA:Node, inputB:Node):
        super().__init__()
        self.__output = None
        self.set(inputA, inputB)
    def set(self, inputA:Node, inputB:Node):
        self.inputA = inputA
        self.inputB = inputB
        if type(inputA) == Number and type(inputB) == Number:
            self.__output = Number(inputA.value+inputB.value)
        elif issubclass(type(inputA), Unit) and type(inputA) == type(inputB): # TO-DO: ADD UNIT CONVERSION
            self.__output = inputA.__class__(inputA.value+inputB.value)
        elif type(inputA) == Coordinate and type(inputB) == Coordinate:
            self.__output = Coordinate(Number(inputA.__x+inputB.__x), Number(inputA.__y+inputB.__y))
        elif type(inputA) == Frame and type(inputB) == Time:
            self.__output = Frame(inputA.__value, Addition(inputA.__time, inputB))
        elif type(inputA) == Frame and inputA.type == type(inputB):
            self.__output = Frame(Addition(inputA.__value, inputB), inputA.__time)
        elif type(inputA) == Path and type(inputB) == Path:
            pass # TO-DO: FINISH PATH LOGIC
        else:
            self.addError(f"Addition between {type(inputA)} and {type(inputB)} not supported!")
    def update(self):
        if type(self.inputA) == Number and type(self.inputB) == Number:
            self.__output.set(self.inputA.update()+self.inputB.update())
        elif issubclass(type(self.inputA), Unit) and type(self.inputA) == type(self.inputB): # TO-DO: ADD UNIT CONVERSION
            self.__output.set(self.inputA.update()+self.inputB.update())
        elif type(self.inputA) == Coordinate and type(self.inputB) == Coordinate:
            self.__output.set(Number(self.inputA.__x+self.inputB.__x), Number(self.inputA.__y+self.inputB.__y))
        elif type(self.inputA) == Frame and type(self.inputB) == Time:
            self.__output.set(self.inputA.__value, Addition(self.inputA.__time, self.inputB))
        elif type(self.inputA) == Frame and self.inputA.type == type(self.inputB):
            self.__output.set(Addition(self.inputA.__value, self.inputB), self.inputA.__time)
        elif type(self.inputA) == Path and type(self.inputB) == Path:
            pass # TO-DO: FINISH PATH LOGIC
        else:
            self.addError(f"Addition between {type(self.inputA)} and {type(self.inputB)} not supported!")
        return self.__output

@Input("Node A", [Node], True)
@Input("Node B", [Node], True)
@Input("Product", [Node], True)
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
            self.value = Number(inputA.update()*inputB.update())
        elif issubclass(type(inputA), Unit) and type(inputB) == Number:
            self.value = inputA.__class__(inputA.update()*inputB.update())
        elif type(inputA) == Coordinate and type(inputB) == Number:
            self.value = Coordinate(Number(inputA.__x*inputB.update()), Number(inputA.__y*inputB.update()))
        else:
            self.addError(f"Multiplication between {type(inputA)} and {type(inputB)} not supported!")
        # TO-DO: ADD MORE VALID MULTIPLICATION CASES
    def update(self):
        return self.value


