# MicroPython 1.24.1 ESP32-S3 Octal SPIRAM

from machine import Pin, SPI, I2C
import ft6336
import st7796
import mem_used

def draw_point(result_tuple):
    x, y, pressed = result_tuple
    print(f"{x:3d} {y:3d} {pressed}")
    if(pressed):
        display.pixel(x, y, st7796.YELLOW)
    else:
        display.pixel(x, y, st7796.RED)
    display.refresh()
    
cs  = Pin(17, Pin.OUT, value=1)
dc  = Pin(15, Pin.OUT, value=1)
rst = Pin(16, Pin.OUT, value=1)
spi = SPI(2, baudrate=80_000_000, polarity=0, phase=0, sck=Pin(5), mosi=Pin(6), miso=Pin(4))
display = st7796.ST7796(spi, cs, dc, rst)

i2c = I2C(0, scl=Pin(1), sda=Pin(2), freq=400000)
touch = ft6336.FT6336(i2c, 10, draw_point)

mem_used.print_ram_used()
