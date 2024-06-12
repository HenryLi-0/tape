from subsystems.pathing import bezierPathCoords
import time
import random

gen = lambda: 180-random.random()*360
steps = 60

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
#     bezierPathCoords(coords,steps)
#     end = time.time()
#     total+=end-start
#     tests+=1

#     print(f"{tests} tests | avg: {total/tests} seconds")



coords = [(0,0),(7,1),(-10,3),(-10,-9),(3,-12),(8,-15)]
coords = bezierPathCoords(coords,30)
print(coords)