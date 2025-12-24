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

peer_mac = b'\xd8\xa0\x1di\x9fD'
everyone = b'\xFF\xFF\xFF\xFF\xFF\xFF'
e.add_peer(peer_mac)
e.add_peer(everyone)

e.send(everyone, "Wiadomość do wszystkich")
e.send(everyone, "Wiadomość do wszystkich bez potwierdzenia odbioru", False)
e.send(peer_mac, "Wiadomość do wybranego odbiorcy")
