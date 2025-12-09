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

#peer = b'\x98\xf4\xab:kl'   # MAC address of peer's wifi interface
peer = b'\xFF\xFF\xFF\xFF\xFF\xFF' # Send to all
e.add_peer(peer)      # Must add_peer() before send()

e.send(peer, "Starting...")
e.send(peer, "Hello 1234567890")
e.send(peer, "end")
