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

def recv_cb(e):
    while True:  # Read out all messages waiting in the buffer
        mac, msg = e.irecv(0)  # Don't wait if no messages left
        if mac is None:
            return
        print(mac, msg)

e.irq(recv_cb)