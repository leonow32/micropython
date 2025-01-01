from machine import Pin, I2C
from font.dos16 import *
from font.galaxy16_digits import *
from font.galaxy24_digits import *
from font.sans16_unicode import *
from font.sans16B_unicode import *
import framebuf
import ssd1309
import mem_used
import time       

i2c = I2C(0, scl=Pin(1), sda=Pin(2), freq=400000)
display = ssd1309.SSD1309(i2c)
start_time = time.ticks_us()

#print_char(display, dos16["F"], 0, 0)
#print_char(display, dos16["j"], 8, 0)
#print_text(display, dos16, "Test DOS 16x8", 0, 0)

# used_font = sans16_unicode
# # used_font = sans16B_unicode
# print_text(display, used_font, "ABCDEFGHIJKLMNOPQRSTUVWXYZ", 0, 0)
# print_text(display, used_font, "abcdefghijklmnopqrstuvwxyz", 0, 16)
# print_text(display, used_font, "ĄĘĆŚŃŁÓŹŻ ąęćśńłóźż", 0, 32)
# print_text(display, used_font, "0123456789", 0, 48)

display.pixel(64, 0, 1)
display.print_text(galaxy24_digits, "23:59", 127, 2, "r")
display.print_text(galaxy16_digits, "12.05.2025", 127, 27, "R")

display.refresh()
#display.simulate()

end_time = time.ticks_us()
print(f"Work time: {end_time-start_time} us")
mem_used.print_ram_used()
