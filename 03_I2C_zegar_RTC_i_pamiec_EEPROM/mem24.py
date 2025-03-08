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
#               print(".", end="")
                self.i2c.readfrom(self.device_address, 1)
                break
            except:
                pass
    
    def read(self, memory_address, length):
        self.wait_for_ready()
        return self.i2c.readfrom_mem(self.device_address, memory_address, length, addrsize=self.addr_size)
    
    def write(self, memory_address, data):
        self.wait_for_ready()
        i2c.writeto_mem(self.device_address, memory_address, data, addrsize=self.addr_size)
        
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
        print("       0  1  2  3  4  5  6  7  8  9  A  B  C  D  E  F")
        
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