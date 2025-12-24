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
e.set_pmk(b'\x00\x11\x22\x33\x44\x55\x66\x77\x88\x99\xAA\xBB\xCC\xDD\xEE\xFF')

sender_mac = b'\xdc\xda\x0c\x1eN\xe0'
e.add_peer(sender_mac, b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0A\x0B\x0C\x0D\x0E\x0F', encrypt=True)

while True:
    sender, data = e.recv(-1)
    data = data.decode()
    print(f"{sender} -> {data}")
