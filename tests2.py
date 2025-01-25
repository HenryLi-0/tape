from subsystems.node.node_primatives import *

# node1 = Number(0)
# node2 = Number(10)
# node3 = Boolean(True)
# node4 = Random(node1, node2, node3)
# while True:
#     print(node4.get().get())

# node1 = FileLocation(String("C:/Users/henry/Desktop/Projects/Github Repositories/tape/nonexistence.png"))
# print(node1.getError().getError())

# print(Milliseconds(Days(Seconds(Milliseconds(Days(Milliseconds(Number(10))))))).get().get())
# print(Degrees(Radians(Radians(Degrees(Degrees(Radians(Degrees(Number(10)))))))).get().get())

# import time
# avg = 0
# i = 0
# n = 1000000
# while i < n:
#     start = time.time()
#     exec(f"node{i} = Number(i)")
#     end = time.time()
#     avg += (end-start)
#     i+=1
# avg /= n
# print(avg)

# node = Number(1)
# print(node.get())
# print(node)
# node.set(2)
# print(node.get())
# print(node)

# from subsystems.fancy import *
# from settings import *
# generateHoverIcon(CURSOR_ARROW, False).show()

# print(Random.Output)

# import subsystems.node.node 
# print([x for x in dir(subsystems.node.node.NodeThemes) if x[0:2] != "__"])
# print(subsystems.node.node.THEMES)

from subsystems.simplefancy import *
from settings import NODE_IO_TRIANGLE
fill(NODE_IO_TRIANGLE.copy(), [255,255,255,255], [100,0,0,255]).show()