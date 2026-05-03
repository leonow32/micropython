# MicroPython 1.28.0 ESP32-S3 Octal SPIRAM

import mem_used
import measure_time

from display_hal.display_hal import *

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

dihal.color_set(YELLOW, BLUE)

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
# dihal.color_set(1, 0)

# from display_hal.font.console7 import console7 as font
# from display_hal.font.dos8 import dos8 as font
# from display_hal.font.dos16 import dos16 as font
# from display_hal.font.extronic16_unicode import extronic16_unicode as font
from display_hal.font.extronic16B_unicode import extronic16B_unicode as font
# from display_hal.font.galaxy16_digits import galaxy16_digits as font
# from display_hal.font.galaxy24_digits import galaxy24_digits as font
# from display_hal.font.micro8 import micro8 as font
# from display_hal.font.mini8 import mini8 as font
# from display_hal.font.mini8B import mini8B as font
# from display_hal.font.sans24 import sans24 as font
# from display_hal.font.sans24B import sans24B as font

print_all_characters(dihal, font)

mem_used.print_ram_used()

