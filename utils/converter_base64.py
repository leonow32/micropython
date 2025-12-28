

def bytes_to_base64(data):
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
#     data_in = b"\x00"
#     data_in = b"\xFF"
#     data_in = b"\x00\x00"
#     data_in = b"\x00\x00\x00"
#     data_in = b"\x00\x00\x00\x00"
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
