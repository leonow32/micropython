

def bytes_to_base16(data, separator=None):
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
            
        return result[0:-1]
    
    else:
        for byte in data:
            result.append(lookup[byte >> 4])
            result.append(lookup[byte & 0x0F])
        return result

def base16_to_bytes(data):
    even = True
    result = bytearray()
    lookup = b'0123456789ABCDEF'
    
    if isinstance(data, str):
        data = data.encode()
        
    data = data.upper()
    
    for byte in data:
        num = lookup.find(byte)
        if(num == -1):
            continue
        
        if even:
            result.append(num << 4)
        else:
            result[-1] |= num
        
        even = not even
        
    return bytes(result)

if __name__ == "__main__":
    import measure_time
    import mem_used
    
    data_in = bytearray()
    
    for i in range(256):
        data_in.append(i)
    
    measure_time.begin()
    data_out = bytes_to_base16(data_in, " ")
    measure_time.end("")
    
    print(f"{data_in} -> {data_out}")
    mem_used.print_ram_used()