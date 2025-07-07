import sys
import os

def convert(file):
    print(f"Processing: {file}")
    file = file.replace(".font", "")
    
    with open(f"font/{file}.py", "w", encoding="utf-8") as result:
        result.write(f"{file} = {{\n")
        
        with open(f"font_source/{file}.font", "r", encoding="utf-8") as source:
            lines  = source.readlines()
            bitmap = bytearray()
            
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
                    result.write(f"{num}: {output},\n")
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
    if not os.path.exists("font"):
        os.makedirs("font")
    
    font_files = os.listdir("font_source")

    for font_file in font_files:
        if ".font" in font_file:
            convert(font_file)

