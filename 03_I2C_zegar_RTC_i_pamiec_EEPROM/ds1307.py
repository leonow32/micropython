# MicroPython 1.24.1 ESP32-S3 Octal SPIRAM

import time
from machine import Pin, I2C, RTC

_DS1307_ADDRESS = const(0x68)
i2c = I2C(0, scl=Pin(1), sda=Pin(2), freq=90000)

def dump():
    buffer = bytearray(64)
    
    try:
        i2c.writeto(_DS1307_ADDRESS, b'\x00')
        i2c.readfrom_into(_DS1307_ADDRESS, buffer)
    except:
        print("DS1307 communication error")
        return None
    
    print("     0  1  2  3  4  5  6  7  8  9  A  B  C  D  E  F")
    for i in range(64):
        if i % 16 == 0:
            print(f"{i:02X}: ", end = "")
        print(f"{buffer[i]:02X}", end="\n" if i % 16 == 15 else " ")

def read():
    buffer = bytearray(7)
    
    try:
        i2c.writeto(_DS1307_ADDRESS, b'\x00')
        i2c.readfrom_into(_DS1307_ADDRESS, buffer)
    except:
        print("DS1307 communication error")
        return None
    
    if buffer[0] & 0b10000000:
        print("Clock not set")
        return None
    
    def bcd2bin(value):
        tens = (value & 0xF0) >> 4
        ones = (value & 0x0F)
        return tens * 10 + ones
    
    seconds = bcd2bin(buffer[0])
    minutes = bcd2bin(buffer[1])
    hours   = bcd2bin(buffer[2])
    weekday = buffer[3] - 1
    day     = bcd2bin(buffer[4])
    month   = bcd2bin(buffer[5])
    year    = bcd2bin(buffer[6]) + 2000
    
    print(f"{year}.{month:02}.{day:02} {hours:02}:{minutes:02}:{seconds:02}")
    
    return (year, month, day, hours, minutes, seconds, weekday, 0)
        
def write(time_tuple):
    def bin2bcd(value):
        tens = value // 10
        ones = value % 10
        return tens << 4 | ones
    
    buffer = bytes([
        0x00,                           # Address of the first register to be written
        bin2bcd(time_tuple[5]),         # Seconds
        bin2bcd(time_tuple[4]),         # Minutes
        bin2bcd(time_tuple[3]),         # Hours
        time_tuple[6] + 1,              # Day of week (1..7)
        bin2bcd(time_tuple[2]),         # Day
        bin2bcd(time_tuple[1]),         # Month
        bin2bcd(time_tuple[0] - 2000),  # Year (00..99)
    ])
    
    i2c.writeto(_DS1307_ADDRESS, buffer)

def copy_time_from_rtc_to_system():
    Y, M, D, h, m, s, _, _ = read()
    new_time_tuple = (Y, M, D, 0, h, m, s, 0)
    RTC().datetime(new_time_tuple)

if __name__ == "__main__":
#   dump()
#   read()

    new_time = time.localtime()
#   new_time = (2030, 04, 27, 12, 05, 00, 0, 0)
#   new_time = (2025, 12, 24, 12, 34, 56, 0, 0) 
    write(new_time)
    
    read()
