from machine import Pin, I2C

i2c = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
ds1307_address = 0x68

def read():
    buffer = bytearray(b'\x00')
    i2c.writeto(ds1307_address, buffer)
    buffer = i2c.readfrom(ds1307_address, 7)
    
    for byte in buffer:
        print(f"{byte:02X} ", end="")
        
def read2():
    buffer = i2c.readfrom_mem(ds1307_address, 0x00, 7)
    
    for byte in buffer:
        print(f"{byte:02X} ", end="")
        
def write_mem():
    buffer = bytearray([0x00, 0x34, 0x12, 0x00, 0x27, 0x04, 0x24])
    i2c.writeto_mem(ds1307_address, 0x00, buffer)

write_mem()
#read2()