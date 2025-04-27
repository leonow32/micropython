# MicroPython 1.24.1 ESP32-S3 Octal SPIRAM

from machine import Pin, I2C
import drive24
import mem24
import os
import time

# Zapisywanie testowych plików
def drive_test(path, bytes_in_file):

    # Create dummy content to store in files
    content_to_write = bytearray(bytes_in_file * b"x")

    # Save as many files as possible
    print("===== MULTIPLE SAVES =====")
    time_start = time.ticks_ms()
    i = 0
    while True:
        name = f"{path}/{i}.txt"
        print(f"Writing {name}")
        try:
            with open(name, "wb") as f:
                f.write(content_to_write)
            i += 1
        except:
            print(f"Error at {i}")
            break
    print(f"Time: {time.ticks_ms()-time_start} ms")
            
    # Try to read all saved files   
    print("===== MULTIPLE READS =====")
    time_start = time.ticks_ms()
    files = i
    for i in range(0, files):
        name = f"{path}/{i}.txt"
        print(f"Reading {name}")
        try:
            with open(name, "rb") as f:
                content = f.read()
                #print(f"File {name} = {content}")
        except:
            print(f"File {name} = error")
    print(f"Time: {time.ticks_ms()-time_start} ms")

i2c    = I2C(0)
eeprom = mem24.Mem24(i2c, device_address=0x50, memory_size=4096, page_size=32, addr_size=16)
# eeprom = mem24.Mem24(i2c, device_address=0x50, memory_size=65536, page_size=128, addr_size=16)
drive  = drive24.Drive(eeprom, "/eeprom")

drive_test("/eeprom", 100)

