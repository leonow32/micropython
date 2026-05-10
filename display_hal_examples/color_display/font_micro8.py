# MicroPython 1.28.0 ESP32-S3 Octal SPIRAM

import mem_used
import measure_time

from display_hal.display_hal import *
from display_hal.font.micro8 import *

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
dihal.text("ABCDEFGHIJKLM",              0,  0, micro8, ALIGN_CENTER)
dihal.color_set(YELLOW, BLACK)
dihal.text("NOPQRSTUVWXYZ",              0, 14, micro8, ALIGN_CENTER)
dihal.color_set(GREEN, BLACK)
dihal.text("abcdefghijklmnopqrstuvwxyz", 0, 28, micro8, ALIGN_CENTER)
dihal.color_set(CYAN, BLACK)
dihal.text("0123456789+-*/=()[]{}<>",    0, 42, micro8, ALIGN_CENTER)
dihal.color_set(BLUE, BLACK)
dihal.text("`~!@#$%^&*.,:;'|\/_\"",      0, 56, micro8, ALIGN_CENTER)
measure_time.end("Rendering time")

measure_time.begin()
dihal.refresh()
measure_time.end("Refreshing time")

mem_used.print_ram_used()
