# MicroPython 1.28.0 ESP32-S3 Octal SPIRAM

import mem_used
import measure_time

from display_hal.display_hal import *
from display_hal.font.extronic16_unicode import *
from display_hal.font.extronic16B_unicode import *

# Display TFT-LCD 480x320 with ST7565R
from machine import Pin, PWM, SPI
from display_hal.driver.st7796 import *
pwm = PWM(Pin(16), freq=50000, duty_u16=65535)
spi = SPI(2, baudrate=80_000_000, polarity=0, phase=0, sck=Pin(15), mosi=Pin(7), miso=None)
display = ST7796(spi, cs=Pin(4), dc=Pin(6), rst=Pin(5), rotate=0)
# display = ST7796(spi, cs=Pin(4), dc=Pin(6), rst=Pin(5), rotate=90)
# display = ST7796(spi, cs=Pin(4), dc=Pin(6), rst=Pin(5), rotate=180)
# display = ST7796(spi, cs=Pin(4), dc=Pin(6), rst=Pin(5), rotate=270)

dihal   = DisplayHAL(display)
print(dihal)

dihal.color_set(RED, BLACK)
dihal.text("abcdefghijklmnopqrstuvwxyz0123456789", 0, 16*0, extronic16_unicode,  ALIGN_CENTER)
dihal.text("abcdefghijklmnopqrstuvwxyz0123456789", 0, 16*1, extronic16B_unicode, ALIGN_CENTER)

dihal.color_set(YELLOW, BLACK)
dihal.text("ABCDEFGHIJKLMNOPQRSTUVWXYZ",           0, 16*2, extronic16_unicode,  ALIGN_CENTER)
dihal.text("ABCDEFGHIJKLMNOPQRSTUVWXYZ",           0, 16*3, extronic16B_unicode, ALIGN_CENTER)

dihal.color_set(GREEN, BLACK)
dihal.text("абвгдеёжзийклмнопрстуфхцчшщъыьэ",      0, 16*4, extronic16_unicode,  ALIGN_CENTER)
dihal.text("абвгдеёжзийклмнопрстуфхцчшщъыьэ",      0, 16*5, extronic16B_unicode, ALIGN_CENTER)

dihal.color_set(BLUE, BLACK)
dihal.text("АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩ",          0, 16*6, extronic16_unicode,  ALIGN_CENTER)
dihal.text("АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩ",          0, 16*7, extronic16B_unicode, ALIGN_CENTER)
dihal.refresh()
    
mem_used.print_ram_used()
