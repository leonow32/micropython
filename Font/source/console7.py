
with open("console7.font", "w", encoding="utf-8") as result:
    with open("console7.dat", "r", encoding="utf-8") as source:
        lines = source.readlines()
        char_num = 32
        first_line = True
        bitmaps = []
        
        for line in lines:
            line = line.strip()
            #print(f"Processing {line}")
            
            if(first_line):
                bitmaps = 7 * [""]
                first_line = False
            
            if len(line) == 0:
                # save char to dict
                #dont[char_num] = ()
                # print("================================")
                # print(f"char_num: {char_num}")
                
                for i in range(len(bitmaps)):
                    bitmaps[i] =  bitmaps[i].replace("0", ".")
                    bitmaps[i] =  bitmaps[i].replace("1", "#")
                    
                # for a in bitmaps:
                    # print(a)
                
                result.write(f"char_num:{char_num}\n")
                result.write(f"height:7\n")
                result.write(f"width:5\n")
                result.write(f"space:1\n")
                for a in bitmaps:
                    result.write(f"{a}\n")
                    
                result.write(f"\n")
                
                char_num = char_num + 1
                first_line = True
                continue
                
            for i in range(1,8):
                #print(f"row = {row}")
                try:
                    bitmaps[7-i] += line[i]
                    #bitmaps[5-i] += line[i]
                except:
                    print(line)
                
                # row = row + 1
            
            
            # row = 0
        
            
