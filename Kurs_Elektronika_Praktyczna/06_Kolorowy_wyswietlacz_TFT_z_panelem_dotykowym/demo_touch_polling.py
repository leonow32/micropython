# MicroPython 1.24.1 ESP32-S3 Octal SPIRAM

from machine import Pin, SPI, I2C
import ft6336_polling as ft6336
import st7796_vertical as st7796
import random

event_str = {
    ft6336.EVENT_PRESS:   "Press",
    ft6336.EVENT_LIFT:    "Lift",
    ft6336.EVENT_CONTACT: "Contact",
    ft6336.EVENT_NONE:    "None",
}

def draw_point(x, y, event):
    display.fill_rect(0, 0, 320, 8, st7796.BLUE)
    display.text(f"x={x:3d}, y={y:3d}, event={event_str[event]}", 0, 0, random.randint(0, 65535))
    if event == ft6336.EVENT_PRESS:
        display.pixel(x, y, st7796.GREEN)
    elif event == ft6336.EVENT_CONTACT:
        display.pixel(x, y, st7796.GREEN)
    elif event == ft6336.EVENT_LIFT:
        display.pixel(x, y, st7796.RED)
    display.refresh()
    
spi = SPI(2, baudrate=80_000_000, polarity=0, phase=0, sck=Pin(15), mosi=Pin(7), miso=None)
display = st7796.ST7796(spi, cs=Pin(4), dc=Pin(6), rst=Pin(5))

i2c = I2C(0)
touch = ft6336.FT6336(i2c, 100, draw_point)

display.fill(st7796.BLACK)
display.refresh()
