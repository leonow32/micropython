lookup = '0123456789ABCDEF'

def bytes_to_base16(data, separator=" "):
    result = ""
    
    for byte in data:
        nibble_h = byte >> 4
        nibble_l = byte & 0x0F
        
        char_h = lookup[nibble_h]
        char_l = lookup[nibble_l]
        
        result += char_h
        result += char_l
        result += separator
        
    return result.rstrip(separator)
    
if __name__ == "__main__":
    # decoded = b"\x00"
    decoded = b"\xFF"
    decoded = b"\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0A\x0B\x0C\x0D\x0E\x0F"
            
    encoded = bytes_to_base16(decoded, ":")

    print(f"{decoded} -> '{encoded}'")
