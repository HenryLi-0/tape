'''This file contatins functions for managing the cache data storage'''

from PIL import Image
import os, numpy, uuid, ast
from settings import *

class CacheManager:
    def __init__(self):
        '''A class for managing the cache data storage'''
        CacheManager.check()
        with open(os.path.join("storage", "cache.txt"),"r") as f:
            file = f.read()
            if len(file) > 0:
                self.cache = ast.literal_eval(file)
            else:
                self.cache = {}
    
    def saveCache(self):
        '''Saves self.cache into cache.txt'''
        with open(os.path.join("storage", "cache.txt"),"w") as f:
            f.write(str(self.cache))
    
    def check():
        '''Verify that cache.txt exists and is ready'''
        try:
            with open(os.path.join("storage", "cache.txt"), "r") as f:
                f.read()     
        except:
            print("The file at storage/cache.txt doesn't exist! Creating a new cache.txt.")
            with open(os.path.join("storage", "cache.txt"), "x") as f:
                f.write({})

    def importImage(self,imagePath):   
        '''Imports an image given the path'''     
        image = numpy.array(Image.open(imagePath).convert("RGBA"))
        id = str(uuid.uuid4())
        self.cache[id]=str(imagePath)
        numpy.save(os.path.join("storage", f"{id}.npy"),image)
        self.saveCache()

    def removeImage(self, id):
        '''Removes an image given its UUID'''
        try:
            os.remove(os.path.join("storage",f"{id}.npy"))
            self.cache.remove(id)
            self.saveCache()
        except:
            pass
    
    def getImage(self,id):
        '''Retrieves an image as an array given its UUID. If the image does not exist, it will attempt to recreate it given its stored path. If this fails, the UUID will be removed from the cache.'''
        try:
            return numpy.load(os.path.join("storage",f"{id}.npy")).astype("uint8")
        except:
            print(f"ID {id} doesn't exist! Attempting to recreate")
            try:
                image = numpy.array(Image.open(self.cache[id]).convert("RGBA"))
                numpy.save(os.path.join("storage", f"{id}.npy"),image)
                print("Recreation successful")
                return numpy.load(os.path.join("storage",f"{id}.npy")).astype("uint8")
            except:
                print(f"Recreation unsuccesful, removing {id} from cache")
                self.cache.remove(id)
                self.saveCache()
                return MISSING_IMAGE_ARRAY.astype("uint8")
            
    def getKeys(self):
        '''Returns all UUIDs stored in the cache'''
        return list(self.cache.keys())