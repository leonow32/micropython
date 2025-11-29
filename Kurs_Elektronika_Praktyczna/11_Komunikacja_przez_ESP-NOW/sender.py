import network
import espnow

# A WLAN interface must be active to send()/recv()
sta = network.WLAN(network.STA_IF)  # Or network.AP_IF
print("MAC Address:", sta.config('mac'))
sta.active(True)

e = espnow.ESPNow()
e.active(True)
#peer = b'\x98\xf4\xab:kl'   # MAC address of peer's wifi interface
peer = b'\xFF\xFF\xFF\xFF\xFF\xFF' # Send to all
e.add_peer(peer)      # Must add_peer() before send()

e.send(peer, "Starting...")
e.send(peer, "Hello 1234567890")
e.send(peer, b'end')