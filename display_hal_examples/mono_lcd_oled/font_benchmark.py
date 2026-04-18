# MicroPython 1.24.1 ESP32-S3 Octal SPIRAM
# MicroPython 1.27.0 ESP32 Pico

import mem_used
import measure_time

from display_hal.display_hal import *
from display_hal.font.console7 import *
from display_hal.font.dos8 import *
from display_hal.font.galaxy16_digits import *
from display_hal.font.mini8 import *
from display_hal.font.extronic16_unicode import *
from display_hal.font.extronic16B_unicode import *

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

measure_time.begin()
dihal.text("-= Font Benchmark =-", 0, 0, console7, ALIGN_CENTER)
dihal.text("abcdefghijklmnopqrstuvwxyz01234", 0, 8, mini8, ALIGN_CENTER)
dihal.text("ąęłćśńóźż", 0, 16, extronic16_unicode, ALIGN_LEFT)
dihal.color_set(0, 1)
dihal.text("ąęłćśńóźż", 0, 16, extronic16B_unicode, ALIGN_RIGHT)
dihal.text("abcdefghijklmnop", 0, 32, dos8, ALIGN_CENTER)
dihal.text("qrstuvwxyz123345", 0, 40, dos8, ALIGN_CENTER)
dihal.color_set(1, 0)
dihal.text("0123456789", 0, 49, galaxy16_digits, ALIGN_CENTER)
measure_time.end("Rendering time")

measure_time.begin()
dihal.refresh()
measure_time.end("Refreshing time")

mem_used.print_ram_used()
