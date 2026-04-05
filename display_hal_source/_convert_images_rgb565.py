# 250210
import os
import sys
import numpy            # install with "pip install numpy"
from PIL import Image   # install with "pip install pillow"

def convert(file):
    print(f"Processing: {file}")
    file = file.replace(".bmp", "")
    
    source = Image.open(f"image_source_rgb565/{file}.bmp")
    source.load()
    width, height = source.size
    source = numpy.array(source)
    bitmap = bytearray(width * height * 2)
    
    for row in range(height):
        for column in range(width):
            r, g, b = source[row, column]
            byte_l = ((r & 0b11111000) << 0) | ((g & 0b11100000) >> 5)
            byte_h = ((g & 0b00011100) << 3) | ((b & 0b11111000) >> 3)
            bitmap[2*(row*width+column)+0] = byte_l
            bitmap[2*(row*width+column)+1] = byte_h
    
    with open(f"../display_hal/image_rgb565/{file}.py", "w", encoding="utf-8") as output:
        output.write("import framebuf\n")
        output.write(f"{file} = framebuf.FrameBuffer({bitmap}, {width}, {height}, framebuf.RGB565)\n")

if __name__ == "__main__":
    if not os.path.exists("../display_hal/image_rgb565"):
        os.makedirs("../display_hal/image_rgb565")
        
    files = os.listdir("image_source_rgb565")
    
    for file in files:
        if ".bmp" in file:
            convert(file)
