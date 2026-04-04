# MicroPython 1.24.1 ESP32-S3 Octal SPIRAM

from machine import I2C
from display_hal.display_hal import *
from display_hal.driver.ssd1309 import *
from display_hal.font.console7 import *
from display_hal.font.dos8 import *
from display_hal.font.galaxy16_digits import *
from display_hal.font.mini8 import *
from display_hal.font.extronic16_unicode import *
from display_hal.font.extronic16B_unicode import *

import mem_used
import measure_time

i2c     = I2C(0) # use default pinout and clock frequency
display = SSD1309(i2c, rotate=False, address=0x3C)
dihal   = DisplayHAL(display)
print(dihal)

measure_time.begin()
# dihal.text(console7,            "Benchmark SSD1309", 0, 0, "C")
# dihal.text(mini8,               "abcdefghijklmnopqrstuvwxyz01234", 0, 8, "C")
# dihal.text(extronic16_unicode,  "ąęłćśńóźż", 0, 16, "L")
# dihal.text(extronic16B_unicode, "ąęłćśńóźż", 0, 16, "R")
# dihal.text(dos8,                "abcdefghijklmnop", 0, 32, "C", 0)
# dihal.text(dos8,                "qrstuvwxyz123345", 0, 40, "C", 0)
# dihal.text(galaxy16_digits,     "0123456789", 0, 49, "C")
measure_time.end("Rendering time")

measure_time.begin()
dihal.refresh()
measure_time.end("Refreshing time")

mem_used.print_ram_used()
