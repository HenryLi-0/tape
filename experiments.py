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

thing.setData("c", [0,(0,0),"L",5,(1,1),"S",7,(10,10),"S",10,(10,0),None])
thing.setData("r", [0, 0, "S", 5, 90, "L", 10, 0, None])
thing.setData("a", [0, 0, "L", 5, 1, None])
thing.setData("s", [0, 100, "L", 15, 50, None])
thing.setData("h", [0, 0, None])
thing.setData("t", [0, 0, None])
thing.setData("b", [0, 0, None])
thing.setData("w", [0, 0, None])

print(thing.generateFullSequence())
'''

from subsystems.render import setTransparency
from settings import PLACEHOLDER_IMAGE_2_ARRAY
from PIL import Image
Image.fromarray(setTransparency(PLACEHOLDER_IMAGE_2_ARRAY, 92)).show()