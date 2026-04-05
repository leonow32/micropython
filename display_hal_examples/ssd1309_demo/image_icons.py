# MicroPython 1.24.1 ESP32-S3 Octal SPIRAM
# MicroPython 1.27.0 ESP32 Pico

from machine import I2C
from display_hal.display_hal import *
from display_hal.driver.ssd1309 import *

from display_hal.image_mono.back_32x32 import *
from display_hal.image_mono.book_32x32 import *
from display_hal.image_mono.cancel_32x32 import *
from display_hal.image_mono.clock_32x32 import *
from display_hal.image_mono.down_32x32 import *
from display_hal.image_mono.hand_32x32 import *
from display_hal.image_mono.light_32x32 import *
from display_hal.image_mono.ok_32x32 import *
from display_hal.image_mono.settings_32x32 import *
from display_hal.image_mono.up_32x32 import *

import mem_used
import measure_time

i2c     = I2C(0) # use default pinout and clock frequency
display = SSD1309(i2c, rotate=False, address=0x3C)
dihal   = DisplayHAL(display)
print(dihal)

measure_time.begin()
dihal.image(ok_32x32,        0,  0)
dihal.image(back_32x32,      0, 32)
dihal.image(clock_32x32,    32,  0)
dihal.image(settings_32x32, 32, 32)
dihal.image(book_32x32,     64,  0)
dihal.image(light_32x32,    64, 32)
dihal.image(up_32x32,       96,  0)
dihal.image(down_32x32,     96, 32)
measure_time.end("Rendering time")

measure_time.begin()
dihal.refresh()
measure_time.end("Refreshing time")

dihal.simulate()

mem_used.print_ram_used()
