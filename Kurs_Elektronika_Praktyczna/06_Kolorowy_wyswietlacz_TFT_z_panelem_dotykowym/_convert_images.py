# 250210
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
    bitmap = bytearray(width * height * 2)
    print(f"Height: {height}")
    print(f"Width:  {width}")
    
    for row in range(height):
        for column in range(width):
            r, g, b = source[row, column]
            byte_l = ((r & 0b11111000) << 0) | ((g & 0b11100000) >> 5)
            byte_h = ((g & 0b00011100) << 3) | ((b & 0b11111000) >> 3)
            bitmap[2*(row*width+column)+0] = byte_l
            bitmap[2*(row*width+column)+1] = byte_h
        
    result = f"{name} = framebuf.FrameBuffer({bitmap}, {width}, {height}, framebuf.RGB565)\n"
    return result

if __name__ == "__main__":
    image_files = os.listdir("image_source")
    print(image_files)
    for image_file in image_files:
        if ".bmp" in image_file:
            output_file = image_file.replace("bmp", "py")
            with open(f"image/{output_file}", "w", encoding="utf-8") as output:
                output.write("import framebuf\n")
                output.write(convert(image_file))
        
