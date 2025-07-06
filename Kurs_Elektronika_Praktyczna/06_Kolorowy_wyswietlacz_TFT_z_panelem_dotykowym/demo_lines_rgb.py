# MicroPython 1.24.1 ESP32-S3 Octal SPIRAM

from machine import Pin, SPI
import st7796_vertical as st7796
import st7796_horizontal as st7796
import mem_used
import random
import time

LOOPS = const(1000)
COLORS = (st7796.RED, st7796.YELLOW, st7796.GREEN, st7796.CYAN, st7796.BLUE, st7796.MAGENTA, st7796.WHITE)

cs  = Pin(4,  Pin.OUT, value=1)
dc  = Pin(6, Pin.OUT, value=1)
rst = Pin(5, Pin.OUT, value=1)
spi = SPI(2, baudrate=80_000_000, polarity=0, phase=0, sck=Pin(15), mosi=Pin(7), miso=None)
display = st7796.ST7796(spi, cs, dc, rst)

x1 = 0
y1 = 0

start_time = time.ticks_ms()

for i in range(LOOPS):
    x2 = random.randrange(st7796.WIDTH)
    y2 = random.randrange(st7796.HEIGHT)
    display.line(x1, y1, x2, y2, COLORS[random.randrange(7)])
    display.refresh()
    x1 = x2
    y1 = y2

end_time = time.ticks_ms()
work_time = end_time - start_time
frame_time = work_time / LOOPS

print(f"Frame time: {frame_time} ms")
print(f"Frame rate: {1000/frame_time} fps")

mem_used.print_ram_used()



