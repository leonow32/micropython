# MicroPython 1.24.1 ESP32-S3 Octal SPIRAM
# MicroPython 1.27.0 ESP32 Pico

from machine import I2C
from display_hal.display_hal import *
from display_hal.driver.ssd1309 import *

from display_hal.image_mono.ball_16x16 import *
from display_hal.image_mono.chess_8x8 import *

import mem_used
import measure_time

i2c     = I2C(0) # use default pinout and clock frequency
display = SSD1309(i2c, rotate=False, address=0x3C)
dihal   = DisplayHAL(display)
print(dihal)

measure_time.begin()

# Chessboard as a background
for x in range(0, dihal.width, 8):
    for y in range(0, dihal.height, 8):
        dihal.image(chess_8x8, x, y)

dihal.image(ball_16x16, 20, 4)
dihal.image(ball_16x16, 56, 4)
dihal.image(ball_16x16, 92, 4)

dihal.image(ball_16x16, 20, 24)
dihal.image(ball_16x16, 56, 24)
dihal.image(ball_16x16, 92, 24)

dihal.image(ball_16x16, 20, 44)
dihal.image(ball_16x16, 56, 44)
dihal.image(ball_16x16, 92, 44)

measure_time.end("Rendering time")

measure_time.begin()
dihal.refresh()
measure_time.end("Refreshing time")

dihal.simulate()

mem_used.print_ram_used()


