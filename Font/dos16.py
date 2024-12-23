# dict
# key: char_num
# value: tuple(width, height, spacing, bitmap)

font = dict()

with open("dos16.font", "w", encoding="utf-8") as result:
    with open("dos16.dat", "r", encoding="utf-8") as source:
        lines = source.readlines()
        char_num = 0
        row = 0
        width = 0
        height = 0
        first_line = True
        bitmaps = []
        
        for line in lines:
            line = line.strip()
            #print(f"Processing {line}")
            
            if len(line) == 0:
                # save char to dict
                #dont[char_num] = ()
                # print("================================")
                # print(f"char_num: {char_num}")
                # print(f"height:   {height}")
                # print(f"width:    {width}")
                
                for i in range(len(bitmaps)):
                    bitmaps[i] =  bitmaps[i].replace("0", ".")
                    bitmaps[i] =  bitmaps[i].replace("1", "#")
                    
                # for a in bitmaps:
                    # print(a)
                
                result.write(f"char_num:{char_num}\n")
                result.write(f"height:{height}\n")
                result.write(f"width:{width}\n")
                for a in bitmaps:
                    result.write(f"{a}\n")
                    
                result.write(f"\n")
            
            elif(line[0] == "#"):
                char_num = int(line[1:])
                first_line = True
                row = 0
                width = 0
                height = 0
                
            else:
                if(first_line):
                    height = len(line)
                    bitmaps = height * [""]
                    first_line = False
                
                for char in line:
                    #print(f"row = {row}")
                    bitmaps[height-row-1] += char
                    row = row + 1
                
                row = 0
                width = width + 1
            
