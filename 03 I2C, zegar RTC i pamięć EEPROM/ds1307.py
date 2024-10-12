import time
from machine import Pin, I2C

i2c = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
ds1307_address = 0x68

def read():
    buffer = bytearray(b'\x00')
    
    try:
        i2c.writeto(ds1307_address, buffer)
        buffer = i2c.readfrom(ds1307_address, 7)
    except:
        print("DS1307 communication error")
        return None
    
#     for byte in buffer:
#         print(f"{byte:02X}", end=" ")
#     print()
    
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
    day     = bcd2bin(buffer[4])
    month   = bcd2bin(buffer[5])
    year    = bcd2bin(buffer[6]) + 2000
    
    print(f"{year}.{month:02}.{day:02} {hours:02}:{minutes:02}:{seconds:02}")
    
    return (year, month, day, hours, minutes, seconds, 0, 0)
        
def write(time_tuple):
    year    = time_tuple[0] - 2000
    month   = time_tuple[1]
    day     = time_tuple[2]
    hours   = time_tuple[3]
    minutes = time_tuple[4]
    seconds = time_tuple[5]
    
    def bin2bcd(value):
        tens = value // 10
        ones = value % 10
        return tens << 4 | ones
    
    buffer = bytearray(8)
    buffer[0] = 0x00
    buffer[1] = bin2bcd(seconds)
    buffer[2] = bin2bcd(minutes)
    buffer[3] = bin2bcd(hours)
    buffer[4] = 0
    buffer[5] = bin2bcd(day)
    buffer[6] = bin2bcd(month)
    buffer[7] = bin2bcd(year)
    
    i2c.writeto(ds1307_address, buffer)

# def read2():
#     buffer = i2c.readfrom_mem(ds1307_address, 0x00, 7)
#     
#     for byte in buffer:
#         print(f"{byte:02X} ", end="")
        
# def write_mem():
#     buffer = bytearray([0x00, 0x34, 0x12, 0x00, 0x27, 0x04, 0x24])
#     i2c.writeto_mem(ds1307_address, 0x00, buffer)

def copy_time_from_rtc_to_system():
    print("copy_time_from_rtc_to_system()")
    rtc_time = read();
    if rtc_time != None:
        print(f"settime to {rtc_time}")
        
        from machine import RTC
        RTC().datetime(rtc_time)
        
        print(f"time.localtime() = {time.localtime()}")
    else:
        print("Can't set system time from DS1307")

#read()

# import time
# aaa = time.localtime()
# write(aaa)

#read2()