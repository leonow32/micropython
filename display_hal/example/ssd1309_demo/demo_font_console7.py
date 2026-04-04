# MicroPython 1.24.1 ESP32-S3 Octal SPIRAM
# MicroPython 1.27.0 ESP32 Pico

from machine import I2C
from display_hal.display_hal import *
from display_hal.driver.ssd1309 import *

from display_hal.font.console7 import *

import mem_used
import measure_time   

i2c     = I2C(0) # use default pinout and clock frequency
display = SSD1309(i2c, rotate=False, address=0x3C)
dihal   = DisplayHAL(display)
print(dihal)

measure_time.begin()
dihal.text("ABCDEFGHIJKLM",         0,  0, 1, console7, "CENTER")
dihal.text("NOPQRSTUVWXYZ",         0,  8, 1, console7, "CENTER")
dihal.text("abcdefghijkl",          0, 16, 1, console7, "CENTER")
dihal.text("mnopqrstuvwxyz",        0, 24, 1, console7, "CENTER")
dihal.text("0123456789",            0, 32, 1, console7, "CENTER")
dihal.text("+-*/=()[]{}<>",         0, 40, 1, console7, "CENTER")
dihal.text("`~!@#$%^&*.,:;'|\/_\"", 0, 48, 1, console7, "CENTER")
measure_time.end("Rendering time")

measure_time.begin()
dihal.refresh()
measure_time.end("Refreshing time")

mem_used.print_ram_used()
