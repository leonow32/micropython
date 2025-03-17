def U2_dec(value):
    if value & 0b10000000:
        print("Ujemna")
        result = (~value & 0b01111111) + 1
        result = -result
        
    else:
        print("Dodatnia")
        result = value & 0b01111111
        
    print(result)
    
U2_dec(0b00000000)
U2_dec(0b00000001)
U2_dec(0b00000010)
U2_dec(0b01111111)
U2_dec(0b10000000)
U2_dec(0b11111111)
U2_dec(0b11111110)
U2_dec(0b11111101)