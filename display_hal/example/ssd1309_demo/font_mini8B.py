# MicroPython 1.24.1 ESP32-S3 Octal SPIRAM
# MicroPython 1.27.0 ESP32 Pico

from machine import I2C
from display_hal.display_hal import *
from display_hal.driver.ssd1309 import *

from display_hal.font.mini8B import *

import mem_used
import measure_time   

i2c     = I2C(0) # use default pinout and clock frequency
display = SSD1309(i2c, rotate=False, address=0x3C)
dihal   = DisplayHAL(display)
print(dihal)

measure_time.begin()
dihal.text("ABCDEFGHIJKLMN",       0,  0, 1, mini8B, "CENTER")
dihal.text("OPQRSTUVWXYZ",         0,  9, 1, mini8B, "CENTER")
dihal.text("abcdefghijklmn",       0, 18, 1, mini8B, "CENTER")
dihal.text("opqrstuvwxyz",         0, 27, 1, mini8B, "CENTER")
dihal.text("0123456789+-*/=",      0, 36, 1, mini8B, "CENTER")
dihal.text("`~!@#$%^&*.,:;'|\_\"", 0, 45, 1, mini8B, "CENTER")
dihal.text("()[]{}<>",             0, 54, 1, mini8B, "CENTER")
measure_time.end("Rendering time")

measure_time.begin()
dihal.refresh()
measure_time.end("Refreshing time")

mem_used.print_ram_used()
