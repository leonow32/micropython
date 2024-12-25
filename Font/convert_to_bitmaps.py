# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

file     = sys.argv[1]    # file name for input *.dat and output *.font
space    = sys.argv[2]    # space between characters

with open(f"{file}.font", "w", encoding="utf-8") as result:
    with open(f"{file}.dat", "r", encoding="utf-8") as source:
        lines      = source.readlines()
        number     = 0
        row        = 0
        width      = 0
        height     = 0
        first_line = True
        bitmaps    = []
        
        for line in lines:
            number += 1
            line = line.strip()
            
            if line[0:2] == "//":
                pos = line.find("'")+1
                if pos == 0:
                    char_num = 0
                else:
                    char = line[pos]
                    char_num = ord(char)
            
            elif len(line) == 0:
                for i in range(len(bitmaps)):
                    bitmaps[i] =  bitmaps[i].replace("0", ".")
                    bitmaps[i] =  bitmaps[i].replace("1", "#")
                    
                result.write(f"char_num:{char_num}\n")
                result.write(f"height:{height}\n")
                result.write(f"width:{width}\n")
                result.write(f"space:{space}\n")
                for bitmap in bitmaps:
                    result.write(f"{bitmap}\n")
                result.write(f"\n")
            
                # Prepare for next character
                char_num   = char_num + 1
                first_line = True
                row        = 0
                width      = 0
                height     = 0
                
            else:
                # Find , in line and cut everything after ,
                line = line[0:line.find(",")]
                
                if(first_line):
                    height = len(line)
                    bitmaps = height * [""]
                    first_line = False
                
                for char in line:
                    try:
                        bitmaps[height-row-1] += char
                    except:
                        print(f"Error at {number} line={line}, row={row}, height={height}, width={width}")
                    row += 1
                
                row = 0
                width += 1
            
