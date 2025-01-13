# MicroPython 1.24.1 ESP32-S3 Octal SPIRAM

import time
from machine import Pin

print("Hello world!")

button = Pin(0, Pin.IN, Pin.PULL_UP)
led    = Pin(21, Pin.OUT)
name   = input("Jak masz na imię? ")
print(f"Cześć {name}!!!")

print("Naciśnij przycisk")
while button() != 0:
    pass

for i in range(5):
    print("Dioda świeci")
    led(1)
    time.sleep_ms(250)
    print("Dioda nie świeci")
    led(0)
    time.sleep_ms(250)

print("Koniec programu!")
