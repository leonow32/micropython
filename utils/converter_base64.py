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

"""
if __name__ == "__main__":
    import measure_time
    import mem_used
#     a = b"\x00"
#     a = b"\xFF"
#     a = b"\x00\x00"
#     a = b"\x00\x00\x00"
#     a = b"\x00\x00\x00\x00"
#     a = b"\x00\x00\xFF"
#     a = b"\xFF\x00\x00"
#     a = b"\x00\x11\x22\x33\x44\x55\x66\x77\x88\x99\xAA\xBB\xCC\xDD\xEE\xFF"
#     a = "\x00\x11\x22\x33\x44\x55\x66\x77\x88\x99\xAA\xBB\xCC\xDD\xEE\xFF"
    a = b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~\x7f\x80\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f\xa0\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad\xae\xaf\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf\xc0\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf\xe0\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff'
#     a  = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
    
    measure_time.begin()
    b = encode(a)
    measure_time.end("")

#     a = "AAAA"
    
#     measure_time.begin()
#     b = decode(a)
#     measure_time.end("")    

    print(f"{a} -> {b}")
    mem_used.print_ram_used()
"""

def decode(data: str) -> bytearray:
    lookup = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    result = bytearray()
    
    def find(char):
        res = lookup.find(char)
        return res if res >= 0 else 0
    
#     length = len(data)
#     print(f"length = {length}")
    
    # Add padding characters (=)  in case they are missing
    if len(data) % 4:
        data += '=' * (4 - len(data) % 4)
    
#     print(f"data = '{data}'")
    
    for i in range(0, len(data), 4):
        fragment = data[i:i+4]
#         print(f"{fragment} ", end="")
#         print(f"{fragment[0]} {lookup.find(fragment[0]):02} ", end="")
        
        buffer = (find(fragment[0]) << 18) | \
                 (find(fragment[1]) << 12) | \
                 (find(fragment[2]) <<  6) | \
                 (find(fragment[3]))
        
#         print(f"0x{buffer:06X}")
        
        result.append((buffer >> 16) & 0xFF)
        result.append((buffer >>  8) & 0xFF)
        result.append((buffer      ) & 0xFF)
        
#         print()
        
#         chr0 = lookup.find(str(data[i:i+1]))
#         chr1 = lookup.find(str(data[i+1:i+2]))
#         chr2 = lookup.find(str(data[i+2:i+3]))
#         chr3 = lookup.find(str(data[i+3:i+4]))
#         result.append(((chr0 << 2) & 0xFF) | (chr1 >> 4))
#         result.append(((chr1 << 4) & 0xFF) | (chr2 >> 2))
#         result.append(((chr2 << 6) & 0xFF) | (chr3 >> 2))

    if data.count('=') == 2:
#         print("aaaa")
        return result[0:-2]
    elif data.count('=') == 1:
#         print("bbbb")
        return result[0:-1]
#         
#     print("cccc")
    else:
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
    
    """
#     a = "AA==" # 00
#     a = "AQ==" # 01
#     a = "AAA=" # 00 00
    a = "AAAB" # 00 00 01
#     a = "ABEiM0RVZneImaq7zN3u/w==" # 00112233445566778899AABBCCDDEEFF
    
    measure_time.begin()
    b = decode(a)
    measure_time.end("")

    print(f"{a} -> {b}")
    mem_used.print_ram_used()
    """
