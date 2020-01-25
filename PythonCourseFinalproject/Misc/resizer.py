
#!/usr/bin/python
from PIL import Image
import os, sys

path = "C:/Users/Vallu/OneDrive/Codes/01_Python_course/Finalé/PNG/"
dirs = os.listdir(path)

def resize():
    for item in dirs:
        if os.path.isfile(path+item):
            im = Image.open(path+item)
            f, e = os.path.splitext(path+item)
            imResize = im.resize((300, 200), Image.ANTIALIAS)
            imResize.save(f + ' resized.png', 'PNG', quality=90)

resize()
