# MicroPython 1.24.1 ESP32-S3 Octal SPIRAM

from machine import Pin, I2C
from font.micro8 import *
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

display.print_text(micro8,  "ABCDEFGHIJKLM", 0, 0, "C")
display.print_text(micro8,  "NOPQRSTUVWXYZ", 0, 14, "C")
display.print_text(micro8, "abcdefghijklmnopqrstuvwxyz", 0, 28, "C")
display.print_text(micro8,  "0123456789+-*/=()[]{}<>", 0, 42, "C")
display.print_text(micro8, "`~!@#$%^&*.,:;'|\/_\"", 0, 56, "C")
display.refresh()

time.sleep_ms(100)
while button(): pass
display.fill(0)
display.print_text(micro8,  "ABCDEFGHIJKLM", 0, 0, "C", 0)
display.print_text(micro8,  "NOPQRSTUVWXYZ", 0, 14, "C", 0)
display.print_text(micro8, "abcdefghijklmnopqrstuvwxyz", 0, 28, "C", 0)
display.print_text(micro8,  "0123456789+-*/=()[]{}<>", 0, 42, "C", 0)
display.print_text(micro8, "`~!@#$%^&*.,:;'|\/_\"", 0, 56, "C", 0)
display.refresh()

time.sleep_ms(100)
while button(): pass
display.fill(0)
display.print_text(micro8,  "Litwo, Ojczyzno moja! ty jestes ", 0, 0, "C")
display.print_text(micro8,  "jak zdrowie. Ile cie trzeba cenic,", 0, 8, "C")
display.print_text(micro8,  "ten tylko sie dowie, kto cie stracil.", 0, 16, "C")
display.print_text(micro8,  "Dzis pieknosc twa w calej ozdobie", 0, 24, "C")
display.print_text(micro8,  "Widze i opisuje, bo tesknie po tobie.", 0, 32, "C")
display.print_text(micro8,  "Gdy od placzacej matki, pod Twoja", 0, 40, "C")
display.print_text(micro8,  "opieke ofiarowany martwa podnios-", 0, 48, "C")
display.print_text(micro8,  "lem powieke i zaraz moglem pieszo", 0, 56, "C")
display.refresh()

mem_used.print_ram_used()



