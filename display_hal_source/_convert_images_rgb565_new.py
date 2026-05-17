# 250210
import os
import struct
import numpy            # install with "pip install numpy"
from PIL import Image   # install with "pip install pillow"

input_dir  = "image_source_rgb565_new"
output_dir = "../display_hal/image_rgb565_new"

def convert(file):
    print(f"Processing: {file}")
    file = file.replace(".bmp", "")
    
    source = Image.open(f"{input_dir}/{file}.bmp")
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
    
    with open(f"{output_dir}/{file}.bin", "wb") as output:
        output.write(struct.pack(">BHH", 1, width, height))
        output.write(bitmap)

if __name__ == "__main__":
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    files = os.listdir(input_dir)
    
    for file in files:
        if ".bmp" in file:
            convert(file)
