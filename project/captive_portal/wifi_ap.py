# MicroPython 1.24.1 ESP32-S3 Octal SPIRAM

import network
import sys

local_ip = "0.0.0.0"

def get_ip():
    return local_ip

def init(ssid):
    #global ap
    ap = network.WLAN(network.WLAN.IF_AP)
    
    
    if sys.platform == "esp32":
        ap.active(True)
        ap.config(essid=ssid, authmode=network.AUTH_OPEN)
    elif sys.platform == "rp2":
        ap.config(essid=ssid)
        ap.config(security=0)
        ap.active(True)
    else:
        raise Exception("Microcontroller not supported")
    
    global local_ip
    local_ip = ap.ifconfig()[0]
    print(f"Access Point: {ssid} {local_ip}")
    
if __name__ == "__main__":
    init("AP Test")
    