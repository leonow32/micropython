lookup = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'

def encode(data):
    """
    Converts bytes, bytearray or string to base64 bytestring.
    
    z trzech bajtów robi cztery znaki ASCII
    """
    
    if isinstance(data, str): data = data.encode()
        
    counter = 0
    length  = len(data)
    result  = str()
    
    #print(f"length = {length}")
    
    for byte in data:
        print(f"=== byte 0x{byte:02X} ({chr(byte)}) {type(byte)}===")
        
        # Przetwarzanie pierwszego bajtu
        if counter % 3 == 0:
            
            # Przetwarzamy pierwszy bajt na Base64
            buffer0 = (byte & 0b11111100) >> 2
            buffer1 = (byte & 0b00000011) << 4
            
            print(f"buffer0 = {buffer0}, 0x{buffer0:02X}, {type(buffer0)}")
            
            char = lookup[buffer0]
            #print(f"char = {char}")
            
            # Wysyłamy pierwszy znak Base64 do bufora wyjściowego
            result += char
            
            # Jeżeli to był ostatni bajt w buforze wejściowym to wstawiamy wypełniacze
            if counter == length:
                result += "=="
                print(f"return at counter = {counter}")
                return result
            
        # Przetwarzanie drugiego bajtu
        elif counter % 3 == 1:
            
            # Przetwarzamy drugi bajt na Base64
            buffer1 |= (byte & 0b11110000) >> 4
            buffer2  = (byte & 0b00001111) << 4
            
            # Wysyłamy drugi znak Base64 do bufora wyjściowego
            char = lookup[buffer1]
            #print(f"char = {char}")
            result += char
            
            # Jeżeli to był ostatni bajt w buforze wejściowym
            if counter == length:
                result += "="
                print(f"return at counter = {counter}")
                return result
        
        # Przetwarzanie trzeciego bajtu
        else:
            
            # Przetwarzamy trzeci bajt na Base64
            buffer2 |= (byte & 0b11000000) >> 6
            buffer3  = (byte & 0b00111111) << 0
            
            # Wysyłamy trzeci i czwarty znak Base64 do bufora wyjściowego
            result += lookup[buffer2]
            result += lookup[buffer3]
            
            if counter == length:
                print(f"return at counter = {counter}")
                return result
            
        
        counter += 1
        
# decoded = b"\x00"
decoded = b"\xFF"
# decoded = b"\x00\x00\x00"
# decoded = b"\x00\x00\x00"
# decoded = b"\x00\x00\xFF"
encoded = encode(decoded)

print(f"{decoded} -> {encoded}")
        