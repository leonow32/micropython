# MicroPython 1.24.1 ESP32-S3 Octal SPIRAM
# MicroPython 1.27.0 ESP32 Pico

from machine import I2C
from display_hal.display_hal import *
from display_hal.driver.ssd1309 import *

from display_hal.font.dos16 import *

import mem_used
import measure_time

i2c     = I2C(0) # use default pinout and clock frequency
display = SSD1309(i2c, rotate=False, address=0x3C)
dihal   = DisplayHAL(display)
print(dihal)

char = 0
for page in range(4):
    for row in range(4):
        for col in range(16):
            string = chr(char)
            dihal.text(string, col*8, row*16, 1, dos16)
            char += 1
    dihal.refresh()
    input("Press enter")

char = 0
for page in range(4):
    for row in range(4):
        for col in range(16):
            string = chr(char)
            dihal.text(string, col*8, row*16, 0, dos16)
            char += 1
    dihal.refresh()
    input("Press enter")
    
mem_used.print_ram_used()
