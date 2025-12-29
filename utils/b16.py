def encode(data: bytearray, separator=None) -> str:
    result = bytearray()
    lookup = b'0123456789ABCDEF'
    
    if isinstance(data, str):
        data = data.encode()
    
    if separator:
        separator = ord(separator)
                        
        for byte in data:
            result.append(lookup[byte >> 4])
            result.append(lookup[byte & 0x0F])
            result.append(separator)
            
        return result[0:-1].decode()
    
    else:
        for byte in data:
            result.append(lookup[byte >> 4])
            result.append(lookup[byte & 0x0F])
        return result.decode()

lookup = [
      -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1, 
      -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1, 
      -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1, 
    0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09,   -1,   -1,   -1,   -1,   -1,   -1, 
      -1, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1, 
      -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1, 
      -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1, 
      -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1, 
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
    
    nibble = True
    result = bytearray()
    data   = data.upper()
    temp   = 0
    append = result.append
    
    for byte in data:
        num = lookup[byte]
        
        if(num == -1):
            continue
        
        if nibble:
            temp = num << 4
        else:
            append(temp | num)
        
        nibble = not nibble
        
    return result

if __name__ == "__main__":
    import measure_time
    import mem_used
    
    a = bytearray()
    
    for i in range(256):
        a.append(i)
    
    measure_time.begin()
    b = encode(a, " ")
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

