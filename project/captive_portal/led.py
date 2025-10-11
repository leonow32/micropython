import neopixel
import sys
from machine import Pin

def init():
    global led
    if "ESP32 " in sys.implementation._machine:
        led = neopixel.NeoPixel(Pin(21, Pin.OUT), 1)
    elif "ESP32S3" in sys.implementation._machine:
        led = neopixel.NeoPixel(Pin(38, Pin.OUT), 1)
    elif "RP2040" in sys.implementation._machine:
        led = neopixel.NeoPixel(Pin(0, Pin.OUT), 1)
    else:
        raise Exception("Microcontroller not supported")

def write(r, g, b):
    global led
    led[0] = (r, g, b)
    led.write()
    
def read():
    global led
    return led[0]