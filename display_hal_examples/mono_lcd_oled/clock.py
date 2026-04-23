# MicroPython 1.27.0 ESP32 Pico
# MicroPython 1.27.0 Raspbbery Pi Pico 2

import mem_used
import measure_time
import time

from display_hal.display_hal import *
from display_hal.font.galaxy16_digits import *
from display_hal.font.galaxy24_digits import *

# Display OLED 128x64 monochrome with SSD1309
# from machine import I2C
# from display_hal.driver.ssd1309 import *
# i2c     = I2C(0) # use default pinout and clock frequency
# display = SSD1309(i2c, address=0x3C, rotate=False)

# Display OLED 128x64 monochrome with SH1106
# from machine import I2C
# from display_hal.driver.sh1106 import *
# i2c     = I2C(0) # use default pinout and clock frequency
# display = SH1106(i2c, address=0x3D, rotate=False, offset_x=2)

# Display OLED 128x160 monochrome with SH1108
from machine import Pin, SPI
from display_hal.driver.sh1108 import *
spi = SPI(1, baudrate=10_000_000, polarity=0, phase=0)
display = SH1108(spi, cs=Pin(4), dc=Pin(2), rotate=1, offset_x=16)

# Display LCD DEM128064E1 from Display Elektronik GmbH with ST7565R
# from machine import Pin, PWM, SPI
# from display_hal.driver.dem128064e1 import *
# pwm = PWM(Pin(15), freq=50000, duty_u16=65535)
# spi = SPI(0, baudrate=10_000_000, polarity=0, phase=0, sck=Pin(2), mosi=Pin(3), miso=Pin(4))
# display = DEM128064E1(spi, cs=Pin(5), dc=Pin(6), rst=Pin(7))

dihal   = DisplayHAL(display)
print(dihal)

while True:
    time_tuple = time.localtime()
    dihal.clear()
    dihal.text(f"{time_tuple[3]}:{time_tuple[4]:02}", 127, 10, galaxy24_digits, ALIGN_CENTER)
    dihal.text(f"{time_tuple[2]}.{time_tuple[1]:02}.{time_tuple[0]}", 127, 38, galaxy16_digits, ALIGN_CENTER)
    dihal.refresh()
    mem_used.print_ram_used()
    time.sleep(60)
    #machine.lightsleep(60_000)
