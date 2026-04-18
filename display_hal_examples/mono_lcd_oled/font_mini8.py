# MicroPython 1.24.1 ESP32-S3 Octal SPIRAM
# MicroPython 1.27.0 ESP32 Pico

import mem_used
import measure_time

from display_hal.display_hal import *
from display_hal.font.mini8 import *

# Display OLED 128x64 monochrome with SSD1309
from machine import I2C
from display_hal.driver.ssd1309 import *
i2c     = I2C(0) # use default pinout and clock frequency
display = SSD1309(i2c, rotate=False, address=0x3C)
dihal   = DisplayHAL(display)
print(dihal)

measure_time.begin()
dihal.text("ABCDEFGHIJKLM",              0,  0, mini8, ALIGN_CENTER)
dihal.text("NOPQRSTUVWXYZ",              0, 14, mini8, ALIGN_CENTER)
dihal.text("abcdefghijklmnopqrstuvwxyz", 0, 28, mini8, ALIGN_CENTER)
dihal.text("0123456789+-*/=()[]{}<>",    0, 42, mini8, ALIGN_CENTER)
dihal.text("`~!@#$%^&*.,:;'|\/_\"",      0, 56, mini8, ALIGN_CENTER)
measure_time.end("Rendering time")

measure_time.begin()
dihal.refresh()
measure_time.end("Refreshing time")

mem_used.print_ram_used()
