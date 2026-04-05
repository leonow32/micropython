# MicroPython 1.24.1 ESP32-S3 Octal SPIRAM
# MicroPython 1.27.0 ESP32 Pico

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
dihal.text("-= Font Benchmark =-", 0, 0, 1, console7, "CENTER")
dihal.text("abcdefghijklmnopqrstuvwxyz01234", 0, 8, 1, mini8, "CENTER")
dihal.text("ąęłćśńóźż", 0, 16, 1, extronic16_unicode, "LEFT")
dihal.text("ąęłćśńóźż", 0, 16, 1, extronic16B_unicode, "RIGHT")
dihal.text("abcdefghijklmnop", 0, 32, 0, dos8, "CENTER")
dihal.text("qrstuvwxyz123345", 0, 40, 0, dos8, "CENTER")
dihal.text("0123456789", 0, 49, 1, galaxy16_digits, "CENTER")
measure_time.end("Rendering time")

measure_time.begin()
dihal.refresh()
measure_time.end("Refreshing time")

mem_used.print_ram_used()
