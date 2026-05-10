# MicroPython 1.28.0 ESP32-S3 Octal SPIRAM

import mem_used
import measure_time
import random
import time

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

LOOPS = const(100)
x1 = 0
y1 = 0

measure_time.begin()

for i in range(LOOPS):
    x2 = random.randrange(dihal.width)
    y2 = random.randrange(dihal.height)
    r  = random.randrange(256)
    g  = random.randrange(256)
    b  = random.randrange(256)
    dihal.color_set(dihal.color(r, g, b))
    dihal.line(x1, y1, x2, y2)
    dihal.refresh()
    x1 = x2
    y1 = y2

measure_time.end("Work time")

mem_used.print_ram_used()

