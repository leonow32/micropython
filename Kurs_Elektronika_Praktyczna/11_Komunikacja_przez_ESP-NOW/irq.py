# MicroPython 1.27.0 ESP32 Pico
# MicroPython 1.27.0 ESP32-S3 Octal SPIRAM

import binascii
import espnow
import network

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
# wlan.config(channel=6, protocol=network.WLAN.PROTOCOL_LR)

mac = wlan.config('mac')
print(f"MAC Address: {mac}")

mac = binascii.hexlify(mac, ":").decode().upper()
print(f"MAC Address: {mac}")

e = espnow.ESPNow()
e.active(True)

def receive_cb(e):
    while e.any():
        sender, data = e.irecv()
#         print(type(sender))
#         print(type(data))
        sender = binascii.hexlify(sender, ":").decode().upper()
        data = data.decode()
        print(f"{sender} -> {data}")
    print("No more messages")

#e.irq(receive_cb)
