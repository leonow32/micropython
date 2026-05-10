# MicroPython 1.28.0 ESP32-S3 Octal SPIRAM

import mem_used
import measure_time

from display_hal.display_hal import *
from display_hal.image_mono.ball_64x64 import *

# Display TFT-LCD 480x320 with ST7565R
from machine import Pin, PWM, SPI
from display_hal.driver.st7796 import *
pwm = PWM(Pin(16), freq=50000, duty_u16=65535)
spi = SPI(2, baudrate=80_000_000, polarity=0, phase=0, sck=Pin(15), mosi=Pin(7), miso=None)
display = ST7796(spi, cs=Pin(4), dc=Pin(6), rst=Pin(5), rotate=0)
# display = ST7796(spi, cs=Pin(4), dc=Pin(6), rst=Pin(5), rotate=90)
# display = ST7796(spi, cs=Pin(4), dc=Pin(6), rst=Pin(5), rotate=180)
# display = ST7796(spi, cs=Pin(4), dc=Pin(6), rst=Pin(5), rotate=270)

dihal   = DisplayHAL(display)
print(dihal)

measure_time.begin()

# Fill the background
dihal.color_set(BLUE, BLACK)
dihal.fill()

cols = 3
rows = 3
icon_width  = 64
icon_height = 64
sw = (dihal.width-cols*icon_width) // (cols+1)   # separator width
sh = (dihal.height-rows*icon_height) // (rows+1) # separator height

def get_x(col):
    return sw*(col+1)+icon_width*col

def get_y(row):
    return sh*(row+1)+icon_height*row
    
# Row 0, Col 0 - foreground off, background off
dihal.color_set(BLACK, BLACK)
dihal.image(ball_64x64, get_x(0), get_y(0))

# Row 0, Col 1 - foreground off, background on (negative)
dihal.color_set(BLACK, WHITE)
dihal.image(ball_64x64, get_x(1), get_y(0))

# Row 0, Col 2 - foreground off, background transparent
dihal.color_set(BLACK, -1)
dihal.image(ball_64x64, get_x(2), get_y(0))

# Row 1, Col 0 - foreground on, background off
dihal.color_set(WHITE, BLACK)
dihal.image(ball_64x64, get_x(0), get_y(1))

# Row 1, Col 1 - foreground on, background on
dihal.color_set(WHITE, WHITE)
dihal.image(ball_64x64, get_x(1), get_y(1))

# Row 1, Col 2 - foreground on, background transparent
dihal.color_set(WHITE, -1)
dihal.image(ball_64x64, get_x(2), get_y(1))

# Row 2, Col 0 - foreground transparent, background off
dihal.color_set(-1, BLACK)
dihal.image(ball_64x64, get_x(0), get_y(2))

# Row 2, Col 1 - foreground transparent, background on
dihal.color_set(-1, WHITE)
dihal.image(ball_64x64, get_x(1), get_y(2))

# Row 2, Col 2 - foreground transparent, background transparent
dihal.color_set(-1, -1)
dihal.image(ball_64x64, get_x(2), get_y(2))

measure_time.end("Rendering time")

measure_time.begin()
dihal.refresh()
measure_time.end("Refreshing time")

mem_used.print_ram_used()


