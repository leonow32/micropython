from machine import Pin, I2C
from dos16 import *
from sans16B_unicode import *
import framebuf
import ssd1309
import mem_used
import time

def print_char(screen, font, char, x, y):
    try:
        bitmap = font[ord(char)]
    except:
        bitmap = font[0]
        print(f"Char {char} doesn't exist in font")
    
    buffer = framebuf.FrameBuffer(bitmap[3:], bitmap[1], bitmap[0], 0)
    screen.blit(buffer, x, y)
    return bitmap[1] + bitmap[2]
    

def print_text(screen, font, text, x, y):
    for char in text:
        x += print_char(screen, font, char, x, y)
        

i2c = I2C(0, scl=Pin(1), sda=Pin(2), freq=400000)
display = ssd1309.SSD1309(i2c)
start_time = time.ticks_us()

#print_char(display, dos16["F"], 0, 0)
#print_char(display, dos16["j"], 8, 0)
print_text(display, dos16, "Test DOS 16x8", 0, 0)
print_text(display, sans16B_unicode, "Test San16B", 0, 16)
print_text(display, sans16B_unicode, "ĄĘĆŚŃŁÓŹŻ", 0, 32)
print_text(display, sans16B_unicode, "ąęćśńłóźż", 0, 48)

display.refresh()

end_time = time.ticks_us()
print(f"Work time: {end_time-start_time} us")
mem_used.print_ram_used()
