# MicroPython 1.27.0 ESP32 Pico
# MicroPython 1.27.0 ESP32-S3 Octal SPIRAM

import espnow
import network

wlan = network.WLAN(network.STA_IF)
wlan.active(True)

mac = wlan.config('mac')
print(f"MAC Address: {mac}")

e = espnow.ESPNow()
e.active(True)
e.set_pmk(b'\x00\x11\x22\x33\x44\x55\x66\x77\x88\x99\xAA\xBB\xCC\xDD\xEE\xFF')

receiver_mac = b'\xd8\xa0\x1di\x9fD'
e.add_peer(receiver_mac, b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0A\x0B\x0C\x0D\x0E\x0F', encrypt=True)

e.send(receiver_mac, "Szyfrowana wiadomość")
