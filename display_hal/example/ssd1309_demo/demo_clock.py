# MicroPython 1.27.0 ESP32 Pico
from machine import I2C
from display_hal.display_hal import *
from display_hal.driver.ssd1309 import *

from display_hal.font.galaxy16_digits import *
from display_hal.font.galaxy24_digits import *
from display_hal.font.galaxy16_digits import *
from display_hal.font.mini8 import *
from display_hal.font.extronic16_unicode import *
from display_hal.font.extronic16B_unicode import *

import time
import mem_used
import measure_time

i2c     = I2C(0) # use default pinout and clock frequency
display = SSD1309(i2c, rotate=False, address=0x3C)
dihal   = DisplayHAL(display)
print(dihal)

while True:
    time_tuple = time.localtime()
    dihal.fill(0)
    dihal.text(f"{time_tuple[3]}:{time_tuple[4]:02}", 127, 10, 1, galaxy24_digits, "CENTER")
    dihal.text(f"{time_tuple[2]}.{time_tuple[1]:02}.{time_tuple[0]}", 127, 38, 1, galaxy16_digits, "CENTER")
    dihal.refresh()
    mem_used.print_ram_used()
    time.sleep(60)
    #machine.lightsleep(60_000)
