'''This file contains functions for generating paths and other movements.'''

from settings import PATH_FLOAT_ACCURACY

#SMOOTH PATHING TIME YIPPEE

# Basic

def point(x,y):
    '''Returns a tuple (x,y) given the coordinate's x and y'''
    return (x,y)

def line(coord1: tuple|list,coord2: tuple|list):
    '''Returns a lambda f(x)=mx+b, given two points in (x,y) format '''
    return lambda x: ((coord2[1]-coord1[1])/(coord2[0]-coord1[0]))*(x-coord1[0])+coord1[1]

def midpoint(coord1: tuple|list,coord2: tuple|list):
    '''Returns a midpoint, given two points in (x,y) format'''
    return ((coord1[0]+coord2[0])/2,(coord1[1]+coord2[1])/2)

def intersect(line1: tuple|list, line2: tuple|list):
    '''Returns the (x,y) intersection of two lines, given as (m,b) where y=mx+b'''
    return (((line2[1]-line1[1])/(line1[0]-line2[0])),(((line2[1]-line1[1])/(line1[0]-line2[0]))*line1[0]+line1[1]))

def averagep(coord1: tuple|list,coord2: tuple|list):
    '''Returns the average of two points (x,y)'''
    return (((coord1[0]+coord2[0])/2),((coord1[1]+coord2[1])/2))

def roundf(float: float, digits: int):
    '''Returns the rounded value of the input float with digits digits after the decimal point'''
    return round(float*(10**digits))/(10**digits)

def roundp(point: tuple|list):
    '''Returns the rounded (x,y) point with PATH_FLOAT_ACCURACY digits after the decimal point'''
    return (roundf(point[0],PATH_FLOAT_ACCURACY), roundf(point[1],PATH_FLOAT_ACCURACY))

# bezier

def pointA(coord1: tuple|list,coord2: tuple|list,coord3: tuple|list):
    '''
        Returns "Point A", given two points in (x,y) format.
        Point 1 is the first end (start)
        Point 2 is a step between point 1 and 3
        Point 3 is the second end (end)
    '''
    return (2*coord2[0]-((coord1[0]+coord3[0])/2),2*coord2[1]-((coord1[1]+coord3[1])/2))

def bezierL(coord1: tuple|list, coord2: list|tuple, coord3: tuple|list):
    '''
        Returns a lambda f(x,u)=mx+b (u part of bezier) that takes in x and u, given two points in (x,y) format
        Point 1 is the stop to the left of the target (first end, start)
        Point 2 is a step between 1 and 3
        Point 3 is the stop to the right of the target (second end, end)
    '''
    return lambda x, percent: ((4*coord2[1]-3*coord1[1]-coord3[1]+4*percent*(coord3[1]+coord1[1]-2*coord2[1]))/(4*coord2[0]-3*coord1[0]-coord3[0]+4*percent*(coord3[0]+coord1[0]-2*coord2[0])))*(x-coord1[0]+2*percent*(0-coord2[0]+((3*coord1[0])/4)+((coord3[0])/4)))+coord1[1]-2*percent*(0-coord2[1]+((3*coord1[1])/4)+(coord3[1]/4))
def bezierMB(coord1: tuple|list, coord2: list|tuple, coord3: tuple|list):
    '''
        Returns a lambda (m,b), where f(x,u)=mx+b (u part of bezier) that takes in u, given two points in (x,y) format
        Point 1 is the stop to the left of the target (first end, start)
        Point 2 is a step between 1 and 3
        Point 3 is the stop to the right of the target (second end, end)
    '''
    return lambda percent: ((((4*coord2[1]-3*coord1[1]-coord3[1]+4*percent*(coord3[1]+coord1[1]-2*coord2[1]))/(4*coord2[0]-3*coord1[0]-coord3[0]+4*percent*(coord3[0]+coord1[0]-2*coord2[0])))),(((4*coord2[1]-3*coord1[1]-coord3[1]+4*percent*(coord3[1]+coord1[1]-2*coord2[1]))/(4*coord2[0]-3*coord1[0]-coord3[0]+4*percent*(coord3[0]+coord1[0]-2*coord2[0])))*(0-coord1[0]+2*percent*(0-coord2[0]+((3*coord1[0])/4)+((coord3[0])/4)))+coord1[1]-2*percent*(0-coord2[1]+((3*coord1[1])/4)+(coord3[1]/4))))


def bezierPath3coords(coords: tuple[list|tuple]|list[list|tuple], steps: int):
    '''Returns a list of (x,y) points, given a set of 3 coords [(x,y),(x,y),(x,y)] and steps'''
    bezier = bezierMB(coords[0],coords[1],coords[2])
    result = []
    for i in range(1,steps):
        result.append(roundp(intersect(bezier(i/steps),bezier((i+1)/steps))))
    return result

def bezierPathCoords(coords: tuple[list|tuple]|list[list|tuple], eachhalfsteps: int):
    if len(coords) >= 3:
        iterate = range(1, eachhalfsteps)
        totalPath = []
        for i in range(len(coords)-2):
            bezier = bezierMB(coords[i],coords[i+1],coords[i+2])
            totalPath.append([roundp(intersect(bezier(ie/(eachhalfsteps*2)),bezier((ie+1)/(eachhalfsteps*2)))) for ie in iterate])
            totalPath.append([roundp(intersect(bezier((ie+eachhalfsteps)/(eachhalfsteps*2)),bezier((ie+eachhalfsteps+1)/(eachhalfsteps*2)))) for ie in iterate])
        for i in range(1,len(coords)-2):        
            totalPath[i] = [averagep(totalPath[i][ie-1], totalPath[i+1][ie-1]) for ie in iterate]
            totalPath.pop(i+1)
        for i in range(0, len(coords)):
            totalPath.insert(i*2,[coords[i]])
        totalPath = [roundp(point) for section in totalPath for point in section]
        return totalPath
    else:
        raise IndexError(f"Input coords are too short, input was {len(coords)} long, should be at least 3")