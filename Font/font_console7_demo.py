from machine import Pin, I2C
from font.console7 import *
# from mpy.console7 import *
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
start_time = time.ticks_us()

display.print_text(console7,  "ABCDEFGHIJKLM", 0, 0, "C")
display.print_text(console7,  "NOPQRSTUVWXYZ", 0, 8, "C")
display.print_text(console7, "abcdefghijkl", 0, 16, "C")
display.print_text(console7, "mnopqrstuvwxyz", 0, 24, "C")
display.print_text(console7,  "0123456789", 0, 32, "C")
display.print_text(console7,  "+-*/=()[]{}<>", 0, 40, "C")
display.print_text(console7, "`~!@#$%^&*.,:;'|\/_\"", 0, 48, "C")
display.refresh()

end_time = time.ticks_us()
print(f"Work time: {end_time-start_time} us")
mem_used.print_ram_used()



