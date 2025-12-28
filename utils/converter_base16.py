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

def decode(data: str) -> bytearray:
    nibble = True
    result = bytearray()
    lookup = '0123456789ABCDEF'
    data   = data.upper()
    
    for byte in data:
        num = lookup.find(byte)
        
        if(num == -1):
            continue
        
        if nibble:
            result.append(num << 4)
        else:
            result[-1] |= num
        
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

