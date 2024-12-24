char_num = 32   # first character in font
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
                print(f"Continue at {number}")
                continue
            
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
                if(first_line):
                    height = len(line)
                    bitmaps = height * [""]
                    first_line = False
                
                # Find , in line and cut everything after ,
                line = line[0:line.find(",")]
                
                for char in line:
                    #print(f"row = {row}")
                    
                    
                    try:
                        bitmaps[row] += char
                        #bitmaps[height-row-1] += char
                    except:
                        print(f"Error at {number} line={line}, row={row}, height={height}, width={width}")
                    row += 1
                
                row = 0
                width += 1
            
