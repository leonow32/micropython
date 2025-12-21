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
e.add_peer(b'\xdc\xda\x0c\x1eN\xe0', b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0A\x0B\x0C\x0D\x0E\x0F', encrypt=True)

def receive_cb(e):
    sender, data = e.irecv()
    sender = binascii.hexlify(sender, ":").decode().upper()
    data = data.decode()
    print(f"{sender} -> {data}")

e.irq(receive_cb)
