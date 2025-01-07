from machine import Pin, I2C
from font.dos16 import *
# from mpy.dos16 import *
import framebuf
import ssd1309
import simulator
import mem_used
import time       

button = Pin(0, Pin.IN, Pin.PULL_UP)
i2c = I2C(0, scl=Pin(1), sda=Pin(2), freq=400000)
try:
    display = ssd1309.SSD1309(i2c)
except:
    display = simulator.SIM()

char = 0
for page in range(4):
    for row in range(4):
        for col in range(16):
            string = chr(char)
            display.print_text(dos16, string, col*8, row*16)
            char += 1
    display.refresh()
    time.sleep_ms(100)
    while button(): pass

char = 0
for page in range(4):
    for row in range(4):
        for col in range(16):
            string = chr(char)
            display.print_text(dos16, string, col*8, row*16, 0, 0)
            char += 1
    display.refresh()
    time.sleep_ms(100)
    while button(): pass

mem_used.print_ram_used()



