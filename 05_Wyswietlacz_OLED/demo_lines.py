# MicroPython 1.24.1 ESP32-S3 Octal SPIRAM

from machine import Pin, I2C
import ssd1309
import mem_used
import random
import time

LOOPS = const(100)

i2c = I2C(0, scl=Pin(1), sda=Pin(2), freq=400000)
display = ssd1309.SSD1309(i2c)

x1 = 0
y1 = 0

start_time = time.ticks_ms()

for i in range(LOOPS):
    x2 = random.randrange(ssd1309.WIDTH)
    y2 = random.randrange(ssd1309.HEIGHT)
    display.line(x1, y1, x2, y2, 1)
    display.refresh()
    x1 = x2
    y1 = y2

end_time = time.ticks_ms()
work_time = end_time - start_time
frame_time = work_time / LOOPS

print(f"Frame time: {frame_time} ms")
print(f"Frame rate: {1000/frame_time} fps")

mem_used.print_ram_used()
