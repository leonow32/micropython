# MicroPython 1.24.1 ESP32-S3 Octal SPIRAM

from machine import Pin, SPI
from st7796_horizontal import *
# from st7796_vertical import *
import mem_used
import random
import time

spi = SPI(2, baudrate=80_000_000, polarity=0, phase=0, sck=Pin(15), mosi=Pin(7), miso=None)
display = ST7796(spi, cs=Pin(4), dc=Pin(6), rst=Pin(5))

start_time = time.ticks_us()
    
row = 0
step = 256 / (HEIGHT // 5)

# Red -> Yellow
temp = 0
for i in range(HEIGHT // 5):
    display.hline(0, row, WIDTH, display.color(255, temp, 0))
    temp += step
    row += 1

# Yellow -> Green
temp = 256
for i in range(HEIGHT // 5):
    display.hline(0, row, WIDTH, display.color(temp, 255, 0))
    temp -= step
    row += 1

# Green -> Cyan
temp = 0
for i in range(HEIGHT // 5):
    display.hline(0, row, WIDTH, display.color(0, 255, temp))
    temp += step
    row += 1

# Cyan -> Blue
temp = 256
for i in range(HEIGHT // 5):
    display.hline(0, row, WIDTH, display.color(0, temp, 255))
    temp -= step
    row += 1

# Blue -> Magenta
temp = 0
for i in range(HEIGHT // 5):
    display.hline(0, row, WIDTH, display.color(temp, 0, 255))
    temp += step
    row += 1

work_time = (time.ticks_us() - start_time) / 1000    
display.text(f"Czas: {work_time}ms", 10, 10, BLACK) 
display.refresh()
