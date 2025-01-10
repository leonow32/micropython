from machine import Pin, I2C
from font.galaxy16_digits import *
from font.galaxy24_digits import *
# from mpy.galaxy16_digits import *
# from mpy.galaxy24_digits import *
import framebuf
import ssd1309
import simulator
import mem_used
import time       

button = Pin(0, Pin.IN, Pin.PULL_UP)
i2c = I2C(0, scl=Pin(1), sda=Pin(2), freq=400000)
try:
    display = ssd1309.SSD1309(i2c)
except:
    display = simulator.SIM()

display.print_text(galaxy16_digits,  "0123456789", 0, -1, "C")
display.print_text(galaxy24_digits,  "01234", 0, 15, "C")
display.print_text(galaxy24_digits, "56789", 0, 40, "C")
display.print_text(galaxy16_digits,  "", 0, 48, "C")
display.refresh()

mem_used.print_ram_used()



