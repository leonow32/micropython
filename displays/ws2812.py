from machine import Pin
from neopixel import NeoPixel

gpio = Pin(38, Pin.OUT)
np = NeoPixel(gpio, 1)
np[0] = (0, 255, 0)
np.write()
