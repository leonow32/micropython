def U2_dec_8bit(value):
    if value & 0b10000000:
        print("Ujemna    ", end="")
        value = -(~value & 0b01111111) - 1    # ok
#       value = -2**7 + (value & 0b01111111)  # ok
    else:
        print("Dodatnia  ", end="")
        
    print(value)

def U2_dec_12bit(value):
    if value & 0b100000000000:
        print("Ujemna    ", end="")
        value = -(~value & 0b011111111111) - 1    # ok
#        value = -2**11 + (value & 0b011111111111) # ok
        
    else:
        print("Dodatnia  ", end="")
        
    print(value)


U2_dec_8bit(0b00000000)
U2_dec_8bit(0b00000001)
U2_dec_8bit(0b00000010)
U2_dec_8bit(0b01111111)
U2_dec_8bit(0b10000000)
U2_dec_8bit(0b11111111)
U2_dec_8bit(0b11111110)
U2_dec_8bit(0b11111101)


U2_dec_12bit(0b0000_0000_0000)
U2_dec_12bit(0b0000_0000_0001)
U2_dec_12bit(0b0000_0000_0010)
U2_dec_12bit(0b0111_1111_1111)
U2_dec_12bit(0b1000_0000_0000)
U2_dec_12bit(0b1111_1111_1110)
U2_dec_12bit(0b1111_1111_1111)
