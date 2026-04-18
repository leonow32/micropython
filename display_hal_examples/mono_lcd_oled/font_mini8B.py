# MicroPython 1.24.1 ESP32-S3 Octal SPIRAM
# MicroPython 1.27.0 ESP32 Pico

import mem_used
import measure_time

from display_hal.display_hal import *
from display_hal.font.mini8B import *

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
dihal.text("ABCDEFGHIJKLMN",       0,  0, mini8B, ALIGN_CENTER)
dihal.text("OPQRSTUVWXYZ",         0,  9, mini8B, ALIGN_CENTER)
dihal.text("abcdefghijklmn",       0, 18, mini8B, ALIGN_CENTER)
dihal.text("opqrstuvwxyz",         0, 27, mini8B, ALIGN_CENTER)
dihal.text("0123456789+-*/=",      0, 36, mini8B, ALIGN_CENTER)
dihal.text("`~!@#$%^&*.,:;'|\_\"", 0, 45, mini8B, ALIGN_CENTER)
dihal.text("()[]{}<>",             0, 54, mini8B, ALIGN_CENTER)
measure_time.end("Rendering time")

measure_time.begin()
dihal.refresh()
measure_time.end("Refreshing time")

mem_used.print_ram_used()
