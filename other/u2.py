def U2_decode_8bit(value):
    if value & 0b10000000:
        print("Ujemna    ", end="")
        value = -(~value & 0b01111111) - 1    # ok
#       value = -2**7 + (value & 0b01111111)  # ok
    else:
        print("Dodatnia  ", end="")
        
    print(value)

def U2_decode_12bit(value):
    if value & 0b100000000000:
        print("Ujemna    ", end="")
        value = -(~value & 0b011111111111) - 1    # ok
#        value = -2**11 + (value & 0b011111111111) # ok
        
    else:
        print("Dodatnia  ", end="")
        
    print(value)

def U2_decode(value, bits):
    bits -= 1
    
    if value & (1 << bits):
        print("Ujemna    ", end="")
        mask = 2**bits - 1
        value = -2**bits + (value & mask) # ok
    else:
        print("Dodatnia  ", end="")
        
    print(value)

"""
U2_decode_8bit(0b00000000)
U2_decode_8bit(0b00000001)
U2_decode_8bit(0b00000010)
U2_decode_8bit(0b01111111)
U2_decode_8bit(0b10000000)
U2_decode_8bit(0b11111111)
U2_decode_8bit(0b11111110)
U2_decode_8bit(0b11111101)

U2_decode(0b00000000, 8)
U2_decode(0b00000001, 8)
U2_decode(0b00000010, 8)
U2_decode(0b01111111, 8)
U2_decode(0b10000000, 8)
U2_decode(0b11111111, 8)
U2_decode(0b11111110, 8)
U2_decode(0b11111101, 8)

"""
U2_decode_12bit(0b0000_0000_0000)
U2_decode_12bit(0b0000_0000_0001)
U2_decode_12bit(0b0000_0000_0010)
U2_decode_12bit(0b0111_1111_1111)
U2_decode_12bit(0b1000_0000_0000)
U2_decode_12bit(0b1111_1111_1110)
U2_decode_12bit(0b1111_1111_1111)

U2_decode(0b0000_0000_0000, 12)
U2_decode(0b0000_0000_0001, 12)
U2_decode(0b0000_0000_0010, 12)
U2_decode(0b0111_1111_1111, 12)
U2_decode(0b1000_0000_0000, 12)
U2_decode(0b1111_1111_1110, 12)
U2_decode(0b1111_1111_1111, 12)
