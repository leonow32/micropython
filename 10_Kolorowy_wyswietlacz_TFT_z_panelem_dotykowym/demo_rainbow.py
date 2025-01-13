# MicroPython 1.24.1 ESP32-S3 Octal SPIRAM

from machine import Pin, SPI
import st7796
import mem_used
import random
import time

cs  = Pin(17, Pin.OUT, value=1)
dc  = Pin(15, Pin.OUT, value=1)
rst = Pin(16, Pin.OUT, value=1)
spi = SPI(2, baudrate=80_000_000, polarity=0, phase=0, sck=Pin(5), mosi=Pin(6), miso=Pin(4))
display = st7796.ST7796(spi, cs, dc, rst)

start_time = time.ticks_us()
    
row = 0
step = 256 / (st7796.HEIGHT // 5)

# Red -> Yellow
temp = 0
for i in range(st7796.HEIGHT // 5):
    display.hline(0, row, st7796.WIDTH, display.color(255, temp, 0))
    temp += step
    row += 1

# Yellow -> Green
temp = 256
for i in range(st7796.HEIGHT // 5):
    display.hline(0, row, st7796.WIDTH, display.color(temp, 255, 0))
    temp -= step
    row += 1

# Green -> Cyan
temp = 0
for i in range(st7796.HEIGHT // 5):
    display.hline(0, row, st7796.WIDTH, display.color(0, 255, temp))
    temp += step
    row += 1

# Cyan -> Blue
temp = 256
for i in range(st7796.HEIGHT // 5):
    display.hline(0, row, st7796.WIDTH, display.color(0, temp, 255))
    temp -= step
    row += 1

# Blue -> Magenta
temp = 0
for i in range(st7796.HEIGHT // 5):
    display.hline(0, row, st7796.WIDTH, display.color(temp, 0, 255))
    temp += step
    row += 1

work_time = (time.ticks_us() - start_time) / 1000    
display.text(f"Czas: {work_time}ms", 10, 10, st7796.BLACK) 
display.refresh()
