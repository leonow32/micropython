from machine import Pin, I2C

class Mem24():
    
    def __init__(self, i2c, device_address, memory_size, page_size, addr_size=16):
        self.i2c = i2c
        self.device_address = device_address
        self.memory_size = memory_size
        self.page_size = page_size
        self.addr_size = addr_size
    
    def wait_for_ready(self):
        while True:
            try:
                print(".", end="")
                self.i2c.readfrom(self.device_address, 1)
                break
            except:
                pass
    
    def read(self, memory_address, length):
        self.wait_for_ready()
        return self.i2c.readfrom_mem(self.device_address, memory_address, length, addrsize=self.addr_size)
    
    def write(self, memory_address, data):
        self.wait_for_ready()
        self.i2c.writeto_mem(self.device_address, memory_address, data, addrsize=16)
    
    def write_new(self, memory_address, data):
#         bytes_left = len(data)
#         page_first = memory_address // self.page_size
#         page_last  = (memory_address + bytes_left) // self.page_size
#         print(f"len(data)  = {len(data)}")
#         print(f"page_first = {page_first}")
#         print(f"page_last  = {page_last}")

        
        
        address_end = memory_address + len(data) - 1
        print(f"memory_address = {memory_address:04X}")
        
        page_actual = memory_address // self.page_size
        print(f"page_actual = {page_actual}")
        
        page_end = address_end // self.page_size
        print(f"page_end = {page_end}")
        
        data_begin = 0
        
        while page_actual <= page_end:

            # Znajdź adres końca bieżącej strony
            last_address_in_page = (1 + page_actual) * self.page_size - 1
            print(f"last_address_in_page = {last_address_in_page:04X}")
            
            
        
        return
        
        
        while True:
            
            
            
#             if memory_address + bytes_to_write - 1 >= last_address_in_page:
#                 end = last_address_in_page - memory_address
#             else:
#                 end = 
            
            # Ile bajtów jest między aktualnym adresem a końcem strony
            margin = last_address_in_page - memory_address + 1
            print(f"margin = {margin}")
            
            
            
            
            
            bytes_written = 0;
            
            self.wait_for_ready()
            i2c.writeto_mem(self.device_address, memory_address, data[begin:end], addrsize=self.addr_size)
            
#             if memory_address + len(data) - 1 <= last_address_in_page:
#                 bytes_to_write = 
            
            
#             if memory_address + len(data) - 1 <= last_address_in_page:
#                 self.wait_for_ready()
#                 i2c.writeto_mem(self.device_address, memory_address, data, addrsize=self.addr_size)
#                 break;
#             else:
#                 print("x")
#                 break
            
            if bytes_written == len(data):
                print("Done")
                break
        
        
        
        
        
        
    def erase_chip(self):
        buffer = bytes(self.page_size * [0x00])
        memory_address = 0
        
        while memory_address < self.memory_size:
            self.wait_for_ready()
            self.write(memory_address, buffer)
            memory_address += self.page_size
    
    def dump(self):
        buffer = bytearray(16)
        memory_address = 0
        print("           0  1  2  3  4  5  6  7  8  9  A  B  C  D  E  F")
        
        while memory_address < self.memory_size:
            self.i2c.readfrom_mem_into(self.device_address, memory_address, buffer, addrsize=self.addr_size)
            print(f"{memory_address:08X}: ", end = "")
            for byte in buffer:
                print(f"{byte:02X} ", end="")
            for byte in buffer:
                if byte >= 32 and byte <= 127:
                    print(chr(byte), end="")
                else:
                    print(" ", end="")
            print()
            memory_address += 16
    
if __name__ == "__main__":
    i2c = I2C(0, scl=Pin(1), sda=Pin(2), freq=400000)
    mem = Mem24(i2c, device_address=0x50, memory_size=4096, page_size=32, addr_size=16)
    
    mem.dump()