# MicroPython 1.24.1 ESP32-S3 Octal SPIRAM
# MicroPython 1.27.0 ESP32 Pico

from machine import Pin, PWM, SPI
from display_hal.display_hal import *
from display_hal.driver.dem240064b import *

from display_hal.image_mono.world_128x64 import *

import mem_used
import measure_time

pwm = PWM(Pin(28), freq=50000, duty_u16=65535)
spi = SPI(0, baudrate=10_000_000, polarity=0, phase=0, sck=Pin(18), mosi=Pin(19), miso=Pin(16))
display = DEM240064B(spi, cs0=Pin(17), cs1=Pin(22), dc=Pin(20), rst=Pin(21))
dihal = DisplayHAL(display)
print(dihal)

measure_time.begin()
dihal.image(world_128x64, 56, 0)

measure_time.end("Rendering time")

measure_time.begin()
dihal.refresh()
measure_time.end("Refreshing time")

mem_used.print_ram_used()

