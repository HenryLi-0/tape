'''strange tests'''

from subsystems.pathing import bezierPathCoords, straightPathCoords
import time
import random
from subsystems.render import *
from settings import *
from subsystems.fonts import display

tests = 0
total = 0

while tests<1000:
    text = "".join([x for x in [("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-_=+")[random.randrange(0,75)] for x in range(100)]])
    start = time.time()
    img = display(text, "s")
    end = time.time()
    total+=end-start
    tests+=1
    print(f"{tests} tests | avg: {total/tests} seconds")



# coords = [(0,0),(8,4),(-4,6),(-8,0),(-8,-6)]
# coords = bezierPathCoords(coords,30)
# print(coords)


# merge(PLACEHOLDER_IMAGE, PLACEHOLDER_IMAGE)