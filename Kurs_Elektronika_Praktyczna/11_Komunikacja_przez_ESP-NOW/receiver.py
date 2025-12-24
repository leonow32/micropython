# MicroPython 1.27.0 ESP32 Pico
# MicroPython 1.27.0 ESP32-S3 Octal SPIRAM

import espnow
import network

sta = network.WLAN(network.STA_IF)
sta.active(True)

mac = sta.config('mac')
print(f"MAC Address: {mac}")

e = espnow.ESPNow()
e.active(True)

while True:
    sender, data = e.recv(-1)
    data = data.decode()
    print(f"{sender} -> {data}")
