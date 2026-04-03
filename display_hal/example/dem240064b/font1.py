import mem_used
import measure_time
from machine import Pin, PWM, SPI
from display_hal.display_hal import *
from display_hal.driver.dem240064b import *
from display_hal.font.extronic16B_unicode import *

pwm = PWM(Pin(28), freq=50000, duty_u16=65535)
spi = SPI(0, baudrate=10_000_000, polarity=0, phase=0, sck=Pin(18), mosi=Pin(19), miso=Pin(16))
display = DEM240064B(spi, cs0=Pin(17), cs1=Pin(22), dc=Pin(20), rst=Pin(21))
dihal = DisplayHAL(display)
print(dihal)

measure_time.begin()
dihal.text("abcdefghijklmnopqrstuvwxyz0123456789", 0,  0, 1, extronic16B_unicode, "CENTER")
dihal.text("ABCDEFGHIJKLMNOPQRSTUVWXYZ", 0, 16, 1, extronic16B_unicode, "CENTER")
dihal.text("абвгдеёжзийклмнопрстуфхцчшщъыьэ", 0, 32, 1, extronic16B_unicode, "CENTER")
dihal.text("АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩ", 0, 48, 1, extronic16B_unicode, "CENTER")
measure_time.end("Rendering time")

measure_time.begin()
dihal.refresh()
measure_time.end("Refreshing time")

mem_used.print_ram_used()
