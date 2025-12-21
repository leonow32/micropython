# MicroPython 1.27.0 ESP32 Pico
# MicroPython 1.27.0 ESP32-S3 Octal SPIRAM

import binascii
import espnow
import network

wlan = network.WLAN(network.STA_IF)
wlan.active(True)

mac = wlan.config('mac')
mac = binascii.hexlify(mac, ":").decode().upper()
print(f"MAC Address: {mac}")

e = espnow.ESPNow()
e.active(True)

while True:
    sender, data = e.recv(-1)
    sender = binascii.hexlify(sender, ":").decode().upper()
    data = data.decode()
    print(f"{sender} -> {data}")
