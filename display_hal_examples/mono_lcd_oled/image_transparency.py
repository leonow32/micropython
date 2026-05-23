# MicroPython 1.24.1 ESP32-S3 Octal SPIRAM
# MicroPython 1.27.0 ESP32
# MicroPython 1.27.0 Raspbbery Pi Pico 2

import mem_used
import measure_time

from display_hal.display_hal import *

# Display OLED 128x64 monochrome with SSD1309
# from machine import I2C
# from display_hal.driver.ssd1309 import *
# i2c     = I2C(0) # use default pinout and clock frequency
# display = SSD1309(i2c, address=0x3C, rotate=False)

# Display OLED 128x64 monochrome with SH1106
# from machine import I2C
# from display_hal.driver.sh1106 import *
# i2c     = I2C(0) # use default pinout and clock frequency
# display = SH1106(i2c, address=0x3D, rotate=False, offset_x=2)

# Display OLED 128x160 monochrome with SH1108
# from machine import Pin, SPI
# from display_hal.driver.sh1108 import *
# spi = SPI(1, baudrate=10_000_000, polarity=0, phase=0)
# display = SH1108(spi, cs=Pin(4), dc=Pin(2), rotate=1, offset_x=16)

# Display LCD DEM128064E1 128x64 from Display Elektronik GmbH with ST7565R
from machine import Pin, PWM, SPI
from display_hal.driver.dem128064e1 import *
pwm = PWM(Pin(15), freq=50000, duty_u16=65535)
spi = SPI(0, baudrate=10_000_000, polarity=0, phase=0, sck=Pin(2), mosi=Pin(3), miso=Pin(4))
display = DEM128064E1(spi, cs=Pin(5), dc=Pin(6), rst=Pin(7))

# Display LCD DEM240064B 240x64 from Display Elektronik GmbH with ST7565P
# from machine import Pin, PWM, SPI
# from display_hal.driver.dem240064b import *
# pwm = PWM(Pin(28), freq=50000, duty_u16=65535)
# spi = SPI(0, baudrate=10_000_000, polarity=0, phase=0, sck=Pin(18), mosi=Pin(19), miso=Pin(16))
# display = DEM240064B(spi, cs0=Pin(17), cs1=Pin(22), dc=Pin(20), rst=Pin(21))

dihal   = DisplayHAL(display)
print(dihal)

measure_time.begin()

chess_8x8  = dihal.image_load("display_hal/image_mono/chess_8x8.bin")
ball_16x16 = dihal.image_load("display_hal/image_mono/ball_16x16.bin")

# Chessboard as a background
dihal.color_set(1, 0)
for x in range(0, dihal.width, chess_8x8.width):
    for y in range(0, dihal.height, chess_8x8.height):
        dihal.image(chess_8x8, x, y)

cols = 3
rows = 3
sw = (dihal.width-cols*ball_16x16.width) // (cols+1)   # separator width
sh = (dihal.height-rows*ball_16x16.height) // (rows+1) # separator height

def get_x(col):
    return sw*(col+1) + col*ball_16x16.width

def get_y(row):
    return sh*(row+1) + row*ball_16x16.height
    
# Row 0, Col 0 - foreground off, background off
dihal.color_set(0, 0)
dihal.image(ball_16x16, get_x(0), get_y(0))

# Row 0, Col 1 - foreground off, background on (negative)
dihal.color_set(0, 1)
dihal.image(ball_16x16, get_x(1), get_y(0))

# Row 0, Col 2 - foreground off, background transparent
dihal.color_set(0, -1)
dihal.image(ball_16x16, get_x(2), get_y(0))

# Row 1, Col 0 - foreground on, background off
dihal.color_set(1, 0)
dihal.image(ball_16x16, get_x(0), get_y(1))

# Row 1, Col 1 - foreground on, background on
dihal.color_set(1, 1)
dihal.image(ball_16x16, get_x(1), get_y(1))

# Row 1, Col 2 - foreground on, background transparent
dihal.color_set(1, -1)
dihal.image(ball_16x16, get_x(2), get_y(1))

# Row 2, Col 0 - foreground transparent, background off
dihal.color_set(-1, 0)
dihal.image(ball_16x16, get_x(0), get_y(2))

# Row 2, Col 1 - foreground transparent, background on
dihal.color_set(-1, 1)
dihal.image(ball_16x16, get_x(1), get_y(2))

# Row 2, Col 2 - foreground transparent, background transparent
dihal.color_set(-1, -1)
dihal.image(ball_16x16, get_x(2), get_y(2))

measure_time.end("Rendering time")

measure_time.begin()
dihal.refresh()
measure_time.end("Refreshing time")

mem_used.print_ram_used()

