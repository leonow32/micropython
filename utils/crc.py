# 2025.07.02

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
    data   = bytes([0x11, 0x22, 0x44, 0x88])
    
    assert crc(data, 8, 0x2F, 0xFF, 0xFF, False, False) == 0xD7
    assert crc8(data, 0x2F, 0xFF, 0xFF, False, False) == 0xD7
    
    assert crc(data, 8, 0x31, 0x00, 0x00, True, True) == 0x82
    assert crc8(data, 0x31, 0x00, 0x00, True, True) == 0x82
    
    assert crc(data, 8, 0x1D, 0xC7, 0x00, False, False) == 0xD7
    assert crc8(data, 0x1D, 0xC7, 0x00, False, False) == 0xD7
    
    assert crc(data, 16, 0x0589, 0x0000, 0x0000, False, False) == 0xDCBF
    assert crc16(data, 0x0589, 0x0000, 0x0000, False, False) == 0xDCBF
    
    assert crc(data, 16, 0x1021, 0xC6C6, 0x0000, True, True) == 0x16DF
    assert crc16(data, 0x1021, 0xC6C6, 0x0000, True, True) == 0x16DF
    
    assert crc(data, 16, 0x8005, 0x0000, 0xFFFF, True, True) == 0xAF69
    assert crc16(data, 0x8005, 0x0000, 0xFFFF, True, True) == 0xAF69
    
    assert crc(data, 16, 0x1DCF, 0xFFFF, 0xFFFF, False, False) == 0x739D
    assert crc16(data, 0x1DCF, 0xFFFF, 0xFFFF, False, False) == 0x739D
    
    assert crc(data, 32, 0xF4ACFB13, 0xFFFFFFFF, 0xFFFFFFFF, True, True) == 0x749DC2A3
    assert crc32(data, 0xF4ACFB13, 0xFFFFFFFF, 0xFFFFFFFF, True, True) == 0x749DC2A3

    print("OK")
