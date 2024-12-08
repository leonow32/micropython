import network

local_ip = "192.168.1.0"

def init(ssid):
    #global ap
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    
    # IP address, netmask, gateway, DNS
    ap.ifconfig((local_ip, "255.255.255.0", local_ip, local_ip))
    ap.config(essid=ssid, authmode=network.AUTH_OPEN)
    
    print(f"Access Point: {ssid} {ap.ifconfig()[0]}")
    
if __name__ == "__main__":
    init("ESP32-S3_HotSpot")