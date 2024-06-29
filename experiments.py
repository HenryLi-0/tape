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
from subsystems.pathing import smoothChangeAt
print(smoothChangeAt(25,50,10))