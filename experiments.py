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
# print(bezierPathCoords(path, steps))
# print(selectiveBezierPathCoords(path, steps, 5))