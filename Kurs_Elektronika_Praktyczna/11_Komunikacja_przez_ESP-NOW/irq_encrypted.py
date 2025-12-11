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
e.set_pmk(b'\x00\x11\x22\x33\x44\x55\x66\x77\x88\x99\xAA\xBB\xCC\xDD\xEE\xFF')

def receive_cb(e):
    sender, data = e.irecv()
    sender = binascii.hexlify(sender, ":").decode().upper()
    data = data.decode()
    print(f"{sender} -> {data}")

e.irq(receive_cb)
