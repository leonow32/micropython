# MicroPython 1.24.1 ESP32-S3 Octal SPIRAM
# v1.0.0 2025.03.17

import time
from machine import Pin, I2C, RTC

_DS3231_ADDRESS = const(0x68)

class DS3231():
    """
    Create an object to support DS3231 real time clock.
    Does not support alarms and configuration.
    - i2c: instance of I2C object, max clock speed is 400 kHz.
    """
    
    def __init__(self, i2c):
        self.i2c = i2c
    
    def read(self):
        """
        Read time from the clock and return it as a time tuple
        """
        
        buffer = self.i2c.readfrom_mem(_DS3231_ADDRESS, 0x00, 7)
        
        def bcd2bin(value):
            tens = (value & 0xF0) >> 4
            ones = (value & 0x0F)
            return tens * 10 + ones
        
        s = bcd2bin(buffer[0])
        m = bcd2bin(buffer[1])
        h = bcd2bin(buffer[2])
        w = buffer[3] - 1
        D = bcd2bin(buffer[4])
        M = bcd2bin(buffer[5] & 0b00011111)
        Y = bcd2bin(buffer[6]) + 2000
        return (Y, M, D, h, m, s, w, 0)
    
    def read_temperature(self):
        """
        Returns float. Temperature resolution is 0.25'C.
        """
        
        buffer = self.i2c.readfrom_mem(_DS3231_ADDRESS, 0x11, 2)
        value = ((buffer[0] & 0b01111111) << 2) | ((buffer[1] & 0b11000000) >> 6)
        if value & (1 << 11): value = -2**11 + (value & (2**11 - 1))
        return value / 4
    
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
        
        self.i2c.writeto_mem(_DS3231_ADDRESS, 0x00, buffer)
       
    def print(self):
        """
        Read the time and print it to the console.
        """
        
        Y, M, D, h, m, s, _, _ = self.read()
        print(f"{Y}.{M:02}.{D:02} {h:02}:{m:02}:{s:02}")
         
    def dump(self):
        """
        Read and print all contents of the memory. Useful for debug.
        """
        
        buffer = self.i2c.readfrom_mem(_DS3231_ADDRESS, 0x00, 0x13)
        
        print("Address: ", end="")
        for i in range(0x13): print(f"{i:02X} ", end = "")
        print("\nValue:   ", end="")
        for i in range(0x13): print(f"{buffer[i]:02X} ", end="")
        print()

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
    print(i2c)                # print pinout and clock frequency
    
    rtc = DS3231(i2c)
    
#   rtc.dump()

#   new_time = time.localtime()
#   new_time = (2030, 04, 27, 12, 05, 00, 0, 0)
#   new_time = (2025, 12, 24, 12, 34, 56, 0, 0) 
#   rtc.write(new_time)
    
    rtc.print()
#   rtc.copy_time_to_system()

    print(rtc.read_temperature())
    
    mem_used.print_ram_used()

