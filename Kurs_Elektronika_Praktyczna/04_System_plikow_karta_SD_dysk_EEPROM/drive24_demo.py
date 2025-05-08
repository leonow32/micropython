from machine import Pin, I2C
import drive24
import mem24

i2c    = I2C(0)
# eeprom = mem24.Mem24(i2c, device_address=0x50, memory_size=4096, page_size=32, addr_size=16)
eeprom = mem24.Mem24(i2c, device_address=0x50, memory_size=65536, page_size=128, addr_size=16)
drive  = drive24.Drive(eeprom, "/eeprom")

try:
    with open("eeprom/test.txt") as file:
        counter = int(file.read())
except:
    counter = 0
    
with open("eeprom/test.txt", "w") as file:
    counter += 1
    file.write(str(counter))
    print(counter)
