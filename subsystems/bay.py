'''This file contatins functions for managing data'''

from PIL import Image, ImageFont
import os, numpy, uuid, ast

def check():
    '''Verify that the master cache is exists and is ready'''
    try:
        with open(os.path.join("storage", "cache.txt"), "r") as f:
            f.read()     
    except:
        print("The file at storage/cache.txt doesn't exist! Creating a new cache.txt.")
        with open(os.path.join("storage", "cache.txt"), "x") as f:
            f.write("")

    # with open(os.path.join("storage", "cache.txt"), "w") as f:
    #     f.write("")



def importImage(imagePath):
    imagePath = "C:/Users/henry/Downloads/image.png"    
    image = numpy.array(Image.open(imagePath).convert("RGBA"))
    open(os.path.join("storage", "cache.txt"), "a")



with open(os.path.join("storage", "cache.txt"), "r") as f:
    result = ast.literal_eval(f.read())
    print(result)
    print(type(result))