lookup = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"

def bytes_to_base64(data):
    if isinstance(data, str):
        data = data.encode()

    result  = ""
    
    for i in range(len(data)):
        
        if i % 3 == 0:
            buffer0 = (data[i] & 0b11111100) >> 2
            buffer1 = (data[i] & 0b00000011) << 4
            result += lookup[buffer0]
            
            if i == len(data)-1:
                result += lookup[buffer1] + "=="
            
        elif i % 3 == 1:
            buffer1 |= (data[i] & 0b11110000) >> 4
            buffer2  = (data[i] & 0b00001111) << 2
            result += lookup[buffer1]
            
            if i == len(data)-1:
                result += lookup[buffer2] + "="
        
        else:
            buffer2 |= (data[i] & 0b11000000) >> 6
            buffer3  = (data[i] & 0b00111111) << 0
            result += lookup[buffer2]
            result += lookup[buffer3]
    
    return result

def base64_to_bytearray(data):
    result = bytearray()
    
    for i in range(0, len(data), 4):
        chr0 = lookup.find(str(data[i:i+1]))
        chr1 = lookup.find(str(data[i+1:i+2]))
        chr2 = lookup.find(str(data[i+2:i+3]))
        chr3 = lookup.find(str(data[i+3:i+4]))
        result.append(((chr0 << 2) & 0xFF) | (chr1 >> 4))
        result.append(((chr1 << 4) & 0xFF) | (chr2 >> 2))
        result.append(((chr2 << 6) & 0xFF) | (chr3 >> 2))
        
    return result

if __name__ == "__main__":
    import measure_time
    import mem_used
#     decoded = b"\x00"
#     data_in = b"\xFF"
#     data_in = b"\x00\x00"
#     data_in = b"\x00\x00\x00"
#     data_in = b"\x00\x00\xFF"
#     data_in = b"\xFF\x00\x00"
#     data_in = b"\x00\x11\x22\x33\x44\x55\x66\x77\x88\x99\xAA\xBB\xCC\xDD\xEE\xFF"
#     data_in = "\x00\x11\x22\x33\x44\x55\x66\x77\x88\x99\xAA\xBB\xCC\xDD\xEE\xFF"
    data_in  = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
    
    measure_time.begin()
    data_out = bytes_to_base64(data_in)
    measure_time.end("")

#     data_in = "AAAA"
    
#     measure_time.begin()
#     data_out = base64_to_bytearray(data_in)
#     measure_time.end("")    

    print(f"{data_in} -> {data_out}")
    mem_used.print_ram_used()
