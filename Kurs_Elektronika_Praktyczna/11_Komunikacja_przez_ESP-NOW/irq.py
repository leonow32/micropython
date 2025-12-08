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

def recv_cb2(e):
    sender, data = e.irecv()  # Don't wait if no messages left
    sender = binascii.hexlify(sender, ":").decode().upper()
    data = data.decode()
    print(f"{sender} -> {data}")


def recv_cb(e):
    while True:  # Read out all messages waiting in the buffer
        sender, data = e.irecv(0)  # Don't wait if no messages left
        if sender is None:
            print("No more messages")
            return
        print(f"{sender} -> {data}")

e.irq(recv_cb2)