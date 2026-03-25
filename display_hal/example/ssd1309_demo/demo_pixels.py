# MicroPython 1.24.1 ESP32-S3 Octal SPIRAM

from machine import Pin, I2C
import ssd1309
import mem_used
import random
import time

LOOPS = const(1000)

i2c = I2C(0) # use default pinout and clock frequency
print(i2c)   # print pinout and clock frequency
display = ssd1309.SSD1309(i2c)

x1 = 0
y1 = 0

start_time = time.ticks_ms()

for i in range(LOOPS):
    x = random.randrange(ssd1309.WIDTH)
    y = random.randrange(ssd1309.HEIGHT)
    display.pixel(x, y, 0) # black pixel
    x = random.randrange(ssd1309.WIDTH)
    y = random.randrange(ssd1309.HEIGHT)
    display.pixel(x, y, 1) # white pixel
    display.refresh()

end_time = time.ticks_ms()
work_time = end_time - start_time
frame_time = work_time / LOOPS

print(f"Frame time: {frame_time} ms")
print(f"Frame rate: {1000/frame_time} fps")

mem_used.print_ram_used()

