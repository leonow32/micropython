# MicroPython 1.24.1 ESP32-S3 Octal SPIRAM
# v1.0.1 2025.04.26

import time

TIMEOUT_MS = const(10)

class Mem24:
    """
    Create an object to support EEPROM memories, such as AT24C32.
    - i2c: instance of I2C object
    - device_address: address of the memory chip on I2C bus
    - memory_size: size of the memory chip in bytes
    - page_size: size of the page in bytes
    - addr_size: how many bits are used to point the address, usually 8, 16, 24.
    """
    
    def __init__(self, i2c, device_address, memory_size, page_size, addr_size=16):
        self.i2c = i2c
        self.device_address = device_address
        self.memory_size = memory_size
        self.page_size = page_size
        self.addr_size = addr_size
        
    def __str__(self):
        return f"Mem24({str(self.i2c)}, device_address=0x{self.device_address:02X}," \
        f"memory_size={self.memory_size}, page_size={self.page_size}, addr_size={self.addr_size})"      
    
    def wait_for_ready(self):
        """
        Check in a loop if the memory will respond to an address call on the I2C bus.
        The memory does not respond if a write is in progress. This function may throw
        ETIMEDOUT exception if memory does not acknowledge in requirewd time, specified
        by TIMEOUT.
        """
        
        timeout = TIMEOUT_MS
        while timeout:
            try:
                self.i2c.readfrom(self.device_address, 1)
                return
            except:
                time.sleep_ms(1)
                timeout -= 1
        
        raise OSError(errno.ETIMEDOUT, "I2C polling too many times without ACK")
    
    def read(self, memory_address, length):
        """
        Read data from the memory.
        Return: bytes
        """
        self.wait_for_ready()
        return self.i2c.readfrom_mem(self.device_address, memory_address, length, addrsize=self.addr_size)
    
    def read_into(self, memory_address, buffer):
        """
        Read as many bytes from memory as the length of `buffer`.
        The result is written to `buffer` without allocating new memory space.
        """
        self.wait_for_ready()
        self.i2c.readfrom_mem_into(self.device_address, memory_address, buffer, addrsize=self.addr_size)
    
    def write_page(self, memory_address, data):
        """
        Write data into a single page in the memory.
        """
        self.wait_for_ready()
        self.i2c.writeto_mem(self.device_address, memory_address, data, addrsize=self.addr_size)
    
    def write(self, memory_address, data):
        """
        Write data into a single or multiple pages in the memory.
        """
        address_end         = memory_address + len(data) - 1
        page_start_num      = memory_address // self.page_size
        page_end_num        = address_end // self.page_size
        page_actual_num     = page_start_num
        page_actual_adr_end = None
        actual_start        = memory_address
        actual_end          = None
        actual_length       = None
        bytes_sent          = 0
        
        while page_actual_num <= page_end_num:
            page_actual_adr_end = self.page_size * (page_actual_num + 1) - 1
            actual_end = address_end if address_end <= page_actual_adr_end else page_actual_adr_end
            actual_length = actual_end - actual_start + 1
            self.wait_for_ready()
            self.write_page(actual_start, data[bytes_sent:bytes_sent+actual_length])
            bytes_sent += actual_length
            page_actual_num += 1
            actual_start = actual_end + 1
    
    def erase_chip(self):
        """
        Erase the whole memory and set all bytes to 0xFF.
        """
        buffer = bytes(self.page_size * [0xFF])
        memory_address = 0
        
        while memory_address < self.memory_size:
            self.wait_for_ready()
            self.write_page(memory_address, buffer)
            memory_address += self.page_size
    
    def dump(self):
        """
        Read and print all contents of the memory. Useful for debug.
        """
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
    import mem_used
    import machine
    import time
           
    def print_hex(buffer):
        for byte in buffer:
            print(f"{byte:02X} ", end="")
        print()
    
    start_time = time.ticks_us()
    
    i2c = machine.I2C(0) # use default pinout and clock frequency
    print(i2c)   # print pinout and clock frequency
    eeprom = Mem24(i2c, device_address=0x50, memory_size=4096, page_size=32, addr_size=16)   # AT24C32
#   eeprom = Mem24(i2c, device_address=0x50, memory_size=65536, page_size=128, addr_size=16) # AT24C512
    print(eeprom)
    
#   buffer = eeprom.read(0x0000, 64)
#   print_hex(buffer)
#     
#   buffer = bytearray(16)
#   eeprom.read_into(0x0010, buffer)
#   print_hex(buffer)
    
#   eeprom.write(0x0F10, b'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefABCDEFGHIJKLMNOPQRSTUVWXYZabcdefABCDEFGHIJKLMNOPQRSTUVWXYZabcdef')

#   eeprom.erase_chip()
    
    print(f"Time: {(time.ticks_us() - start_time) / 1000} ms")
    
    eeprom.dump()
    
    mem_used.print_ram_used()
