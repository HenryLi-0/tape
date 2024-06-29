'''The class all about the sprites, which are the manipulatable images that move across the screen.'''


'''
Sprite Data Storage:
c (coord)   - coords compact path         (x,y)
r (rots)    - rotations compact path      (dir)
p (path)    - full path compact path      (x,y,dir)
s (->)      - size path
h (hue)     - color effect
t (->)      - transparency
b (->)      - brightness
w (weird)   - pixelation

compact coords storage: (x,y), (straight, beizer), (x,y)...     (x and y are coords)
compact rotations storage: (deg), (straight, beizer), (deg)...  (deg are degrees)
compact effect storage: (t, y), (straight, curve), (t, y)...    (t and y is time and strength)
'''
class Sprite:
    def __init__(self,name):
        self.name = name
        self.data = []
    def addData(self, data):
        self.data.append(data)
    def getData(self):
        return self.data
    
