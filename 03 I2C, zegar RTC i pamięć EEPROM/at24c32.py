import time
from machine import Pin, I2C, RTC

device_address = 0x50
memory_size = 4096
page_size = 32
i2c = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)

def read(memory_address, length):
    return i2c.readfrom_mem(device_address, memory_address, length, addrsize=16)

def write(memory_address, data):
    i2c.writeto_mem(device_address, memory_address, data, addrsize=16)

def dump():
    buffer = bytearray(16)
    memory_address = 0
    print("       0  1  2  3  4  5  6  7  8  9  A  B  C  D  E  F")
    
    while memory_address < memory_size:
        i2c.readfrom_mem_into(device_address, memory_address, buffer, addrsize=16)
        print(f"{memory_address:04X}: ", end = "")
        for byte in buffer:
            print(f"{byte:02X} ", end="")
        print()
        memory_address += 16
        
if __name__ == "__main__":
    dump()
    
    import gc
    total_ram = gc.mem_alloc() + gc.mem_free()
    used_ram  = gc.mem_alloc()
    print(f'RAM: {used_ram} / {total_ram}')