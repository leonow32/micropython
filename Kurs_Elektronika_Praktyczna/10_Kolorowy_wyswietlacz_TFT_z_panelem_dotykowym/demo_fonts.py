# MicroPython 1.24.1 ESP32-S3 Octal SPIRAM

from machine import Pin, SPI
import mem_used
import st7796_horizontal as st7796
# import st7796_vertical as st7796
import time

from font.console7 import *
from font.dos8 import *
from font.dos16 import *
from font.galaxy16_digits import *
from font.galaxy24_digits import *
from font.micro8 import *
from font.mini8 import *
from font.sans24 import *
from font.sans24B import *
from font.squared16_unicode import *
from font.squared16B_unicode import *
      
cs  = Pin(17, Pin.OUT, value=1)
dc  = Pin(15, Pin.OUT, value=1)
rst = Pin(16, Pin.OUT, value=1)
spi = SPI(2, baudrate=80_000_000, polarity=0, phase=0, sck=Pin(6), mosi=Pin(7), miso=None)
display = st7796.ST7796(spi, cs, dc, rst)

start_time = time.ticks_us()
display.print_text(squared16B_unicode, "Testy czcionek na wyświetlaczu TFT", 0, 0, "C", st7796.WHITE)

display.print_text(squared16B_unicode, "Console7", 0, 16, "L", st7796.GREEN)
display.print_text(console7,           "ABCDEFGHIJKLMNOPQRSTUVWXYZ abcdefghijklmnopqrstuvwxyz", 0, 16, "C", st7796.YELLOW)
display.print_text(console7,           "0123456789 +-*/=()[]{}<>`~!@#$%^&*.,:;'|\/_\"", 0, 24, "C", st7796.YELLOW)

display.print_text(squared16B_unicode, "Micro8", 0, 32, "L", st7796.GREEN)
display.print_text(micro8,             "ABCDEFGHIJKLMNOPQRSTUVWXYZ abcdefghijklmnopqrstuvwxyz 0123456789 +-*/=()[]{}<>`~!@#$%^&*.,:;'|\/_\"", 0, 38, "R", st7796.YELLOW)

display.print_text(squared16B_unicode, "Mini8", 0, 48, "L", st7796.GREEN)
display.print_text(mini8,              "ABCDEFGHIJKLMNOPQRSTUVWXYZ abcdefghijklmnopqrstuvwxyz 0123456789 +-*/=()[]{}<>`~!@#$%^&*.,:;'|\/_\"", 0, 54, "R", st7796.YELLOW)

display.print_text(squared16B_unicode, "Dos8", 0, 64, "L", st7796.GREEN)
display.print_text(dos8,               "ABCDEFGHIJKLMNOPQRSTUVWXYZ abcdefghijklmnopqrstuvwxyz ", 0, 64, "R", st7796.YELLOW)
display.print_text(dos8,               "0123456789 +-*/=()[]{}<>`~!@#$%^&*.,:;'|\/_\"", 0, 72, "R", st7796.YELLOW)

display.print_text(squared16B_unicode, "Dos16", 0, 80, "L", st7796.GREEN)
display.print_text(dos16,              "ABCDEFGHIJKLMNOPQRSTUVWXYZ abcdefghijklmnopqrstuvwxyz ", 0, 80, "R", st7796.YELLOW)
display.print_text(dos16,              "0123456789 +-*/=()[]{}<>`~!@#$%^&*.,:;'|\/_\"", 0, 96, "R", st7796.YELLOW)

display.print_text(squared16B_unicode, "Squared16", 0, 112, "L", st7796.GREEN)
display.print_text(squared16_unicode,  "ABCDEFGHIJKLMNOPQRSTUVWXYZ abcdefghijklmnopqrstuvwxyz ", 0, 112, "R", st7796.YELLOW)
display.print_text(squared16_unicode,  "0123456789 +-*/=()[]{}<>`~!@#$%^&*.,:;'|\/_\"", 0, 128, "R", st7796.YELLOW)

display.print_text(squared16B_unicode, "Squared16B", 0, 144, "L", st7796.GREEN)
display.print_text(squared16B_unicode, "ABCDEFGHIJKLMNOPQRSTUVWXYZ abcdefghijklmnopqrstuvwxyz ", 0, 144, "R", st7796.YELLOW)
display.print_text(squared16B_unicode, "0123456789 +-*/=()[]{}<>`~!@#$%^&*.,:;'|\/_\"", 0, 160, "R", st7796.YELLOW)

display.print_text(squared16B_unicode, "Sans24", 0, 176, "L", st7796.GREEN)
display.print_text(sans24,             "ABCDEFGHIJKLMNOPQRSTUVWXYZ  ", 0, 176, "R", st7796.YELLOW)
display.print_text(sans24,             "abcdefghijklmnopqrstuvwxyz 0123456789", 0, 200, "R", st7796.YELLOW)

display.print_text(squared16B_unicode, "Sans24B", 0, 224, "L", st7796.GREEN)
display.print_text(sans24B,            "ABCDEFGHIJKLMNOPQRSTUVWXYZ  ", 0, 224, "R", st7796.YELLOW)
display.print_text(sans24B,            "abcdefghijklmnopqrstuvwxyz 0123456789", 0, 248, "R", st7796.YELLOW)

display.print_text(squared16B_unicode, "Galaxy16", 0, 272, "L", st7796.GREEN)
display.print_text(galaxy16_digits,    "0123456789.:'", 0, 272, "C", st7796.YELLOW)

display.print_text(squared16B_unicode, "Galaxy24", 0, 288, "L", st7796.GREEN)
display.print_text(galaxy24_digits,    "0123456789.:'ACFMP", 0, 288, "R", st7796.YELLOW)

end_time = time.ticks_us()

display.refresh()

mem_used.print_ram_used()
print(f"Work time: {end_time-start_time} us")






