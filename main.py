import tkinter as tk
from subsystems.window import Window


# window = Window()
# window.start()


from PIL import Image, ImageDraw, ImageFont
import numpy, os

i = 12
text = 'test 123'

font = ImageFont.truetype(os.path.join("resources", "Comfortaa-Medium.ttf"), i)
PIL_image = Image.new('RGB', (100, 100), color=0xffffff)
draw = ImageDraw.Draw(PIL_image)
draw.text((31, 11), text, font=font, fill=10, anchor='mm')
Image.fromarray(numpy.array(PIL_image)).show()