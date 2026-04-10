from random import randint

def print_key(name, sbox):
    print(f"    constexpr uint8_t {name}[256] = {{ ")
    print("    //     0     1     2     3     4     5     6     7     8     9     A     B     C     D     E     F")
    for i, byte in enumerate(sbox):
        if i%16 == 0: print("        ", end="")
        print(f"0x{byte:02X}, ", end="")
        if i%16 == 15: print(f"// {((i//16)*16):02X}")
    print("    };")

def generate_key_a():
    key_a = bytearray()

    while True:
        value = randint(0x00, 0xFF).to_bytes()
        if key_a.find(value) == -1:
            key_a.extend(value)
            
            if len(key_a) == 256:
                return bytes(key_a)

def generate_key_b(key_a):
    key_b = bytearray()
    
    for i in range(256):
        key_b.append(key_a.find(i.to_bytes()))
        
    return bytes(key_b)

def encrypt(key_a, plaintext):
    if isinstance(plaintext, str):
        plaintext = plaintext.encode()
    
    ciphertext = bytearray(len(plaintext))
    for i, byte in enumerate(plaintext):
        ciphertext[i] = key_a[byte ^ (i & 0xFF)]

    return ciphertext

def decrypt(key_b, ciphertext):
    plaintext = bytearray(len(ciphertext))
    for i, byte in enumerate(ciphertext):
        plaintext[i] = key_b[byte] ^ (i & 0xFF)
        
    return plaintext

def encrypt2(key_a, plaintext):
    if isinstance(plaintext, str):
        plaintext = plaintext.encode()
    
    length = len(plaintext)
    ciphertext = bytearray(length)
    for i, byte in enumerate(plaintext):
        ciphertext[i] = key_a[byte ^ (i & 0xFF)]
        if i>0: ciphertext[i] = ciphertext[i] ^ ciphertext[i-1]
        
#     for i in range(length):
#         ciphertext[i] = key_a[plaintext[i] ^ (i & 0xFF)]
#         if i>0: ciphertext[i] = ciphertext[i] ^ ciphertext[i-1]

    return ciphertext

def decrypt2(key_b, ciphertext):
    length = len(ciphertext)
    plaintext = bytearray(length)
    for i, byte in enumerate(ciphertext):
        if i>0: byte = byte ^ ciphertext[i-1]
        plaintext[i] = key_b[byte] ^ (i & 0xFF)

#     for i in range(length):
#         if i>0: ciphertext[i] = ciphertext[i] ^ ciphertext[i-1]
#         plaintext[i] = key_b[ciphertext[i]] ^ (i & 0xFF)
        
    return plaintext

if __name__ == "__main__":
    import measure_time
#     key_a = generate_key_a()
#     key_b = generate_key_b(key_a)
    
    key_a = b'*\\\x8e\xa2\x9a\xb1?"\x14RP\xd9\x81#\x18O@\xf4D\xc1j\x1d):\x1a\xcfC;n\xab\x8f\x0e\xe2\xbc\xd6\xa5^,\xd4\xd2\xaes\xfaJ\xfeX\x97Q\x93\x04\x8c\x17\xb9\x02l\xa3a\x9bF \xdb\xcb\x86\xb8\x0f\x88\xf6\xb7!\xd3\xafr\xbb\xf1\x00LB\xeam\xbf2\x01&\xe1%I\xde\xec~$\x03\x8b\x9eo\xfb\x82W\xad\xee\xa1\xf7x\x08\r\x91\xf0\xcd\xc9h\xa8\xb2\x90UK\x15AV\xb4S\x16\xe3\xcc\xa7\xed\x9d\xdf\x19\'\x85\xfd4+\xaa\xf8\xb0\xbd\xf2\xe4\x92>f\x1f\x0b\xb6\x0c\xc0[\x11\x84M(gu.\xa9\xbe\x05\xf5\xd1\xa4\xda\x96\x8d\xe8\x07\x9f\xb5\x89\xeb\xd7\xc3d8c\xa6\xdc\xe0\xb3\xe6N\x13T\xf3\n\xacY`z\xc7w\x1c6\xc2\xd0\xc5k\xc6q\x06\xceHG\x99Ev|_\x10\x94\x9c\xef0\x831\x7fp7b\x98\xe9/\x80]\xff\t<\x95{\x8ai\x12\xc4\xca\xe5\xf9\xddy-e\xc8\xd8\xfc\x1e\xd5\xe7\x1b9Zt3=}\xa0\x875\xba'
    key_b = b'JQ5Z1\x9c\xc6\xa4f\xe0\xb7\x8e\x90g\x1f@\xcf\x93\xe6\xb4\x08rw3\x0e~\x18\xf5\xbe\x15\xf2\x8d;D\x07\rYTR\x7f\x96\x16\x00\x83%\xed\x99\xdc\xd3\xd5P\xf9\x82\xfe\xbf\xd8\xac\xf6\x17\x1b\xe1\xfa\x8b\x06\x10sL\x1a\x12\xcb:\xc9\xc8U+qK\x95\xb3\x0f\n/\tv\xb5pt`-\xb9\xf7\x92\x01\xde$\xce\xba8\xd9\xad\xab\xee\x8c\x97l\xe5\x14\xc36N\x1c]\xd7\xc5G)\xf8\x98\xcc\xbde\xec\xbb\xe3\xcd\xfbX\xd6\xdd\x0c_\xd4\x94\x80>\xfdA\xa7\xe4[2\xa2\x02\x1eoh\x8a0\xd0\xe2\xa1.\xda\xca\x049\xd1|\\\xa5\xfcc\x037\x9f#\xaezm\x9a\x84\x1d\xb8a(F\x86\x05n\xb1u\xa6\x8fC?4\xffH!\x87\x9bO\x91\x13\xc0\xaa\xe7\xc2\xc4\xbc\xefk\xe8=yj\xc7\x19\xc1\x9e\'E&\xf3"\xa9\xf0\x0b\xa0<\xaf\xebV}\xb0S x\x89\xe9\xb2\xf4\xa3\xdbM\xa8W{b\xd2iI\x88\xb6\x11\x9dBd\x85\xea*^\xf1\x81,\xdf'
    
    def print_hex(caption, data):
        print(f"{caption}: ", end="")
        for byte in data:
            print(f"{byte:02X}", end=" ")
        print()

#     print_key("key_a", key_a)
#     print_key("key_b", key_b)

#     a = b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~\x7f\x80\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f\xa0\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad\xae\xaf\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf\xc0\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf\xe0\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff'
    a = b'\x00\x11\x22\x33\x44\x55\x66\x77\x88\x99\xAA\xBB\xCC\xDD\xEE\xFF'
    
    measure_time.begin()
    b = encrypt(key_a, a)
    c = decrypt(key_b, b)
    measure_time.end("Time")
    
    measure_time.begin()
    
    print_hex("A", a)
    b = encrypt2(key_a, a)
    print_hex("B", b)
    c = decrypt2(key_b, b)
    print_hex("C", c)
    measure_time.end("Time2")
    
    if a == c:
        print("OK")
    else:
        print("ERROR")
