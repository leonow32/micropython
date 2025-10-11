import machine
import sys

if sys.platform == "esp32":
    import esp32
elif sys.platform == "rp2":
    raise Exception("Microcontroller not supported")
else:
    raise Exception("Microcontroller not supported")

def temperature_get():
    if "ESP32 " in sys.implementation._machine:
        return int((esp32.raw_temperature() - 32) / 1.8)
    elif "ESP32S3" in sys.implementation._machine:
        return esp32.mcu_temperature()
#     elif "RP2040" in sys.implementation._machine:
#         led = neopixel.NeoPixel(Pin(0, Pin.OUT), 1)
    else:
        raise Exception("Microcontroller not supported")


