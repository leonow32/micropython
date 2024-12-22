# dict
# key: char_num
# value: tuple(width, height, spacing, bitmap)

font = dict()

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
        print(f"Processing {line}")
        
        if len(line) == 0:
            # save char to dict
            #dont[char_num] = ()
            print("end")
            row = 0
            first_line = True
            width = 0
            height = 0
            
            print("================================")
            for a in bitmaps:
                print(a)
            print("================================")
        
        elif(line[0] == "#"):
            char_num = int(line[1:])
            
            first_line = True
            
        else:
            if(first_line):
                height = len(line)
                bitmaps = height * [""]
                first_line = False
            
            for char in line:
                print(f"row = {row}")
                bitmaps[height-row-1] += char
                row = row + 1
            
            row = 0
            width = width + 1
        

        
    