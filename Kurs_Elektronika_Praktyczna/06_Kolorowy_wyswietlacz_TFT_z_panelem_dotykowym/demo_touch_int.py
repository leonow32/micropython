# MicroPython 1.24.1 ESP32-S3 Octal SPIRAM

from machine import Pin, SPI, I2C
import ft6336_int as ft6336
import st7796_vertical as st7796

prev_x = 0
prev_y = 0
prev_e = ft6336.EVENT_NONE
refresh_request = False

def irq_handler(x, y, e):
    if e == ft6336.EVENT_PRESS:
        global prev_x
        global prev_y
        global prev_e
        global refresh_request
        e_str = "Press"
        prev_x = x
        prev_y = y
        prev_e = e
    
    elif e == ft6336.EVENT_CONTACT:
        global prev_x
        global prev_y
        global prev_e
        global refresh_request
        e_str = "Contact"
#         display.pixel(x, y, st7796.YELLOW)
        display.line(x, y, prev_x, prev_y, st7796.GREEN if prev_e == ft6336.EVENT_PRESS else st7796.YELLOW)
#         display.refresh()
        
        prev_x = x
        prev_y = y
        prev_e = e
        refresh_request = True
        
    elif e == ft6336.EVENT_LIFT:
        global prev_x
        global prev_y
        global prev_e
        global refresh_request
        e_str = "Lift"
#         display.pixel(x, y, st7796.RED)
        display.line(x, y, prev_x, prev_y, st7796.RED)
#         display.refresh()
        prev_x = x
        prev_y = y
        prev_e = e
        refresh_request = True
        
    else:
        e_str = "None"
    
    print(f"x={x:3d}, y={y:3d}, e_str={e_str}")

spi = SPI(2, baudrate=80_000_000, polarity=0, phase=0, sck=Pin(15), mosi=Pin(7), miso=None)
display = st7796.ST7796(spi, cs=Pin(4), dc=Pin(6), rst=Pin(5))

i2c = I2C(0)
print(i2c)
touch = ft6336.FT6336(i2c, int_gpio=Pin(16), int_cb=irq_handler)

display.fill(st7796.BLACK)
display.refresh()

while True:
    if refresh_request:
        display.refresh()
        refresh_request = False

