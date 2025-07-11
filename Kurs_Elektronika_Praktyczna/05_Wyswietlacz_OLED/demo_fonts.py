# MicroPython 1.24.1 ESP32-S3 Octal SPIRAM

from machine import Pin, I2C
import framebuf
import mem_used
import ssd1309
import time

from font.dos8 import *
from font.galaxy16_digits import *
from font.mini8 import *
from font.mini8B import *
from font.squared16_unicode import *
from font.squared16B_unicode import *
      
i2c = I2C(0) # use default pinout and clock frequency
print(i2c)   # print pinout and clock frequency 

display = ssd1309.SSD1309(i2c)

start_time = time.ticks_us()
display.print_text(mini8B,             "Font demo SSD1309", 0, 0, "C")
display.print_text(mini8,              "abcdefghijklmnopqrstuvwxyz01234", 0, 8, "C")
display.print_text(squared16_unicode,  "ąęłćśńóźż", 0, 16, "L")
display.print_text(squared16B_unicode, "ąęłćśńóźż", 0, 16, "R")
display.print_text(dos8,               "abcdefghijklmnop", 0, 32, "C")
display.print_text(dos8,               "qrstuvwxyz123345", 0, 40, "C", 0)
display.print_text(galaxy16_digits,    "0123456789", 0, 49, "C")
end_time = time.ticks_us()

display.refresh()

mem_used.print_ram_used()
print(f"Work time: {end_time-start_time} us")





