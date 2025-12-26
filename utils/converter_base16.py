lookup = '0123456789ABCDEF'

def bytes_to_base16(data, separator=" "):
    if isinstance(data, str):
        data = data.encode()
    
    result = ""
    
    for byte in data:
        result += lookup[byte >> 4]
        result += lookup[byte & 0x0F]
        result += separator
        
    return result.rstrip(separator)

def base16_to_bytes(data):
    even = True
    result = bytearray()
    
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
