# MicroPython 1.27.0 ESP32 Pico
# MicroPython 1.27.0 ESP32-S3 Octal SPIRAM

import binascii
import espnow
import network

sta = network.WLAN(network.STA_IF)
sta.active(True)
# sta.config(channel=6, protocol=network.WLAN.PROTOCOL_LR)

mac = sta.config('mac')
print(f"MAC Address: {mac}")

mac = binascii.hexlify(mac, ":").decode().upper()
print(f"MAC Address: {mac}")

e = espnow.ESPNow()
e.active(True)

def receive_cb(e):
    sender, data = e.irecv()
    sender = binascii.hexlify(sender, ":").decode().upper()
    data = data.decode()
    print(f"{sender} -> {data}")

e.irq(receive_cb)
