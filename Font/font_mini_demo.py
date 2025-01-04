from machine import Pin, I2C
from font.mini8 import *
import framebuf
import ssd1309
import simulator
import mem_used
import time       

button = Pin(0, Pin.IN, Pin.PULL_UP)
i2c = I2C(0, scl=Pin(1), sda=Pin(2), freq=400000)
display = ssd1309.SSD1309(i2c)
#display = simulator.SIM()
start_time = time.ticks_us()

display.print_text(mini8,  "ABCDEFGHIJKLM", 0, 0, "C")
display.print_text(mini8,  "NOPQRSTUVWXYZ", 0, 14, "C")
display.print_text(mini8, "abcdefghijklmnopqrstuvwxyz", 0, 28, "C")
display.print_text(mini8,  "0123456789+-*/=()[]{}<>", 0, 42, "C")
display.print_text(mini8, "`~!@#$%^&*.,:;'|\/_\"", 0, 56, "C")
display.refresh()

while button(): pass
display.fill(0)
display.print_text(mini8,  "ABCDEFGHIJKLM", 0, 0, "C", 0)
display.print_text(mini8,  "NOPQRSTUVWXYZ", 0, 14, "C", 0)
display.print_text(mini8, "abcdefghijklmnopqrstuvwxyz", 0, 28, "C", 0)
display.print_text(mini8,  "0123456789+-*/=()[]{}<>", 0, 42, "C", 0)
display.print_text(mini8, "`~!@#$%^&*.,:;'|\/_\"", 0, 56, "C", 0)
display.refresh()

end_time = time.ticks_us()
print(f"Work time: {end_time-start_time} us")
mem_used.print_ram_used()


