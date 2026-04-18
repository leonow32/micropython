# MicroPython 1.24.1 ESP32-S3 Octal SPIRAM
# MicroPython 1.27.0 ESP32 Pico

from machine import I2C
from display_hal.display_hal import *
from display_hal.driver.ssd1309 import *

import mem_used
import measure_time
import random
import time

LOOPS = const(100)

i2c     = I2C(0) # use default pinout and clock frequency
display = SSD1309(i2c, rotate=False, address=0x3C)
dihal   = DisplayHAL(display)
print(dihal)

x1 = 0
y1 = 0

measure_time.begin()

for i in range(LOOPS):
    x2 = random.randrange(dihal.width)
    y2 = random.randrange(dihal.height)
    dihal.line(x1, y1, x2, y2)
    dihal.refresh()
    x1 = x2
    y1 = y2

measure_time.end("Work time")

mem_used.print_ram_used()
