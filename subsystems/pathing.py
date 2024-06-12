'''This file contains functions for generating paths and other movements.'''

from settings import PATH_FLOAT_ACCURACY

#SMOOTH PATHING TIME YIPPEE

# Basic

def point(x,y):
    '''Returns a tuple (x,y) given the coordinate's x and y'''
    return (x,y)

def addP(coord1: tuple|list, coord2: tuple|list):
    '''Adds the x and y coordinates of 2 points given in (x,y) format'''
    return (coord1[0]+coord2[0],coord1[1]+coord2[1])

def subtractP(coord1: tuple|list, coord2: tuple|list):
    '''Subtracts (x1,y1) by (x2,y2) given in (x,y) format'''
    return (coord1[0]-coord2[0],coord1[1]-coord2[1])

def multiplyP(coord: tuple|list, mul):
    '''Multiplies the x and y coordinate of a given (x,y) by mul'''
    return (coord[0]*mul, coord[1]*mul)

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

# Bezier

def oneAxisCurve(c1: int|float,c2: int|float,c3: int|float):
    '''Returns a lambda that takes in a t for one axis of a curve'''
    return lambda t: ((1-t)**2)*c1 + 2*(1-t)*t*c2 + (t**2)*c3

def bezierCurve(coord1: tuple|list,coord2: tuple|list, coord3: tuple|list):
    '''Returns a lambda that returns a point on a curve given t, the progression through the curve out of 1'''
    return lambda t: roundp((oneAxisCurve(coord1[0],coord2[0],coord3[0])(t),oneAxisCurve(coord1[1],coord2[1],coord3[1])(t)))

def bezierPathCoords(coords: tuple[list|tuple]|list[list|tuple], steps: int):
    if len(coords) >= 3:
        iterate = range(0, steps)
        totalPath = []
        coords.insert(1,coords[0])
        bezier = bezierCurve(coords[0],coords[1],coords[2])
        for t in iterate:
            totalPath.append(roundp(bezier(t/steps)))
        for i in range(1,len(coords)-1):
            bezier = bezierCurve(coords[i],multiplyP(subtractP(coords[i],coords[i-1]),2),coords[i+1])
            for t in iterate:
                totalPath.append(roundp(bezier(t/steps)))
        return totalPath
    else:
        raise IndexError(f"Input coords are too short, input was {len(coords)} long, should be at least 3")