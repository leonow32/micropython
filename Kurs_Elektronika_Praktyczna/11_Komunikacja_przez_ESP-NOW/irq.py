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

def receive_cb(e):
    sender, data = e.irecv()
    sender = binascii.hexlify(sender, ":").decode().upper()
    data = data.decode()
    print(f"{sender} -> {data}")

e.irq(receive_cb)
