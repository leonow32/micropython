
with open("dos8.font", "w", encoding="utf-8") as result:
    with open("dos8.dat", "r", encoding="utf-8") as source:
        lines = source.readlines()
        num = 0
        # row = 0
        counter = 0
        first_line = True
        bitmaps = []
        
        for line in lines:
            line = line.strip()
            #print(f"Processing {line}")
            
            if(first_line):
                bitmaps = 8 * [""]
                first_line = False
            
            for i in range(8):
                #print(f"row = {row}")
                bitmaps[7-i] += line[i]
                # row = row + 1
                
            if counter == 7:
                # save char to dict
                #dont[num] = ()
                # print("================================")
                # print(f"num: {num}")
                
                for i in range(len(bitmaps)):
                    bitmaps[i] =  bitmaps[i].replace("0", ".")
                    bitmaps[i] =  bitmaps[i].replace("1", "#")
                    
                # for a in bitmaps:
                    # print(a)
                
                result.write(f"char:{chr(num) if num >= 32 else ""}\n")
                result.write(f"num:{num}\n")
                result.write(f"height:8\n")
                result.write(f"width:8\n")
                result.write(f"space:0\n")
                for a in bitmaps:
                    result.write(f"{a}\n")
                    
                result.write(f"\n")
                
                counter = 0
                num = num + 1
                first_line = True
                
            else:
                counter = counter + 1
            
            
            # row = 0
        
            
