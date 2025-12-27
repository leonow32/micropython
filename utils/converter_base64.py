lookup = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"

def bytes_to_base64(data):
    if isinstance(data, str):
        data = data.encode()
        
    counter = 0
    length  = len(data)-1
    result  = ""
    
    for byte in data:
#         print(f"=== byte 0x{byte:02X} ===")
        
        # Przetwarzanie pierwszego bajtu
        if counter % 3 == 0:
            buffer0 = (byte & 0b11111100) >> 2
            buffer1 = (byte & 0b00000011) << 4
            
            result += lookup[buffer0]
            
            # Jeżeli to był ostatni bajt w buforze wejściowym to wstawiamy wypełniacze
            if counter == length:
                result += lookup[buffer1]
                result += "=="
                print(f"return at counter = {counter}")
                return result
            
        # Przetwarzanie drugiego bajtu
        elif counter % 3 == 1:
            buffer1 |= (byte & 0b11110000) >> 4
            buffer2  = (byte & 0b00001111) << 2
            
            result += lookup[buffer1]
            
            # Jeżeli to był ostatni bajt w buforze wejściowym
            if counter == length:
                result += lookup[buffer2]
                result += "="
                print(f"return at counter = {counter}")
                return result
        
        # Przetwarzanie trzeciego bajtu
        else:
            buffer2 |= (byte & 0b11000000) >> 6
            buffer3  = (byte & 0b00111111) << 0
            
            result += lookup[buffer2]
            result += lookup[buffer3]
            
            if counter == length:
                print(f"return at counter = {counter}")
                return result
        
        counter += 1
    
    return ""

if __name__ == "__main__":
    import measure_time
    import mem_used
    decoded = b"\x00"
#     data_in = b"\xFF"
#     data_in = b"\x00\x00"
#     data_in = b"\x00\x00\x00"
#     data_in = b"\x00\x00\xFF"
#     data_in = b"\x00\x11\x22\x33\x44\x55\x66\x77\x88\x99\xAA\xBB\xCC\xDD\xEE\xFF"
#     data_in = "\x00\x11\x22\x33\x44\x55\x66\x77\x88\x99\xAA\xBB\xCC\xDD\xEE\xFF"
    data_in  = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
    
    measure_time.begin()
    data_out = bytes_to_base64(data_in)
    measure_time.end("")

    print(f"{data_in} -> {data_out}")
    mem_used.print_ram_used()
