from subsystems.node.node_primatives import *

# node1 = Number(0)
# node2 = Number(10)
# node3 = Boolean(True)
# node4 = Random(node1, node2, node3)
# node4.get()

# node1 = FileLocation(String("C:/Users/henrys/Desktop/Projects/Github Repositories/tape/nonexistence.png"))
# print(node1.getError())

# print(Milliseconds(Days(Seconds(Milliseconds(Days(Milliseconds(Number(10))))))).get().get())
# print(Degrees(Radians(Radians(Degrees(Degrees(Radians(Degrees(Number(10)))))))).get().get())

import time
avg = 0
i = 0
n = 1000000
while i < n:
    start = time.time()
    exec(f"node{i} = Number(i)")
    end = time.time()
    avg += (end-start)
    i+=1
avg /= n
print(avg)