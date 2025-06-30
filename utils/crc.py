

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


data   = bytes([0x11, 0x22, 0x44, 0x88])


# result = crc16(data, 0x0589, 0x0000, 0x0000, False, False)     # CRC-16/DECT-X
# result = crc16(data, 0x8005, 0x0000, 0xFFFF, True, True)       # CRC-16/MAXIM-DOW
# result = crc16(data, 0x1021, 0xC6C6, 0x0000, True, True)       # CRC-16/ISO-IEC-14443-3-A
result = crc16(data, 0x1DCF, 0xFFFF, 0xFFFF, False, False)       # CRC-16/PROFIBUS

print(f"Result = {result:04X}")