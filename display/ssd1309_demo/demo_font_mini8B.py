# MicroPython 1.24.1 ESP32-S3 Octal SPIRAM

from machine import Pin, I2C
from font.mini8B import *
import framebuf
import ssd1309
import simulator
import mem_used
import time       

button = Pin(0, Pin.IN, Pin.PULL_UP)
i2c = I2C(0) # use default pinout and clock frequency
print(i2c)   # print pinout and clock frequency
try:
    display = ssd1309.SSD1309(i2c)
except:
    display = simulator.SIM()

display.print_text(mini8B, "ABCDEFGHIJKLMN",       0,  0, "C")
display.print_text(mini8B, "OPQRSTUVWXYZ",         0,  9, "C")
display.print_text(mini8B, "abcdefghijklmn",       0, 18, "C")
display.print_text(mini8B, "opqrstuvwxyz",         0, 27, "C")
display.print_text(mini8B, "0123456789+-*/=",      0, 36, "C")
display.print_text(mini8B, "`~!@#$%^&*.,:;'|\_\"", 0, 45, "C")
display.print_text(mini8B, "()[]{}<>",             0, 54, "C")
display.refresh()
"""
time.sleep_ms(100)
while button(): pass
display.fill(0)
display.print_text(mini8B,  "ABCDEFGHIJKLM", 0, 0, "C", 0)
display.print_text(mini8B,  "NOPQRSTUVWXYZ", 0, 14, "C", 0)
display.print_text(mini8B, "abcdefghijklmnopqrstuvwxyz", 0, 28, "C", 0)
display.print_text(mini8B,  "0123456789+-*/=()[]{}<>", 0, 42, "C", 0)
display.print_text(mini8B, "`~!@#$%^&*.,:;'|\/_\"", 0, 56, "C", 0)
display.refresh()
"""
"""
time.sleep_ms(100)
while button(): pass
display.fill(0)
display.print_text(mini8,  "Litwo, Ojczyzno moja! ty jestes ", 0, 0, "C")
display.print_text(mini8,  "jak zdrowie. Ile cie trzeba cenic,", 0, 8, "C")
display.print_text(mini8,  "ten tylko sie dowie, kto cie stracil.", 0, 16, "C")
display.print_text(mini8,  "Dzis pieknosc twa w calej ozdobie", 0, 24, "C")
display.print_text(mini8,  "Widze i opisuje, bo tesknie po tobie.", 0, 32, "C")
display.print_text(mini8,  "Gdy od placzacej matki, pod Twoja", 0, 40, "C")
display.print_text(mini8,  "opieke ofiarowany martwa podnios-", 0, 48, "C")
display.print_text(mini8,  "lem powieke i zaraz moglem pieszo", 0, 56, "C")
display.refresh()
"""

mem_used.print_ram_used()



