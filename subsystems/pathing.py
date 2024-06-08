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

def beizerL(coord1: tuple|list, coord2: list|tuple, coord3: tuple|list):
    '''
        Returns a lambda f(x,u)=mx+b (u part of beizer), given two points in (x,y) format
        Point 1 is the stop to the left of the target (first end, start)
        Point 2 is a step between 1 and 3
        Point 3 is the stop to the right of the target (second end, end)
    '''
    return lambda x, percent: ((4*coord2[1]-3*coord1[1]-coord3[1]+4*percent*(coord3[1]+coord1[1]-2*coord2[1]))/(4*coord2[0]-3*coord1[0]-coord3[0]+4*percent*(coord3[0]+coord1[0]-2*coord2[0])))*(x-coord1[0]+2*percent*(0-coord2[0]+((3*coord1[0])/4)+((coord3[0])/4)))+coord1[1]-2*percent*(0-coord2[1]+((3*coord1[1])/4)+(coord3[1]/4))
def beizerMB(coord1: tuple|list, coord2: list|tuple, coord3: tuple|list):
    '''
        Returns a lambda (m,b), where f(x,u)=mx+b (u part of beizer), given two points in (x,y) format
        Point 1 is the stop to the left of the target (first end, start)
        Point 2 is a step between 1 and 3
        Point 3 is the stop to the right of the target (second end, end)
    '''
    return lambda percent: ((((4*coord2[1]-3*coord1[1]-coord3[1]+4*percent*(coord3[1]+coord1[1]-2*coord2[1]))/(4*coord2[0]-3*coord1[0]-coord3[0]+4*percent*(coord3[0]+coord1[0]-2*coord2[0])))*(0-coord1[0]+2*percent*(0-coord2[0]+((3*coord1[0])/4)+((coord3[0])/4)))),(coord1[1]-2*percent*(0-coord2[1]+((3*coord1[1])/4)+(coord3[1]/4))))

def intersect(line1: tuple|list, line2: tuple|list):
    '''Returns the (x,y) intersection of two lines, given as (m,b) where y=mx+b'''
    return (((line2[1]-line1[1])/(line1[0]-line2[0])),(((line2[1]-line1[1])/(line1[0]-line2[0]))*line1[0]+line1[1]))


def path3coords(coords: tuple[list|tuple]|list[list|tuple], stops: int):
    '''Returns a list of (x,y) points, given a set of 3 coords [(x,y),(x,y),(x,y)] and stops'''
    coord1=coords[0]
    coord2=coords[1]
    coord3=coords[2]
    beizer = beizerMB(coord1,coord2,coord3)
    result = []
    for i in range(1,stops):
        result.append(intersect(beizer(i/stops),beizer((i+1)/stops)))
    return result