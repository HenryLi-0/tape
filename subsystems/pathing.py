'''This file contains functions for generating paths.'''

from settings import FLOAT_ACCURACY
import math
from subsystems.point import *

#SMOOTH PATHING TIME YIPPEE (very satsifying)

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

def timelyBezierPathCoords(coords: tuple[list|tuple]|list[list|tuple], steps: tuple|list, partion = False):
    '''Generates a bezier path of coordinates based on a given list of coords and time, with a changing number of steps number of points between each given coordinate based on the given steps list'''
    if len(coords) == 0: return [[]] if partion else []
    if len(coords) >= 3:
        coordsc = coords.copy()
        coordsI = range(1,len(coordsc)-1)
        totalPath = []
        coordsc.insert(1,averagep(coordsc[0],coordsc[1]))
        bezier = bezierCurve(coordsc[0],coordsc[1],coordsc[2])
        if partion:
            tempPath = []
            for t in range(0, steps[0]): tempPath.append(roundp(bezier(t/steps[0])))
            totalPath.append(tempPath)
        else:
            for t in range(0, steps[0]): totalPath.append(roundp(bezier(t/steps[0])))
        for i in coordsI:
            coordsc.insert(i*2+1, subtractP(multiplyP(coordsc[i*2],2),coordsc[i*2-1]))
            bezier = bezierCurve(coordsc[i*2],coordsc[i*2+1],coordsc[i*2+2])
            if partion:
                tempPath = []
                for t in range(0, steps[i]): tempPath.append(roundp(bezier(t/steps[i])))
                totalPath.append(tempPath)
            else:
                for t in range(0, steps[i]): totalPath.append(roundp(bezier(t/steps[i])))
        if not(partion):
            totalPath.append(coordsc[-1])
        return totalPath
    else: 
        if partion: return [straightPathCoords(coords,steps[0])]
        else: return straightPathCoords(coords,steps[0])

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
    for step in range(round(steps)): path.append(a+(b-a)*math.log(step+1, steps+1))
    return path

def straightChangeAt(a, b, steps):
    return [a + (b-a)*(i/steps) for i in range(round(steps))]

# Math

def tcoordVelocity(tcoords: tuple|list):
    if len(tcoords) > 0:
        path = [(tcoords[0][0], 0)]
        for i in range(1, len(tcoords)):
            change = subtractP(tcoords[i][1],tcoords[i-1][1])
            path.append((tcoords[i][0],roundf(math.sqrt(change[0]**2 + change[1]**2), FLOAT_ACCURACY)))
        return path
    else: return [(0, 0)]