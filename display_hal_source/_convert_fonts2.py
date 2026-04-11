# 250301
import os

input_dir  = "font_source"
output_dir = "../display_hal/font2"

def convert(file):
    print(f"Processing: {file}")
    file = file.replace(".font", "")

    bitmap = bytearray()

    with open(f"{output_dir}/{file}.py", "w", encoding="utf-8") as result:
        result.write("import framebuf\n")
        result.write(f"{file} = {{\n")
        
        with open(f"{input_dir}/{file}.font", "r", encoding="utf-8") as source:
            lines = source.readlines()
            
            for line in lines:
                line = line.strip()
                
                if "char" in line:
                    continue
                
                elif "num" in line:
                    num = int(line[line.find(":")+1:])
                
                elif "width" in line:
                    width = int(line[line.find(":")+1:])
                    
                elif "height" in line:
                    height = int(line[line.find(":")+1:])
                    
                elif "space" in line:
                    space = int(line[line.find(":")+1:])
                    
                elif len(line) == 0:
                    output = bytearray([width]) + bytearray([height]) + bytearray([space]) + bitmap
                    #result.write(f"{num}: {output},\n")
                    result.write(f"{num}: ({width}, {height}, {space}, framebuf.FrameBuffer({bitmap}, {width}, {height}, framebuf.MONO_VLSB)),\n")
                    
                    bitmap = bytearray()
                    
                elif "." in line or "#" in line:
                    if len(bitmap) == 0:
                        bitmap = bytearray(width * height // 8)
                        x = 0
                        y = 0
                    
                    for pixel in line:
                        if pixel == "#":
                            address = (y // 8) * width + x
                            bitmap[address] |= 1 << (y % 8)
                            
                        x += 1
                        if x == width:
                            x = 0
                        
                    y += 1
                        
        result.write("}\n")

if __name__ == "__main__":
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    files = os.listdir(input_dir)
    
    for file in files:
        if ".font" in file:
            convert(file)