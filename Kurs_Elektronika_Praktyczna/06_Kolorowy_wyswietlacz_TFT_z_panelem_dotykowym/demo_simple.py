from machine import Pin, SPI
from st7796_horizontal import *
# from st7796_vertical import *
import framebuf
import time

spi = SPI(2, baudrate=80_000_000, polarity=0, phase=0, sck=Pin(15), mosi=Pin(7), miso=None)
display = ST7796(spi, cs=Pin(4), dc=Pin(6), rst=Pin(5))

display.rect(0, 0, 128, 64, WHITE)
display.text('abcdefghijklm', 1, 2, RED)
display.text('nopqrstuvwxyz', 1, 10, YELLOW)
display.text('ABCDEFGHIJKLM', 1, 18, GREEN)
display.text('NOPQRSTUVWXYZ', 1, 26, CYAN)
display.text('0123456789+-*/', 1, 34, BLUE)
display.text('!@#$%^&*(),.<>?', 1, 42, MAGENTA)
display.refresh()
