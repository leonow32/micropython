# MicroPython 1.28.0 ESP32-S3 Octal SPIRAM

import mem_used
import measure_time

from display_hal.display_hal import *
from display_hal.font.console7 import *
from display_hal.font.dos8 import *
from display_hal.font.galaxy16_digits import *
from display_hal.font.mini8 import *
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

measure_time.begin()
dihal.color_set(RED, BLACK)
dihal.text("-= Font Benchmark =-", 0, 0, console7, ALIGN_CENTER)
dihal.color_set(YELLOW, BLUE)
dihal.text("abcdefghijklmnopqrstuvwxyz01234", 0, 8, mini8, ALIGN_CENTER)
dihal.text("ąęłćśńóźż", 0, 16, extronic16_unicode, ALIGN_LEFT)
dihal.color_set(BLACK, YELLOW)
dihal.text("ąęłćśńóźż", 0, 16, extronic16B_unicode, ALIGN_RIGHT)
dihal.text("abcdefghijklmnop", 0, 32, dos8, ALIGN_CENTER)
dihal.text("qrstuvwxyz123345", 0, 40, dos8, ALIGN_CENTER)
dihal.color_set(RED, WHITE)
dihal.text("0123456789", 0, 49, galaxy16_digits, ALIGN_CENTER)
measure_time.end("Rendering time")

measure_time.begin()
dihal.refresh()
measure_time.end("Refreshing time")

mem_used.print_ram_used()
