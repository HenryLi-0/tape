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

from subsystems.sprite import findStateThroughSingle, iterateThoughSingle
states = [
    0, 2, "L",
    1, 1, "L",
    3, 3, "S",
    8, 0, "S",
    9, 5, "L",
    15, 10, None
]

# print(findStateThroughSingle(states, 0.9))

# print([(i/10, findStateThroughSingle(states, i/10)) for i in range(100)])
print(iterateThoughSingle(states))