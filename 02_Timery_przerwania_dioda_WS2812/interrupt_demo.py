# MicroPython 1.24.1 ESP32-S3 Octal SPIRAM

import mem_used
import neopixel
import random
from machine import Pin, Timer

def timer_int(source):
    print(f"Przerwanie od {source}")
    
    led[0] = (0, 0, 0)
    led.write()

def button_int(source):
    print(f"Przerwanie od {source}")
    
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    
    led[0] = (r, g, b)
    led.write()
    
    print(f"Wylosowany kolor to: {led[0]}")
    
    Timer(0, mode=Timer.ONE_SHOT, period=2000, callback=timer_int)

button = Pin(0, Pin.IN, Pin.PULL_UP)
button.irq(trigger=Pin.IRQ_FALLING, handler=button_int)
led = neopixel.NeoPixel(Pin(38, Pin.OUT), 1)
mem_used.print_ram_used()
