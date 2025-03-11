import machine
from font.galaxy16_digits import *
from font.galaxy24_digits import *
import ssd1309
import mem_used
import time

i2c = machine.I2C(0, scl=machine.Pin(1), sda=machine.Pin(2), freq=400000)
display = ssd1309.SSD1309(i2c)

while True:
    time_tuple = time.localtime()
    display.fill(0)
    display.print_text(galaxy24_digits, f"{time_tuple[3]}:{time_tuple[4]:02}", 127, 10, "C")
    display.print_text(galaxy16_digits, f"{time_tuple[2]}.{time_tuple[1]:02}.{time_tuple[0]}", 127, 38, "C")
    display.refresh()
    mem_used.print_ram_used()
    time.sleep(60)
    #machine.lightsleep(60_000)

