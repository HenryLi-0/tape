from subsystems.pathing import bezierPathCoords
import time
import random

gen = lambda: 180-random.random()*360
steps = 60

tests = 0
total = 0

while tests<1000:
    coords = [
        (gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),
        (gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),
        (gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),
        (gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),
        (gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),
        (gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),
        (gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),
        (gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),
        (gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),
        (gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen()),(gen(),gen())
        ]
    start = time.time()
    bezierPathCoords(coords,steps)
    end = time.time()
    total+=end-start
    tests+=1
    print(f"{tests} tests | avg: {total/tests} seconds")



# coords = [(0,0),(0,10),(10,10),(20,0),(10,-10),(30,-20),(0,-20),(-20,0),(-20,10),(0,-10)]
# coords = bezierPathCoords(coords,30)
# print(coords)