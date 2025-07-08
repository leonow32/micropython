# MicroPython 1.24.1 ESP32-S3 Octal SPIRAM

from machine import Pin, SPI, I2C
import ft6336
import st7796_vertical as st7796
import mem_used

def draw_point(result_tuple):
    x, y, pressed = result_tuple
    print(f"{x:3d} {y:3d} {pressed}")
    if(pressed):
        display.pixel(x, y, st7796.YELLOW)
    else:
        display.pixel(x, y, st7796.RED)
    display.refresh()
    
spi = SPI(2, baudrate=80_000_000, polarity=0, phase=0, sck=Pin(15), mosi=Pin(7), miso=None)
display = st7796.ST7796(spi, cs=Pin(4), dc=Pin(6), rst=Pin(5))

i2c = I2C(0)
touch = ft6336.FT6336(i2c, 10, draw_point)

mem_used.print_ram_used()
