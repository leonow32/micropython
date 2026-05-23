# MicroPython 1.28.0 ESP32-S3 Octal SPIRAM

import mem_used
import measure_time
import random

from display_hal.display_hal import *

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

images = (
    dihal.image_load("display_hal/image_mono/ok_32x32.bin"),
    dihal.image_load("display_hal/image_mono/clock_32x32.bin"),
    dihal.image_load("display_hal/image_mono/book_32x32.bin"),
    dihal.image_load("display_hal/image_mono/up_32x32.bin"),
    dihal.image_load("display_hal/image_mono/back_32x32.bin"),
    dihal.image_load("display_hal/image_mono/settings_32x32.bin"),
    dihal.image_load("display_hal/image_mono/cancel_32x32.bin"),
    dihal.image_load("display_hal/image_mono/down_32x32.bin"),
    dihal.image_load("display_hal/image_mono/hand_32x32.bin"),
    dihal.image_load("display_hal/image_mono/light_32x32.bin")
)

colors = (RED, YELLOW, GREEN, CYAN, BLUE, MAGENTA, WHITE, BLACK)

icon_width  = images[0].width
icon_height = images[0].height

cols = dihal.width  // icon_width
rows = dihal.height // icon_height

sw = (dihal.width-cols*icon_width) // (cols+1)   # separator width
sh = (dihal.height-rows*icon_height) // (rows+1) # separator height

for row in range(rows):
    for col in range(cols):
        color_fg = colors[random.randrange(len(colors))]
        color_bg = colors[random.randrange(len(colors))]
        dihal.color_set(color_fg, color_bg)
        dihal.image(images[(row*cols+col)%10], sw*(col+1)+icon_width*col, sh*(row+1)+icon_height*row)

measure_time.end("Rendering time")

measure_time.begin()
dihal.refresh()
measure_time.end("Refreshing time")

print("-----")
print(f"Array of {cols} columns and {rows} rows.")
print(f"Horizontal separator: {sw:3} px")
print(f"Vertical separator:   {sh:3} px")
print("-----")

mem_used.print_ram_used()

