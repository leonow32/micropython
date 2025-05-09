# MicroPython 1.24.1 ESP32-S3 Octal SPIRAM
# v1.0.1 2025.03.13

import time
from machine import Pin, I2C, RTC

_DS1307_ADDRESS = const(0x68)

class DS1307():
    """
    Create an object to support DS1307 real time clock.
    - i2c: instance of I2C object, max clock speed is 100 kHz!
    """
    
    def __init__(self, i2c):
        self.i2c = i2c
    
    def read(self):
        """
        Read time from the clock and return it as a time tuple
        """
        
        buffer = self.i2c.readfrom_mem(_DS1307_ADDRESS, 0x00, 7)
        
        if buffer[0] & 0b10000000:
            print("Clock not set")
            raise OSError(errno.ENODATA, "Clock not set") 
        
        def bcd2bin(value):
            tens = (value & 0xF0) >> 4
            ones = (value & 0x0F)
            return tens * 10 + ones
        
        s = bcd2bin(buffer[0])
        m = bcd2bin(buffer[1])
        h = bcd2bin(buffer[2])
        w = buffer[3] - 1
        D = bcd2bin(buffer[4])
        M = bcd2bin(buffer[5])
        Y = bcd2bin(buffer[6]) + 2000
        return (Y, M, D, h, m, s, w, 0)
    
    def write(self, time_tuple):
        """
        Write time to the clock
        """
        
        def bin2bcd(value):
            tens = value // 10
            ones = value % 10
            return tens << 4 | ones
        
        buffer = bytes([
            bin2bcd(time_tuple[5]),         # Seconds
            bin2bcd(time_tuple[4]),         # Minutes
            bin2bcd(time_tuple[3]),         # Hours
            time_tuple[6] + 1,              # Day of week (1..7)
            bin2bcd(time_tuple[2]),         # Day
            bin2bcd(time_tuple[1]),         # Month
            bin2bcd(time_tuple[0] - 2000),  # Year (00..99)
        ])
        
        self.i2c.writeto_mem(_DS1307_ADDRESS, 0x00, buffer)
       
    def print(self):
        """
        Read the time and print it to the console.
        """
        
        try:
            Y, M, D, h, m, s, _, _ = self.read()
            print(f"{Y}.{M:02}.{D:02} {h:02}:{m:02}:{s:02}")
        except:
            print("Time not set")
         
    def dump(self):
        """
        Read and print all contents of the memory. Useful for debug.
        """
        
        buffer = self.i2c.readfrom_mem(_DS1307_ADDRESS, 0x00, 64)
        
        print("     0  1  2  3  4  5  6  7  8  9  A  B  C  D  E  F")
        for i in range(64):
            if i % 16 == 0:
                print(f"{i:02X}: ", end = "")
            print(f"{buffer[i]:02X}", end="\n" if i % 16 == 15 else " ")

    def copy_time_to_system(self):
        """
        Read time from the clock and copy it to system.
        """
        
        Y, M, D, h, m, s, _, _ = self.read()
        new_time_tuple = (Y, M, D, 0, h, m, s, 0)
        RTC().datetime(new_time_tuple)

if __name__ == "__main__":
    import mem_used
    
    i2c = I2C(0, freq=100000) # use default pinout and clock frequency
    print(i2c)   # print pinout and clock frequency
    
    rtc = DS1307(i2c)
    
    rtc.dump()

#   new_time = time.localtime()
#   new_time = (2030, 04, 27, 12, 05, 00, 0, 0)
#   new_time = (2025, 12, 24, 12, 34, 56, 0, 0) 
#   rtc.write(new_time)
    
    rtc.read()
    rtc.copy_time_to_system()
    
    mem_used.print_ram_used()
