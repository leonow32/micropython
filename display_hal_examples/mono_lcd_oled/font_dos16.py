# MicroPython 1.24.1 ESP32-S3 Octal SPIRAM
# MicroPython 1.27.0 ESP32 Pico

import mem_used
import measure_time

from display_hal.display_hal import *
from display_hal.font.dos16 import *

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

char = 0
dihal.color_set(1, 0)
for page in range(4):
    for row in range(4):
        for col in range(16):
            string = chr(char)
            dihal.text(string, col*8, row*16, dos16)
            char += 1
    dihal.refresh()
    input("Press enter")

char = 0
dihal.color_set(0, 1)
for page in range(4):
    for row in range(4):
        for col in range(16):
            string = chr(char)
            dihal.text(string, col*8, row*16, dos16)
            char += 1
    dihal.refresh()
    input("Press enter")
    
mem_used.print_ram_used()
