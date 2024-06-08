from subsystems.pathing import path3coords
import time
import random

gen = lambda: 2500-random.random()*5000
steps = 60

tests = 0
total = 0

while tests<1000:
    coords = [(gen(),gen()),(gen(),gen()),(gen(),gen())]
    start = time.time()
    path3coords(coords,steps)
    end = time.time()
    total+=end-start
    tests+=1

    print(f"{tests} tests | avg: {total/tests} seconds")

