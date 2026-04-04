# 250131
import os
import sys
import numpy            # install with "pip install numpy"
from PIL import Image   # install with "pip install pillow"

def convert(file):
    print(f"Processing: {file}")
    file = file.replace(".bmp", "")
    
    source = Image.open(f"image_source_mono/{file}.bmp")
    source.load()
    width, height = source.size
    source = numpy.array(source)
    bitmap = bytearray(width * height // 8)
    
    for row in range(height):
        for column in range(width):
            if source[row,column] == 0: # if pixel is visible (LED is ON)
                page = row // 8
                bit  = 1 << (row % 8)
                bitmap[page * width + column] |= bit
        
    with open(f"../display_hal/image_mono/{file}.py", "w", encoding="utf-8") as output:
        output.write("import framebuf\n")
        output.write(f"{file    } = framebuf.FrameBuffer({bitmap}, {width}, {height}, framebuf.MONO_VLSB)\n")

if __name__ == "__main__":
    if not os.path.exists("../display_hal/image_mono"):
        os.makedirs("../display_hal/image_mono")
    
    image_files = os.listdir("image_source_mono")
    
    for image_file in image_files:
        if ".bmp" in image_file:
            convert(image_file)
