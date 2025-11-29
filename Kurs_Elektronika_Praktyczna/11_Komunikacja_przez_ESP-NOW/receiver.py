import network
import espnow
import ubinascii

# A WLAN interface must be active to send()/recv()
sta = network.WLAN(network.STA_IF)
sta.active(True)

e = espnow.ESPNow()
mac = sta.config('mac')
print("MAC Address:", mac)
print(ubinascii.hexlify(mac).decode())
print(f"MAC: {mac!s}")
e.active(True)

while True:
    host, msg = e.recv()
    if msg:             # msg == None if timeout in recv()
        print(host, msg)
        if msg == b'end':
            break