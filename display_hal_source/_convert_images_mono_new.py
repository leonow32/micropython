# 250131
import os
import struct
import numpy            # install with "pip install numpy"
from PIL import Image   # install with "pip install pillow"

input_dir  = "image_source_mono"
output_dir = "../display_hal/image_mono_new"

def convert(file):
    print(f"Processing: {file}")
    file = file.replace(".bmp", "")
    
    source = Image.open(f"{input_dir}/{file}.bmp")
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
        
    with open(f"{output_dir}/{file}.bin", "wb") as output:
        output.write(struct.pack(">BHH", 0, width, height))   # 0 = framebuf.MONO_VLSB
        output.write(bitmap)

if __name__ == "__main__":
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    files = os.listdir(input_dir)
    
    for file in files:
        if ".bmp" in file:
            convert(file)
