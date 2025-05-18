# 250131
import os
import sys
import numpy            # instalacja poleceniem "pip install numpy"
from PIL import Image   # instalacja poleceniem "pip install pillow"

def convert(name):
    print(f"Processing: {name}")
    source = Image.open(f"image_source/{name}")
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
    if not os.path.exists("image"):
        os.makedirs("image")
    
    image_files = os.listdir("image_source")
    print(image_files)
    for image_file in image_files:
        if ".bmp" in image_file:
            output_file = image_file.replace("bmp", "py")
            with open(f"image/{output_file}", "w", encoding="utf-8") as output:
                output.write("import framebuf\n")
                output.write(convert(image_file))
        
