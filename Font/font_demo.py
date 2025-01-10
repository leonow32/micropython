from machine import Pin, I2C
from font.dos16 import *
from font.galaxy16_digits import *
from font.galaxy24_digits import *
import framebuf
import ssd1309
import mem_used
import time       

i2c = I2C(0, scl=Pin(1), sda=Pin(2), freq=400000)
display = ssd1309.SSD1309(i2c)
start_time = time.ticks_us()

display.print_text(galaxy24_digits, "23:59", 127, 10, "C")
display.print_text(galaxy16_digits, "12.05.2025", 127, 38, "C")
display.refresh()

end_time = time.ticks_us()
print(f"Work time: {end_time-start_time} us")
mem_used.print_ram_used()
