'''This file contains functions for generating paths and other movements.'''

from settings import PATH_FLOAT_ACCURACY
import math

#SMOOTH PATHING TIME YIPPEE (very satsifying)

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

def betweenP(coord1: tuple|list,coord2: tuple|list):
    '''Returns a lambda that takes in the percent of the translation between two coordiantes out of one heading to point two, and returns that point'''
    return lambda t: (coord1[0]+t*(coord2[0]-coord1[0]),coord1[1]+t*(coord2[1]-coord1[1]))

def averagep(coord1: tuple|list,coord2: tuple|list):
    '''Returns the average of two points (x,y)'''
    return (((coord1[0]+coord2[0])/2),((coord1[1]+coord2[1])/2))

def roundf(float: float, digits: int):
    '''Returns the rounded value of the input float with digits digits after the decimal point'''
    return round(float*(10**digits))/(10**digits)

def roundp(point: tuple|list):
    '''Returns the rounded (x,y) point with PATH_FLOAT_ACCURACY digits after the decimal point'''
    return (roundf(point[0],PATH_FLOAT_ACCURACY), roundf(point[1],PATH_FLOAT_ACCURACY))

def pointAt(coord1: tuple|list, coord2: tuple|list):
    '''Returns the degrees of point 1 looking at point 2, using the "0 up CCW" rotation'''
    dx=coord2[0]-coord1[0]
    dx=0.0000001 if dx == 0 else dx
    dy=coord2[1]-coord1[1]
    return roundf(-(math.atan(dy/dx)/math.pi)*180-90 if dx>0 else -(math.atan(dy/dx)/math.pi)*180+90, PATH_FLOAT_ACCURACY)

# Bezier Maths

def oneAxisCurve(c1: int|float,c2: int|float,c3: int|float):
    '''Returns a lambda that takes in a t for one axis of a curve'''
    return lambda t: ((1-t)**2)*c1 + 2*(1-t)*t*c2 + (t**2)*c3

def bezierCurve(coord1: tuple|list,coord2: tuple|list, coord3: tuple|list):
    '''Returns a lambda that returns a point on a curve given t, the progression through the curve out of 1'''
    return lambda t: roundp((oneAxisCurve(coord1[0],coord2[0],coord3[0])(t),oneAxisCurve(coord1[1],coord2[1],coord3[1])(t)))

# Paths

def bezierPathCoords(coords: tuple[list|tuple]|list[list|tuple], steps: int):
    '''Generates a bezier path of coordinates based on a given list of coords, with steps number of points between each given coordinate'''
    if len(coords) == 0: return []
    if len(coords) >= 3:
        coordsc = coords.copy()
        stepsI = range(0, steps)
        coordsI = range(1,len(coordsc)-1)
        totalPath = []
        coordsc.insert(1,averagep(coordsc[0],coordsc[1]))
        bezier = bezierCurve(coordsc[0],coordsc[1],coordsc[2])
        for t in stepsI: totalPath.append(roundp(bezier(t/steps)))
        for i in coordsI:
            coordsc.insert(i*2+1, subtractP(multiplyP(coordsc[i*2],2),coordsc[i*2-1]))
            bezier = bezierCurve(coordsc[i*2],coordsc[i*2+1],coordsc[i*2+2])
            for t in stepsI: totalPath.append(roundp(bezier(t/steps)))
        totalPath.append(coordsc[-1])
        return totalPath
    else: return straightPathCoords(coords,steps)

def timelyBezierPathCoords(coords: tuple[list|tuple]|list[list|tuple], steps: tuple|list):
    '''Generates a bezier path of coordinates based on a given list of coords and time, with a changing number of steps number of points between each given coordinate based on the given steps list'''
    if len(coords) == 0: return []
    if len(coords) >= 3:
        coordsc = coords.copy()
        coordsI = range(1,len(coordsc)-1)
        totalPath = []
        coordsc.insert(1,averagep(coordsc[0],coordsc[1]))
        bezier = bezierCurve(coordsc[0],coordsc[1],coordsc[2])
        for t in range(0, steps[0]): totalPath.append(roundp(bezier(t/steps[0])))
        for i in coordsI:
            coordsc.insert(i*2+1, subtractP(multiplyP(coordsc[i*2],2),coordsc[i*2-1]))
            bezier = bezierCurve(coordsc[i*2],coordsc[i*2+1],coordsc[i*2+2])
            for t in range(0, steps[i]): totalPath.append(roundp(bezier(t/steps[i])))
        totalPath.append(coordsc[-1])
        return totalPath
    else: return straightPathCoords(coords,steps)

def selectiveBezierPathCoords(coords: tuple[list|tuple]|list[list|tuple], steps: int, lower: tuple|list):
    '''Generates a bezier path of coordinates between a given low point and the next point, based on a given list of coords and the index of the lower point, with steps number of points between the given coordinates'''
    if len(coords) == 0: return []
    if len(coords) >= 3:
        coordsc = coords.copy()
        stepsI = range(0, steps)
        coordsI = range(1,len(coordsc)-1)
        totalPath = []
        coordsc.insert(1,averagep(coordsc[0],coordsc[1]))
        bezier = bezierCurve(coordsc[0],coordsc[1],coordsc[2])
        if lower == 0:
            for t in stepsI: totalPath.append(roundp(bezier(t/steps)))
        for i in coordsI:
            coordsc.insert(i*2+1, subtractP(multiplyP(coordsc[i*2],2),coordsc[i*2-1]))
            if lower == i:
                bezier = bezierCurve(coordsc[i*2],coordsc[i*2+1],coordsc[i*2+2])
                for t in stepsI: totalPath.append(roundp(bezier(t/steps)))
        totalPath.append(coordsc[-1])
        return totalPath
    else: return straightPathCoords(coords,steps)

def straightPathCoords(coords: tuple[list|tuple]|list[list|tuple], steps: int):
    '''Generates a straight path of coordinates based on a given list of coords, with steps number of points between each given coordinate'''
    if len(coords) == 0: return []
    stepsI = range(0, steps)
    totalPath = []
    for i in range(len(coords)-1):
        translation = betweenP(coords[i], coords[i+1])
        for t in stepsI: totalPath.append(roundp(translation(t/steps)))
    totalPath.append(coords[-1])
    return totalPath

# Rotation

def pointNextCoordRotationPath(coords: tuple[list|tuple]|list[list|tuple]):
    '''Generates a rotation path, given a list of coords, where it points at the next coordinate'''
    if len(coords) == 0: return []
    rotationPath = []
    for i in range(len(coords)-2): rotationPath.append(pointAt(coords[i], coords[i+1]))
    rotationPath.append(rotationPath[-1])
    return rotationPath

def mergeCoordRotationPath(coords: tuple|list, rots: tuple|list):
    '''Merges a coordinate and rotation path and returns a merged path list of (x,y,dir)'''
    if len(coords) == 0: return []
    mergedPath = []
    for i in range(max(len(coords), len(rots))): mergedPath.append((coords[min(i,len(coords)-1)][0], coords[min(i,len(coords)-1)][1], rots[min(i,len(rots)-1)]))
    return mergedPath

# Changes Sequences

def smoothChangeAt(a, b, steps):
    path = []
    for step in range(steps): path.append(a+(b-a)*math.log(step+1, steps+1))
    return path

def straightChangeAt(a, b, steps):
    return [a + (b-a)*(i/steps) for i in range(steps)]