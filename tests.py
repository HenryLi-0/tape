from subsystems.pathing import bezierPathCoords, straightPathCoords
import time
import random

# gen = lambda: 180-random.random()*360
# steps = 60

# tests = 0
# total = 0

# while tests<1000:
#     coords = [
#         (gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),
#         (gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),
#         (gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),
#         (gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),
#         (gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),
#         (gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),
#         (gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),
#         (gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),
#         (gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),
#         (gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen())
#         ]
#     start = time.time()
#     straightPathCoords(coords,steps)
#     end = time.time()
#     total+=end-start
#     tests+=1
#     print(f"{tests} tests | avg: {total/tests} seconds")



# coords = [(0,0),(8,4),(-4,6),(-8,0),(-8,-6)]
# coords = bezierPathCoords(coords,30)
# print(coords)


from subsystems.render import *
from settings import *
# merge(PLACEHOLDER_IMAGE, PLACEHOLDER_IMAGE)

import numpy
arrayToImage(placeOver(PLACEHOLDER_IMAGE,PLACEHOLDER_IMAGE2,(450,450))).show()