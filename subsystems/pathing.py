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

# Bezier

