'''strange experiments'''

'''
project = [
    { #project
        "project name": "example",
        "UUID" : "some uuid",
        "other stats and stuff": "things"
    },
    { #timeline
        "length": 5,
        "some sprite uuid": {
            "name": "thing",
            "image" : "image uuid",
            "some action": "data",
            "some action": "data",
            "some action": "data"
        },
        "some sprite uuid": {
            "name": "thing",
            "image" : "image uuid",
            "some action": "data",
            "some action": "data",
            "some action": "data"
        }
    },
    {  #image data IF the user wants to export it together (otherwise, these images will not exist!)
        "some uuid": "some numpy array",
        "some uuid": "some numpy array",
        "some uuid": "some numpy array",
        "some uuid": "some numpy array",
        "some uuid": "some numpy array"
    }
]


cache = [ # cache of image uuids!
    "some uuid",
    "some uuid",
    "some uuid",
    "some uuid",
    "some uuid"
    ]
'''


'''
from subsystems.sprite import iterateThroughPath
states = [
    0, (0,0), "L",
    1, (3,3), "S",
    3, (5,8), "S",
    8, (10,5), "S",
    9, (11,11), None
]

# print(findStateThroughSingle(states, 0.9))

# print([(i/10, findStateThroughSingle(states, i/10)) for i in range(100)])
print(iterateThroughPath(states))
'''

'''
from subsystems.pathing import bezierPathCoords, selectiveBezierPathCoords
steps = 10
print(bezierPathCoords([(0,0),(5,5),(9,2),(5,6),(7,8)], steps))

from subsystems.sprite import findStateThroughPath

states = [
    0, (0,0), "S",
    1, (5,5), "S",
    2, (9,2), "L",
    3, (5,6), "L",
    8, (7,8), None
]

thing = []
for i in range(81):
    thing.append(findStateThroughPath(states, i/10))
print(thing)
'''

'''
from subsystems.sprite import SingleSprite
thing = SingleSprite("Test Sprite")

thing.setData("c", [0,(0,0),"L",5,(200,200),"S",7.5,(300,100),"S",10,(200,0), "L", 15, (0,200), None])
thing.setData("r", [0, 0, "S", 2.5, 90, "S", 5, 180, "S", 7.5, 270, "S", 10, 360, "L", 15, 0, None])
thing.setData("a", [0, 0, "L", 15, 0, None])
thing.setData("s", [0, 100, "S", 7.5, 200, "S", 15, 100, None])
thing.setData("h", [0, 0, "S", 15, 100, None])
thing.setData("t", [0, 100, "L", 15, 100, None])
thing.setData("b", [0, 0, "S", 2.5, 100, "S", 7.5, 100, "S", 10, 0, None])
thing.setData("w", [0, 0, "L", 5, 100, "L", 6, 0, None])

print(thing.generateFullSequence())
'''

'''
from subsystems.render import setBrightness
from settings import PLACEHOLDER_IMAGE_5_ARRAY
from PIL import Image
Image.fromarray(setBrightness(PLACEHOLDER_IMAGE_5_ARRAY, 50)).show()
'''

'''
from subsystems.sprite import iterateThroughSingle
compact = [
    0, 1, "S",
    1, 2, "S"
]
a = iterateThroughSingle(compact, True)

compact = [
    0, 1, "S",
    1, 2, None
]
b = iterateThroughSingle(compact, True)

print(a)
print(b)
print(a == b)
'''

'''
from subsystems.sprite import iterateThroughPath
compact = [0.0, (0.0, 0.0), 'S', 1.0, (0.0, 0.0), 'L', 3.2, (338.0, 330.0), 'L', 11.24, (157.0, 21.0), 'L', 12.2, (866.0, 363.0), 'L']
print(iterateThroughPath(compact, True))
compact = [0.0, (0.0, 0.0), 'L', 1.0, (0.0, 0.0), 'L', 3.2, (338.0, 330.0), 'L', 11.24, (157.0, 21.0), 'L', 12.2, (866.0, 363.0), 'S']
print(iterateThroughPath(compact, True))
compact = [0.0, (0.0, 0.0), 'S', 1.0, (0.0, 0.0), 'S', 1.84, (4.0, 455.0), 'L', 3.24, (105.0, 47.0), 'S', 9.76, (398.0, 112.0), 'S']
print(iterateThroughPath(compact))
compact = [0.0, (0.0, 0.0), 'S', 0.0, (64.0, 104.0), 'S', 1.0, (0.0, 0.0), 'S', 5.24, (714.0, 492.0), 'L', 10.12, (792.0, 59.0), 'S']
print(iterateThroughPath(compact))
'''

'''
from subsystems.sprite import findStateThroughPath
compact = [0.0, (0.0, 0.0), 'S', 2.28, (293.0, 329.0), 'S', 4.8, (656.0, 446.0), 'L', 6.64, (629.0, 109.0), 'S', 10.16, (433.0, 110.0), 'S', 12.08, (127.0, 427.0), 'L']
print(findStateThroughPath(compact,7))
'''

'''
class Thing:
    def __init__(self, id):
        self.id = id

things = [
    Thing(9),
    Thing(5),
    Thing(3),
    Thing(2),
    Thing(1)
]

print(things)
save = things[0]
things.pop(0)
things.insert(1, save)
print(things)
print(things[1].id)
'''

'''
from PIL import Image
from settings import *
images = [PLACEHOLDER_IMAGE_2]
for i in range(10):
    images.append(PLACEHOLDER_IMAGE_2)

images[0].save('test.gif', format='gif', append_images=images[1:], save_all=True, duration=10, loop=0)
'''

'''
from subsystems.bay import CacheManager
from settings import PLACEHOLDER_IMAGE_5
cache = CacheManager()
cache.importImage("C:/Users/henry/Desktop/Projects/GitHub Repositories/tape/resources/placeholder/placeholder5.png")
# now, imagine if I were to accidentally paste my API keys here. no, i didn't do that. except for that one repository. oops.
'''

'''
try:
    doesThisWork = {
        "a": {
            "wait what": {
                "nesting go brr": {
                    "hi": "wait this isn't java",
                    "no": ["it isn't"]
                }
            }
        }
    }
    print(doesThisWork)
except: print("womp womp")
'''
