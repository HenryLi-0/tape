'''This file contains functions for basic point calculations.'''

from settings import FLOAT_ACCURACY
import math

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
    return (roundf(point[0],FLOAT_ACCURACY), roundf(point[1],FLOAT_ACCURACY))

def pointAt(coord1: tuple|list, coord2: tuple|list):
    '''Returns the degrees of point 1 looking at point 2, using the "0 up CCW" rotation'''
    dx=coord2[0]-coord1[0]
    dx=0.0000001 if dx == 0 else dx
    dy=coord2[1]-coord1[1]
    return roundf(-(math.atan(dy/dx)/math.pi)*180-90 if dx>0 else -(math.atan(dy/dx)/math.pi)*180+90, FLOAT_ACCURACY)
