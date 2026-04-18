# MicroPython 1.27.0 ESP32 Pico

import mem_used
import measure_time
import time

from display_hal.display_hal import *
from display_hal.font.galaxy16_digits import *
from display_hal.font.galaxy24_digits import *

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

while True:
    time_tuple = time.localtime()
    dihal.clear()
    dihal.text(f"{time_tuple[3]}:{time_tuple[4]:02}", 127, 10, galaxy24_digits, ALIGN_CENTER)
    dihal.text(f"{time_tuple[2]}.{time_tuple[1]:02}.{time_tuple[0]}", 127, 38, galaxy16_digits, ALIGN_CENTER)
    dihal.refresh()
    mem_used.print_ram_used()
    time.sleep(60)
    #machine.lightsleep(60_000)
