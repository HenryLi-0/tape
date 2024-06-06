#SMOOTH PATHING TIME YIPPEE


def point(x,y):
    '''Returns a tuple (x,y) given the coordinate's x and y'''
    return (x,y)

def line(coord1: tuple|list,coord2: tuple|list):
    '''Returns a lambda f(x)=mx+b, given two points in (x,y) format '''
    return lambda x: ((coord2[1]-coord1[1])/(coord2[0]-coord1[0]))*(x-coord1[0])+coord1[1]

def midpoint(coord1: tuple|list,coord2: tuple|list):
    '''Returns a midpoint, given two points in (x,y) format'''
    return ((coord1[0]+coord2[0])/2,(coord1[1]+coord2[1])/2)

def pointA(coord1: tuple|list,coord2: tuple|list,coord3: tuple|list):
    '''
        Returns "Point A", given two points in (x,y) format.
        Point 1 is the first end (start)
        Point 2 is a step between point 1 and 3
        Point 3 is the second end (end)
    '''
    return (2*coord2[0]-((coord1[0]+coord3[0])/2),2*coord2[1]-((coord1[1]+coord3[1])/2))

def beizerL(coord1: tuple|list, coord2: list|tuple, coord3: tuple|list, percent):
    '''
        Returns a lambda f(x)=mx+b, given two points in (x,y) format
        Point 1 is the stop to the left of the target (first end, start)
        Point 2 is a step between 1 and 3
        Point 3 is the stop to the right of the target (second end, end)
    '''
    return lambda x: ((4*coord2[1]-3*coord1[1]-coord3[1]+4*percent*(coord3[1]+coord1[1]-2*coord2[1]))/(4*coord2[0]-3*coord1[0]-coord3[0]+4*percent*(coord3[0]+coord1[0]-2*coord2[0])))*(x-coord1[0]+2*percent*(0-coord2[0]+((3*coord1[0])/4)+((coord3[0])/4)))+coord1[1]-2*percent*(0-coord2[1]+((3*coord1[1])/4)+(coord3[1]/4))
def beizerMB(coord1: tuple|list, coord2: list|tuple, coord3: tuple|list, percent):
    '''
        Returns a m and b, where f(x)=mx+b, given two points in (x,y) format
        Point 1 is the stop to the left of the target (first end, start)
        Point 2 is a step between 1 and 3
        Point 3 is the stop to the right of the target (second end, end)
    '''
    return ((((4*coord2[1]-3*coord1[1]-coord3[1]+4*percent*(coord3[1]+coord1[1]-2*coord2[1]))/(4*coord2[0]-3*coord1[0]-coord3[0]+4*percent*(coord3[0]+coord1[0]-2*coord2[0])))*(0-coord1[0]+2*percent*(0-coord2[0]+((3*coord1[0])/4)+((coord3[0])/4)))),(coord1[1]-2*percent*(0-coord2[1]+((3*coord1[1])/4)+(coord3[1]/4))))

def intersect(line1: tuple|list, line2: tuple|list):
    '''Returns the (x,y) intersection of two lines, given as (m,b) where y=mx+b'''
    return (((line2[1]-line1[1])/(line1[0]-line2[0])),(((line2[1]-line1[1])/(line1[0]-line2[0]))*line1[0]+line1[1]))
