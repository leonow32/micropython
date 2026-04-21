# MicroPython 1.24.1 ESP32-S3 Octal SPIRAM
# MicroPython 1.27.0 ESP32
# MicroPython 1.27.0 Raspbbery Pi Pico 2

import mem_used
import measure_time

from display_hal.display_hal import *
from display_hal.font.dos16 import *
from display_hal.font.extronic16B_unicode import *

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

def print_char(hal, font, x, y):
    pass
    
        
def print_all_characters(hal, font):
    x = 0
    y = 0
    n = 0
    loop = 0
    char_height, char_space = font[-1]
    
    hal.clear()
                
    for index, data in font.items():
        print(f"loop: {loop}, index: {index}, data: {data}")
        
        if index == -1:
            print("aaaaa")
            continue
            
        else:
            char_width = data[0]
            
            # Sprawdzenie czy znak pasuje w kierunku x
            if x + char_width + char_space < hal.width:
                hal.text(chr(index), x, y, font)
                x += char_width + char_space
            else:
                hal.circle(30, 30, 10)
                hal.refresh()
                input("Press enter")
                x = 0
                y = 0
                hal.clear()
            
            
            
            
            
            
            # Verify is this char fits into remaining area of the screen
#             if x + char_width + char_space < hal.width and y + char_height < hal.height:
#                 hal.text(chr(n), x, y, font)
#                 char_printed = True
#             else:
#                 char_printed = False
#             
#             x += char_width + char_space
#             if x >= hal.width:
#                 x = 0
#                 y += char_height
#                 if
                
            
                
        
    
# Print all the characters in positive
dihal.color_set(1, 0)
# print_all_characters(dihal, dos16)
print_all_characters(dihal, extronic16B_unicode)

mem_used.print_ram_used()

