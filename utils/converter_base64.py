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

# 27,6
def decode(data: str) -> bytearray:
    lookup = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    result = bytearray()
    
    for i in range(len(data)):
        num = lookup.find(data[i])
        
        if num == -1:
            continue;
        
        if i%4 == 0:
            temp = (num << 2) & 0xFF
        elif i%4 == 1:
            result.append(temp | (num >> 4))
            temp = (num << 4) & 0xFF
        elif i%4 == 2:
            result.append(temp | (num >> 2))
            temp = (num << 6) & 0xFF
        else:
            result.append(temp | num)
        
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
