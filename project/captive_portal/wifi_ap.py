# MicroPython 1.24.1 ESP32-S3 Octal SPIRAM

import network

local_ip = "0.0.0.0"

def get_ip():
    return local_ip

def init(ssid):
    #global ap
    ap = network.WLAN(network.WLAN.IF_AP)
    ap.active(True)
    ap.config(essid=ssid, authmode=network.AUTH_OPEN)
    
    global local_ip
    local_ip = ap.ifconfig()[0]
    print(f"Access Point: {ssid} {local_ip}")
    
if __name__ == "__main__":
    init("ESP32-S3_HotSpot")
    