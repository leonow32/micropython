# dict
# key: num
# value: tuple(width, height, space, bitmap)

font = dict()

with open("dos16.font", "w", encoding="utf-8") as result:
    with open("dos16.dat", "r", encoding="utf-8") as source:
        lines = source.readlines()
        num = 0
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
                #dont[num] = ()
                # print("================================")
                # print(f"num: {num}")
                # print(f"height:   {height}")
                # print(f"width:    {width}")
                
                for i in range(len(bitmaps)):
                    bitmaps[i] =  bitmaps[i].replace("0", ".")
                    bitmaps[i] =  bitmaps[i].replace("1", "#")
                    
                # for a in bitmaps:
                    # print(a)
                
                result.write(f"char:{chr(num) if num >= 32 else ""}\n")
                result.write(f"num:{num}\n")
                result.write(f"height:{height}\n")
                result.write(f"width:{width}\n")
                result.write(f"space:0\n")
                for a in bitmaps:
                    result.write(f"{a}\n")
                    
                result.write(f"\n")
            
            elif(line[0] == "#"):
                num = int(line[1:])
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
            
