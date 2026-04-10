# MicroPython 1.24.1 ESP32-S3 Octal SPIRAM
# MicroPython 1.27.0 ESP32 Pico

from machine import Pin, PWM, SPI
from display_hal.display_hal import *
from display_hal.driver.dem240064b import *

from display_hal.image_mono.ball_16x16 import *
from display_hal.image_mono.chess_8x8 import *

import mem_used
import measure_time

pwm = PWM(Pin(28), freq=50000, duty_u16=65535)
spi = SPI(0, baudrate=10_000_000, polarity=0, phase=0, sck=Pin(18), mosi=Pin(19), miso=Pin(16))
display = DEM240064B(spi, cs0=Pin(17), cs1=Pin(22), dc=Pin(20), rst=Pin(21))
dihal = DisplayHAL(display)
print(dihal)

measure_time.begin()

# Chessboard as a background
dihal.color_set(1, 0)
for x in range(0, dihal.width, 8):
    for y in range(0, dihal.height, 8):
        dihal.image(chess_8x8, x, y)

# Row 0, Col 0 - foreground off, background off
dihal.color_set(0, 0)
dihal.image(ball_16x16, 48, 4)

# Row 0, Col 1 - foreground off, background on (negative)
dihal.color_set(0, 1)
dihal.image(ball_16x16, 112, 4)

# Row 0, Col 2 - foreground off, background transparent
dihal.color_set(0, -1)
dihal.image(ball_16x16, 176, 4)

# Row 1, Col 0 - foreground on, background off
dihal.color_set(1, 0)
dihal.image(ball_16x16, 48, 24)

# Row 1, Col 1 - foreground on, background on
dihal.color_set(1, 1)
dihal.image(ball_16x16, 112, 24)

# Row 1, Col 2 - foreground on, background transparent
dihal.color_set(1, -1)
dihal.image(ball_16x16, 176, 24)

# Row 2, Col 0 - foreground transparent, background off
dihal.color_set(-1, 0)
dihal.image(ball_16x16, 48, 44)

# Row 2, Col 1 - foreground transparent, background on
dihal.color_set(-1, 1)
dihal.image(ball_16x16, 112, 44)

# Row 2, Col 2 - foreground transparent, background transparent
dihal.color_set(-1, -1)
dihal.image(ball_16x16, 176, 44)

measure_time.end("Rendering time")

measure_time.begin()
dihal.refresh()
measure_time.end("Refreshing time")

mem_used.print_ram_used()

