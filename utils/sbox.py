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

if __name__ == "__main__":
    key_a = generate_key_a()
    key_b = generate_key_b(key_a)

    print_key("key_a", key_a)
    print_key("key_b", key_b)
