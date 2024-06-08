from subsystems.pathing import beizerPath3coords, beizerPathCoords
import time
import random

gen = lambda: 180-random.random()*360
steps = 60

# tests = 0
# total = 0

# while tests<1000:
#     coords = [(gen(),gen()),(gen(),gen()),(gen(),gen())]
#     start = time.time()
#     beizerPath3coords(coords,steps)
#     end = time.time()
#     total+=end-start
#     tests+=1

#     print(f"{tests} tests | avg: {total/tests} seconds")

thing = beizerPathCoords([(0,0),(100.01,100.01),(-100.02,100.02),(-100.03,-100.03),(100.04,-100.04),(0.05,0.05)],30)

for item in thing:
    print(item[0])
    print(item[1])