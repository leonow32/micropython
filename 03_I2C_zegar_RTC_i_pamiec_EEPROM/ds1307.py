# MicroPython 1.24.1 ESP32-S3 Octal SPIRAM

import time
import mem_used
import measure_time
from machine import Pin, I2C, RTC

ds1307_address = 0x68
i2c = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)

def dump():
    measure_time.begin()
    buffer = bytearray(b'\x00')
    
    try:
        i2c.writeto(ds1307_address, buffer)
        buffer = i2c.readfrom(ds1307_address, 64)
    except:
        print("DS1307 communication error")
        return None
    
    measure_time.end("dump")
    
    print("     0  1  2  3  4  5  6  7  8  9  A  B  C  D  E  F")
    for i in range(64):
        if i % 16 == 0:
            print(f"{i:02X}: ", end = "")
        print(f"{buffer[i]:02X}", end="\n" if i % 16 == 15 else " ")

def read():
    buffer = bytearray(b'\x00')
    
    try:
        i2c.writeto(ds1307_address, buffer)
        buffer = i2c.readfrom(ds1307_address, 7)
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
    year    = time_tuple[0] - 2000
    month   = time_tuple[1]
    day     = time_tuple[2]
    hours   = time_tuple[3]
    minutes = time_tuple[4]
    seconds = time_tuple[5]
    weekday = time_tuple[6] + 1
    
    def bin2bcd(value):
        tens = value // 10
        ones = value % 10
        return tens << 4 | ones
    
    buffer = bytearray(8)
    buffer[0] = 0x00
    buffer[1] = bin2bcd(seconds)
    buffer[2] = bin2bcd(minutes)
    buffer[3] = bin2bcd(hours)
    buffer[4] = weekday
    buffer[5] = bin2bcd(day)
    buffer[6] = bin2bcd(month)
    buffer[7] = bin2bcd(year)
    
    i2c.writeto(ds1307_address, buffer)
        
def write_mem():
    buffer = bytearray(56)
    i2c.writeto_mem(ds1307_address, 0x08, buffer)

def copy_time_from_rtc_to_system():
    print("copy_time_from_rtc_to_system()")
    ds1307_time = read();
    if ds1307_time != None:
        print(f"settime to {ds1307_time}")
        RTC().datetime(ds1307_time)
        print(f"time.localtime() = {time.localtime()}")
    else:
        print("Can't set system time from DS1307")

def print_system_time():
    time_tuple = time.localtime()
    year    = time_tuple[0]
    month   = time_tuple[1]
    day     = time_tuple[2]
    hours   = time_tuple[3]
    minutes = time_tuple[4]
    seconds = time_tuple[5]
    weekday = time_tuple[6]
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    print(f"{year}.{month:02}.{day:02} {hours:02}:{minutes:02}:{seconds:02} {days[weekday]}")

if __name__ == "__main__":
    dump()

    read()
    
    mem_used.print_ram_used()

    # Ustawianie czasu w DS1307 na podstawie czasu systemowego w ESP32
#     import time
#     write(time.localtime())

