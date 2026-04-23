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
# from machine import Pin, PWM, SPI
# from display_hal.driver.dem128064e1 import *
# pwm = PWM(Pin(15), freq=50000, duty_u16=65535)
# spi = SPI(0, baudrate=10_000_000, polarity=0, phase=0, sck=Pin(2), mosi=Pin(3), miso=Pin(4))
# display = DEM128064E1(spi, cs=Pin(5), dc=Pin(6), rst=Pin(7))

# Display LCD DEM240064B 240x64 from Display Elektronik GmbH with ST7565P
from machine import Pin, PWM, SPI
from display_hal.driver.dem240064b import *
pwm = PWM(Pin(28), freq=50000, duty_u16=65535)
spi = SPI(0, baudrate=10_000_000, polarity=0, phase=0, sck=Pin(18), mosi=Pin(19), miso=Pin(16))
display = DEM240064B(spi, cs0=Pin(17), cs1=Pin(22), dc=Pin(20), rst=Pin(21))

dihal   = DisplayHAL(display)
print(dihal)

def print_all_characters(hal, font):
    x = 0
    y = 0
    
    hal.clear()

    for index in sorted(font):
        data = font[index]
        
        if index == -1:
            char_height, char_space = data
            continue
            
        else:
            char_width = data[0]
            
            # Check if a character fits on the current line
            if x + char_width + char_space <= hal.width:
                hal.text(chr(index), x, y, font)
                x += char_width + char_space
            
            # The character does not fit on the current line.
            else:
                x = 0
                y += char_height
                
                # Checking if the character height fits on a new line
                if y + char_height <= hal.height:
                    hal.text(chr(index), x, y, font)
                    x += char_width + char_space
                
                # The character does not fit on a new line -> refresh the screen
                else:
                    hal.refresh()
                    input("Press enter")
                    
                    x = 0
                    y = 0
                    hal.clear()
                    hal.text(chr(index), x, y, font)
                    x += char_width + char_space
    
    hal.refresh()
    
# Print all the characters in positive
dihal.color_set(1, 0)

# from display_hal.font.console7 import console7 as font
# from display_hal.font.dos8 import dos8 as font
# from display_hal.font.dos16 import dos16 as font
# from display_hal.font.extronic16_unicode import extronic16_unicode as font
# from display_hal.font.extronic16B_unicode import extronic16B_unicode as font
# from display_hal.font.galaxy16_digits import galaxy16_digits as font
# from display_hal.font.galaxy24_digits import galaxy24_digits as font
# from display_hal.font.micro8 import micro8 as font
# from display_hal.font.mini8 import mini8 as font
# from display_hal.font.mini8B import mini8B as font
# from display_hal.font.sans24 import sans24 as font
from display_hal.font.sans24B import sans24B as font

print_all_characters(dihal, font)

mem_used.print_ram_used()
