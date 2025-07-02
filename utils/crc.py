def crc(data, bits, poly, init, xor_out, reflect_in, reflect_out):
    crc = init;

    for byte in data:
        mask = 0b00000001 if reflect_in else 0b10000000
        while mask:
            bit = 1 if byte & mask else 0
            msb = crc >> (bits-1)
            crc = (crc << 1) & ((2**bits)-1)

            if bit != msb:
                crc = crc ^ poly
                
            if reflect_in:
                mask = (mask << 1) & 0xFF
            else:
                mask = mask >> 1

    result = 0
    
    if reflect_out:
        for i in range(bits):
            if crc & (1<<i):
                result = result | (1<<(bits-1-i))
    else:
        result = crc

    return result ^ xor_out;

def crc8(data, poly, init, xor_out, reflect_in, reflect_out):
    crc = init;

    for byte in data:
        mask = 0b00000001 if reflect_in else 0b10000000
        while mask:
            bit = 1 if byte & mask else 0
            msb = crc >> 7
            crc = (crc << 1) & 0xFF

            if bit != msb:
                crc = crc ^ poly
                
            if reflect_in:
                mask = (mask << 1) & 0xFF
            else:
                mask = mask >> 1

    result = 0
    
    if reflect_out:
        for i in range(8):
            if crc & (1<<i):
                result = result | (1<<(7-i))
    else:
        result = crc

    return result ^ xor_out;


def crc16(data, poly, init, xor_out, reflect_in, reflect_out):
    crc = init;

    for byte in data:
        mask = 0b00000001 if reflect_in else 0b10000000
        while mask:
            bit = 1 if byte & mask else 0
            msb = crc >> 15
            crc = (crc << 1) & 0xFFFF

            if bit != msb:
                crc = crc ^ poly
                
            if reflect_in:
                mask = (mask << 1) & 0xFF
            else:
                mask = mask >> 1

    result = 0
    
    if reflect_out:
        for i in range(16):
            if crc & (1<<i):
                result = result | (1<<(15-i))
    else:
        result = crc

    return result ^ xor_out;

def crc32(data, poly, init, xor_out, reflect_in, reflect_out):
    crc = init;

    for byte in data:
        mask = 0b00000001 if reflect_in else 0b10000000
        while mask:
            bit = 1 if byte & mask else 0
            msb = crc >> 31
            crc = (crc << 1) & 0xFFFFFFFF

            if bit != msb:
                crc = crc ^ poly
                
            if reflect_in:
                mask = (mask << 1) & 0xFF
            else:
                mask = mask >> 1

    result = 0
    
    if reflect_out:
        for i in range(32):
            if crc & (1<<i):
                result = result | (1<<(31-i))
    else:
        result = crc

    return result ^ xor_out;

if __name__ == "__main__":
#     data   = bytes([0x11, 0x22, 0x44, 0x88])
    data   = bytes([])
    
    
    """

    result = crc16()     # CRC-16/DECT-X
    result = crc16()         # CRC-16/MAXIM-DOW
    result = crc16()       # CRC-16/ISO-IEC-14443-3-A
    result = crc16()     # CRC-16/PROFIBUS
    print(f"Result = {result:04X}")

    result = crc32(data, 0x814141AB, 0x00000000, 0x00000000, False, False)     # CRC-16/AIXM
    """
    result = crc32(data, 0xF4ACFB13, 0xFFFFFFFF, 0xFFFFFFFF, True, True)     # CRC-16/AUTOSAR
    print(f"Result = {result:08X}")
    
    
    assert crc32(data, 0xF4ACFB13, 0xFFFFFFFF, 0xFFFFFFFF, True, True) == 0x749DC2A3
    print("OK")
