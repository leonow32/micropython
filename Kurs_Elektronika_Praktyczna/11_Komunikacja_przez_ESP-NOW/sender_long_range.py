# MicroPython 1.27.0 ESP32 Pico
# MicroPython 1.27.0 ESP32-S3 Octal SPIRAM

import espnow
import network

sta = network.WLAN(network.STA_IF)
sta.active(True)
sta.config(channel=6, protocol=network.WLAN.PROTOCOL_LR)

mac = sta.config('mac')
print(f"MAC Address: {mac}")

e = espnow.ESPNow()
e.active(True)
e.config(rate=espnow.RATE_LORA_250K)

everyone = b'\xFF\xFF\xFF\xFF\xFF\xFF'
e.add_peer(everyone)

e.send(everyone, "Test długiego zasięgu")
