# MicroPython 1.24.1 ESP32-S3 Octal SPIRAM

from machine import Pin, I2C

_PAGE_SIZE      = const(32)
_MEMORY_SIZE    = const(4096)
_DEVICE_ADDRESS = const(0x50)

i2c = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)

def wait_for_ready():
    while True:
        try:
            print(".", end="")
            i2c.readfrom(_DEVICE_ADDRESS, 1)
            break;
        except:
            pass

def read(memory_address, length):
    wait_for_ready()
    return i2c.readfrom_mem(_DEVICE_ADDRESS, memory_address, length, addrsize=16)

def write(memory_address, data):
    wait_for_ready()
    i2c.writeto_mem(_DEVICE_ADDRESS, memory_address, data, addrsize=16)

def dump():
    buffer = bytearray(16)
    memory_address = 0
    print("       0  1  2  3  4  5  6  7  8  9  A  B  C  D  E  F")
    
    while memory_address < _MEMORY_SIZE:
        i2c.readfrom_mem_into(_DEVICE_ADDRESS, memory_address, buffer, addrsize=16)
        print(f"{memory_address:04X}: ", end = "")
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
    #write(0x0010, b"0123")
    #write(0x0020, b"ABCD")
    dump()
