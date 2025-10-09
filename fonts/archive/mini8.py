num = 32   # first character in font
space    = 1    # common spacing for each character

with open("mini8.font", "w", encoding="utf-8") as result:
    with open("mini8.dat", "r", encoding="utf-8") as source:
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
                continue
            
            elif len(line) == 0:
                for i in range(len(bitmaps)):
                    bitmaps[i] =  bitmaps[i].replace("0", ".")
                    bitmaps[i] =  bitmaps[i].replace("1", "#")
                    
                result.write(f"char:{chr(num) if num >= 32 else ""}\n")
                result.write(f"num:{num}\n")
                result.write(f"height:{height}\n")
                result.write(f"width:{width}\n")
                result.write(f"space:{space}\n")
                for bitmap in bitmaps:
                    result.write(f"{bitmap}\n")
                result.write(f"\n")
            
                # Prepare for next character
                num   = num + 1
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
            
