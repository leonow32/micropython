import binascii
import espnow
import network

sta = network.WLAN(network.STA_IF)
sta.active(True)

mac = sta.config('mac')
mac = binascii.hexlify(mac, ":").decode().upper()
print(f"MAC Address: {mac}")

e = espnow.ESPNow()
e.active(True)

while True:
    sender, data = e.recv(-1)
    sender = binascii.hexlify(sender, ":").decode().upper()
    data = data.decode()
    print(f"{sender} -> {data}")
