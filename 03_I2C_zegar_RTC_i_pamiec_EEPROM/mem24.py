# MicroPython 1.24.1 ESP32-S3 Octal SPIRAM
# v1.0.0 250310

import time
from machine import Pin, I2C

import mem_used

TIMEOUT = const(20)   # Timeout value = TIMEOUT * 100us

class Mem24():
    
    def __init__(self, i2c, device_address, memory_size, page_size, addr_size=16):
        self.i2c = i2c
        self.device_address = device_address
        self.memory_size = memory_size
        self.page_size = page_size
        self.addr_size = addr_size
    
    def wait_for_ready(self):
        timeout = TIMEOUT
        while timeout:
            try:
                self.i2c.readfrom(self.device_address, 1)
                return
            except:
#                 print(".", end="")
                time.sleep_us(100)
                timeout -= 1
        
        raise OSError(errno.ETIMEDOUT, "I2C polling too many times without ACK")
    
    def read(self, memory_address, length):
        self.wait_for_ready()
        return self.i2c.readfrom_mem(self.device_address, memory_address, length, addrsize=self.addr_size)
    
    def read_into(self, memory_address, buffer):
        self.wait_for_ready()
        self.i2c.readfrom_mem_into(self.device_address, memory_address, buffer, addrsize=self.addr_size)
    
    def write_page(self, memory_address, data):
        self.wait_for_ready()
        self.i2c.writeto_mem(self.device_address, memory_address, data, addrsize=16)
    
    def write_new(self, memory_address, data):
        address_end         = memory_address + len(data) - 1    # Adres ostatniego bajtu do zapisania
        page_start_num      = memory_address // self.page_size  # Numer pierwszej strony do zapisania
        page_end_num        = address_end // self.page_size     # Numer ostatniej strony do zapisania
        page_actual_num     = page_start_num                    # Numer aktualnie zapisywanej strony
        page_actual_adr_end = None                              # Adres ostatniego bajtu w obrębie aktualnie zapisywanej strony
        actual_start        = memory_address                    # Adres pierwszego bajtu do zapisania w bieżącej transakcji
        actual_end          = None                              # Adres ostatniego bajtu do zapisania w bieżącej transakcji
        actual_length       = None                              # Liczba bajtów do zapisania w bieżącej transakcji
        bytes_sent          = 0
#         print(f"len(data): {len(data)}")
#         print(f"Pages:     {page_start_num}...{page_end_num}")
#         print(f"Address:   {memory_address:04X}...{address_end:04X}")
        
        while page_actual_num <= page_end_num:
            
#             print(f"----------")
#             print(f"page_actual_num = {page_actual_num}")
            
            # Ustal adres ostatniego bajtu w obrębie bieżącej strony
            page_actual_adr_end = self.page_size * (page_actual_num + 1) - 1
            
            # Jeżeli adres ostatniego bajtu do zapisania jest mniejszy niż adres ostatniego bajtu strony
            # tzn. jeżeli koniec zapisu leży w obrębie strony
            if address_end <= page_actual_adr_end:
                actual_end = address_end
            else:
                actual_end = page_actual_adr_end
                
            actual_length = actual_end - actual_start + 1
            
#             print(f"adresy: {actual_start:04X}...{actual_end:04X}, lenght: {actual_length}, data: {data[bytes_sent:bytes_sent+actual_length]}")
            
            self.wait_for_ready()
            self.i2c.writeto_mem(self.device_address, actual_start, data[bytes_sent:bytes_sent+actual_length], addrsize=16)
            
            bytes_sent += actual_length
            page_actual_num += 1
            actual_start = actual_end + 1
    
    def erase_chip(self):
        buffer = bytes(self.page_size * [0xFF])
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
            self.read_into(memory_address, buffer)
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
    
#   mem.dump()
    
    
    # zapis w obrębie kilku strony
    mem.write_new(0x0F10, b'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefABCDEFGHIJKLMNOPQRSTUVWXYZabcdefABCDEFGHIJKLMNOPQRSTUVWXYZabcdef')
    
    mem_used.print_ram_used()