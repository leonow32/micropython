# MicroPython 1.27.0 ESP32 Pico
# MicroPython 1.27.0 ESP32-S3 Octal SPIRAM

import binascii
import espnow
import network
import measure_time

sta = network.WLAN(network.STA_IF)
sta.active(True)
# sta.config(channel=6, protocol=network.WLAN.PROTOCOL_LR)

ap = network.WLAN(network.AP_IF)
ap.active(True)

# mac = sta.config('mac')
mac = ap.config('mac')
print(f"MAC Address: {mac}")

mac = binascii.hexlify(mac, ":").decode().upper()
print(f"MAC Address: {mac}")

e = espnow.ESPNow()
e.active(True)
# e.config(rate=espnow.RATE_LORA_250K)

peer_mac = b'\xd8\xa0\x1di\x9fD'
everyone = b'\xFF\xFF\xFF\xFF\xFF\xFF'
e.add_peer(peer_mac)
e.add_peer(everyone)

measure_time.begin()
e.send(everyone, "Starting...")
e.send(everyone, "Hello 1234567890", False)  # No respose needed
e.send(everyone, "end")

e.send(peer_mac, "Dedicated message")
measure_time.end("Operation time")