import neopixel
import sys
import time
from machine import Pin, Timer

if "ESP32 " in sys.implementation._machine:
    led = neopixel.NeoPixel(Pin(21, Pin.OUT), 1)
elif "ESP32S3" in sys.implementation._machine:
    led = neopixel.NeoPixel(Pin(38, Pin.OUT), 1)
elif "RP2040" in sys.implementation._machine:
    led = neopixel.NeoPixel(Pin(0, Pin.OUT), 1)
else:
    raise Exception("Microcontroller not supported")

def update_led(r, g, b):
    print(f"update_led({r:3d}, {g:3d}, {b:3d})")
    led[0] = (r, g, b)
    led.write()
    time.sleep_ms(10)

while True:
    for g in range(0, 256):        update_led(255,   g,   0)   # red     -> yellow
    for r in range(255, -1, -1):   update_led(  r, 255,   0)   # yellow  -> green
    for b in range(0, 256):        update_led(  0, 255,   b)   # green   -> cyan
    for g in range(255, -1, -1):   update_led(  0,   g, 255)   # cyan    -> blue
    for r in range(0, 256):        update_led(  r,   0, 255)   # blue    -> magenta
    for b in range(255, -1, -1):   update_led(255,   0,   b)   # magenta -> red