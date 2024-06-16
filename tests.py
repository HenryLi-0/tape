from subsystems.pathing import bezierPathCoords, straightPathCoords
import time
import random
from subsystems.render import *
from settings import *

tests = 0
total = 0

while tests<1000:
    position = (round(random.randrange(-110,522)),round(random.randrange(-110,522)))
    start = time.time()
    img = PLACEHOLDER_IMAGE_ARRAY.copy()
    placeOver(img,PLACEHOLDER_IMAGE_2_ARRAY,position)
    placeOver(img,PLACEHOLDER_IMAGE_2_ARRAY,position)
    placeOver(img,PLACEHOLDER_IMAGE_2_ARRAY,position)
    placeOver(img,PLACEHOLDER_IMAGE_2_ARRAY,position)
    placeOver(img,PLACEHOLDER_IMAGE_2_ARRAY,position)
    placeOver(img,PLACEHOLDER_IMAGE_2_ARRAY,position)
    placeOver(img,PLACEHOLDER_IMAGE_2_ARRAY,position)
    placeOver(img,PLACEHOLDER_IMAGE_2_ARRAY,position)
    placeOver(img,PLACEHOLDER_IMAGE_2_ARRAY,position)
    placeOver(img,PLACEHOLDER_IMAGE_2_ARRAY,position)
    arrayToImage(img)
    end = time.time()
    total+=end-start
    tests+=1
    print(f"{tests} tests | avg: {total/tests} seconds")



# coords = [(0,0),(8,4),(-4,6),(-8,0),(-8,-6)]
# coords = bezierPathCoords(coords,30)
# print(coords)


# merge(PLACEHOLDER_IMAGE, PLACEHOLDER_IMAGE)