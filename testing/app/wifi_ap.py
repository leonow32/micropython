import network
from time import sleep_ms
import app.config as config

ap = None
local_ip = "192.168.4.1"

def init():
    global ap
    ap = network.WLAN(network.AP_IF)
    ap.active(True)

    name = config.get("name")
    mac = ap.config('mac')
    mac_str = ""
    for byte in mac:
        mac_str = f"{mac_str}{byte:02X}"
        
    ap_ssid = f"{name} {mac_str}"
    print(f"AP SSID: {ap_ssid}")
    
    # IP address, netmask, gateway, DNS
    ap.ifconfig((local_ip, "255.255.255.0", local_ip, local_ip))
    ap.config(essid=ap_ssid, authmode=network.AUTH_OPEN)
    
    while not ap.active():
        sleep_ms(100)
    
    print('AP Config:', ap.ifconfig()[0])
    
if __name__ == "__main__":
    config.init()
    init()