import time

'''Parts of the Node system that aren't exactly nodes, but still very important for Nodes to work in Tape.'''

class ActiveError:
    def __init__(self, error = None):
        self.errors = []
        self.addError(error)
    def addError(self, error):
        self.errors.append(f"{time.time()} - {error}")
    def getError(self):
        return self.errors
        
def Input(name = None, type = None, required = None, multiple = False):
    def decorator(inClass):
        if not hasattr(inClass, "Input"):
            inClass.Input = []
        if name != None:
            inClass.Input.insert(0, (name, type, required, multiple))
        return inClass
    return decorator

def Display(name = None, modify = None, getter = None):
    def decorator(inClass):
        if not hasattr(inClass, "Display"):
            inClass.Display = []
        if name != None:
            inClass.Display.insert(0, (name, modify, getter))
        return inClass
    return decorator

def Output(name = None, type = None, getter = None):
    def decorator(inClass):
        if not hasattr(inClass, "Output"):
            inClass.Output = []
        if name != None:
            inClass.Output.insert(0, (name, inClass if type==-1 else type, getter))
        return inClass
    return decorator

def validate(*inputs):
    valid = True
    for input in inputs:
        if input == None:
            valid = False
            break
    return valid