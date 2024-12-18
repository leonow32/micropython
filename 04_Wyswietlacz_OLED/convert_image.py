# 241218
import os
import sys
import numpy
from PIL import Image

def convert(name):
    print(f"Processing: {name}")
    source = Image.open(name)
    name = name.replace(".bmp", "")
    source.load()
    width, height = source.size
    source = numpy.array(source)
    bitmap = bytearray(width * height // 8)
    print(f"Height: {height}")
    print(f"Width:  {width}")
    
    for row in range(height):
        for column in range(width):
            if source[row,column] == 0: # if pixel is visible (LED is ON)
                print("#", end="")
                page = row // 8
                bit  = 1 << (row % 8)
                bitmap[page * width + column] |= bit
            else:
                print(".", end="")
        print("")
        
    result = f"{name} = framebuf.FrameBuffer({bitmap}, {width}, {height}, framebuf.MONO_VLSB)\n"
    return result

if __name__ == "__main__":
    with open("images.py", "w", encoding="utf-8") as images:
        images.write("import framebuf\n")
        files = os.listdir()
        for file in files:
            if ".bmp" in file:
                images.write(convert(file))
        
