# MicroPython 1.24.1 ESP32-S3 Octal SPIRAM
# MicroPython 1.27.0 ESP32
# MicroPython 1.27.0 Raspbbery Pi Pico 2

import mem_used
import measure_time

from display_hal.display_hal import *

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
# from machine import Pin, SPI
# from display_hal.driver.sh1108 import *
# spi = SPI(1, baudrate=10_000_000, polarity=0, phase=0)
# display = SH1108(spi, cs=Pin(4), dc=Pin(2), rotate=1, offset_x=16)

# Display LCD DEM128064E1 128x64 from Display Elektronik GmbH with ST7565R
from machine import Pin, PWM, SPI
from display_hal.driver.dem128064e1 import *
pwm = PWM(Pin(15), freq=50000, duty_u16=65535)
spi = SPI(0, baudrate=10_000_000, polarity=0, phase=0, sck=Pin(2), mosi=Pin(3), miso=Pin(4))
display = DEM128064E1(spi, cs=Pin(5), dc=Pin(6), rst=Pin(7))

# Display LCD DEM240064B 240x64 from Display Elektronik GmbH with ST7565P
# from machine import Pin, PWM, SPI
# from display_hal.driver.dem240064b import *
# pwm = PWM(Pin(28), freq=50000, duty_u16=65535)
# spi = SPI(0, baudrate=10_000_000, polarity=0, phase=0, sck=Pin(18), mosi=Pin(19), miso=Pin(16))
# display = DEM240064B(spi, cs0=Pin(17), cs1=Pin(22), dc=Pin(20), rst=Pin(21))

dihal   = DisplayHAL(display)
print(dihal)

measure_time.begin()

images = (
    dihal.image_load("display_hal/image_mono/ok_32x32.bin"),
    dihal.image_load("display_hal/image_mono/clock_32x32.bin"),
    dihal.image_load("display_hal/image_mono/book_32x32.bin"),
    dihal.image_load("display_hal/image_mono/up_32x32.bin"),
    dihal.image_load("display_hal/image_mono/back_32x32.bin"),
    dihal.image_load("display_hal/image_mono/settings_32x32.bin"),
    dihal.image_load("display_hal/image_mono/cancel_32x32.bin"),
    dihal.image_load("display_hal/image_mono/down_32x32.bin"),
    dihal.image_load("display_hal/image_mono/hand_32x32.bin"),
    dihal.image_load("display_hal/image_mono/light_32x32.bin")
)

icon_width  = images[0].width
icon_height = images[0].height

if dihal.width == 240 and dihal.height == 64:
    cols = 5
    rows = 2
else:
    cols = dihal.width  // icon_width
    rows = dihal.height // icon_height

sw = (dihal.width-cols*icon_width) // (cols+1)   # separator width
sh = (dihal.height-rows*icon_height) // (rows+1) # separator height

for row in range(rows):
    for col in range(cols):
        dihal.image(images[(row*cols+col)%10], sw*(col+1)+icon_width*col, sh*(row+1)+icon_height*row)

measure_time.end("Rendering time")

measure_time.begin()
dihal.refresh()
measure_time.end("Refreshing time")

print("-----")
print(f"Array of {cols} columns and {rows} rows.")
print(f"Horizontal separator: {sw:3} px")
print(f"Vertical separator:   {sh:3} px")
print("-----")

mem_used.print_ram_used()
