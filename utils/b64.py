def encode(data: bytearray) -> str:
    lookup = b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    result = bytearray()
    
    if isinstance(data, str):
        data = data.encode()

    for i in range(0, len(data), 3):
        fragment = data[i:i+3]
        paddnig  = 3 - len(fragment)
        fragment += b"\x00" * paddnig

        n = (fragment[0] << 16) | (fragment[1] << 8) | fragment[2]

        result.append(lookup[(n >> 18) & 0b00111111])
        result.append(lookup[(n >> 12) & 0b00111111])
        result.append(lookup[(n >>  6) & 0b00111111])
        result.append(lookup[(n      ) & 0b00111111])

        if paddnig:
            result[-paddnig:] = b"=" * paddnig

    return result.decode()

lookup = [
      -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1, 
      -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1, 
      -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1, 0x3E,   -1,   -1,   -1, 0x3F, 
    0x34, 0x35, 0x36, 0x37, 0x38, 0x39, 0x3A, 0x3B, 0x3C, 0x3D,   -1,   -1,   -1,   -1,   -1,   -1, 
      -1, 0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 
    0x0F, 0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17, 0x18, 0x19,   -1,   -1,   -1,   -1,   -1, 
      -1, 0x1A, 0x1B, 0x1C, 0x1D, 0x1E, 0x1F, 0x20, 0x21, 0x22, 0x23, 0x24, 0x25, 0x26, 0x27, 0x28, 
    0x29, 0x2A, 0x2B, 0x2C, 0x2D, 0x2E, 0x2F, 0x30, 0x31, 0x32, 0x33,   -1,   -1,   -1,   -1,   -1, 
      -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1, 
      -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1, 
      -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1, 
      -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1, 
      -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1, 
      -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1, 
      -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1, 
      -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1   
]

def decode(data: str | bytes | bytearray) -> bytearray:
    if isinstance(data, str):
        data = data.encode()

    result = bytearray()
    append = result.append
    i = 0
    
    for byte in data:
        num = lookup[byte]
        
        if num == -1:
            continue;
        
        if i == 0:
            temp = (num << 2) & 0xFF
        elif i == 1:
            append(temp | (num >> 4))
            temp = (num << 4) & 0xFF
        elif i == 2:
            append(temp | (num >> 2))
            temp = (num << 6) & 0xFF
        else:
            append(temp | num)
        
        i += 1
        if i == 4:
            i = 0
        
    return result

if __name__ == "__main__":
    import measure_time
    import mem_used
    
    a = bytearray()

    for i in range(256):
        a.append(i)

    measure_time.begin()
    b = encode(a)
    measure_time.end("encode")
    
    measure_time.begin()
    c = decode(b)
    measure_time.end("decode")
    
    if a == c:
        print("Success")
    else:
        print("Fail")
        print(f"a = {a}")
        print(f"b = {b}")
        print(f"c = {c}")
        
    mem_used.print_ram_used()
