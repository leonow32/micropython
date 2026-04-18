# MicroPython 1.24.1 ESP32-S3 Octal SPIRAM
# MicroPython 1.27.0 ESP32 Pico

import mem_used
import measure_time
import random
import time

from display_hal.display_hal import *

# Display OLED 128x64 monochrome with SSD1309
# from machine import I2C
# from display_hal.driver.ssd1309 import *
# i2c     = I2C(0) # use default pinout and clock frequency
# display = SSD1309(i2c, address=0x3C, rotate=False)

# Display OLED 128x64 monochrome with SH1106
from machine import I2C
from display_hal.driver.sh1106 import *
i2c     = I2C(0) # use default pinout and clock frequency
display = SH1106(i2c, address=0x3D, rotate=False, offset_x=2)

dihal   = DisplayHAL(display)
print(dihal)

LOOPS = const(100)
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
