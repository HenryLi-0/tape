from subsystems.node.node_primatives import *
from subsystems.settings import *

'''Location'''

class Coordinate(Node):
    '''
        A coordinate representing a location on a 2D plane

        Requires:
        - `x` represents the x coordinate.
        - `y` represents the y coordinate.
    '''
    def __init__(self, x:Number|Pixel = Number(0), y:Number|Pixel = Number(0)):
        super().__init__()
        if type(x) == Number: xcoord = x
        elif type(x) == Pixel: xcoord = x
        self.coordinate = [x,y]
    def get(self):
        return self
    
    # TO-DO: FINISH

