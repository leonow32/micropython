# MicroPython 1.24.1 ESP32-S3 Octal SPIRAM

from machine import Pin, SPI
import mem_used
import st7796_horizontal as st7796
# import st7796_vertical as st7796
import time

from image.ep_logo import *

spi = SPI(2, baudrate=80_000_000, polarity=0, phase=0, sck=Pin(15), mosi=Pin(7), miso=None)
display = st7796.ST7796(spi, cs=Pin(4), dc=Pin(6), rst=Pin(5))

start_time = time.ticks_us()
display.blit(ep_logo, 0,  105)
end_time = time.ticks_us()
display.refresh()

mem_used.print_ram_used()
print(f"Work time: {end_time-start_time} us")

