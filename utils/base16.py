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

if __name__ == "__main__":
    import time
    # decoded = b"\x00"
#     decoded = b"\xFF"
#     decoded = b"\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0A\x0B\x0C\x0D\x0E\x0F"
#     decoded = bytearray([0xAA, 0xBB, 0xCC, 0xDD])
    decoded = "ABCD"
            
    time_start = time.time()
    encoded = bytes_to_base16(decoded, ":")
    time_end = time.time()
#     encoded = str_to_base16(decoded, ":")

    print(f"{decoded} -> '{encoded}'")
    print(f"time: {(time_end-time_start) * 1_000_000} us")
