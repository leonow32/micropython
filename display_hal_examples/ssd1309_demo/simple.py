# MicroPython 1.27.0 ESP32 Pico

from machine import I2C
from display_hal.display_hal import *
from display_hal.driver.ssd1309 import *

import mem_used
import measure_time

i2c     = I2C(0) # use default pinout and clock frequency
display = SSD1309(i2c, rotate=False, address=0x3C)
dihal   = DisplayHAL(display)
print(dihal)

measure_time.begin()
dihal.rect(0, 0, 128, 64, 1)
dihal.text('abcdefghijklm', 1, 2, 1)
dihal.text('nopqrstuvwxyz', 1, 10, 1)
measure_time.end("Rendering time")

measure_time.begin()
dihal.refresh()
measure_time.end("Refreshing time")

display.simulate()

mem_used.print_ram_used()
