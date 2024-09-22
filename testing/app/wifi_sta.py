import app.config as config

from gc import collect
from time import sleep_ms
import network

station = None

def get_is_connected():
    global station
    return station.isconnected()

def get_ip_str():
    global station
    return station.ifconfig()[0]

def get_status_str():
    global station
    status = station.status()
    if status == network.STAT_ASSOC_FAIL:
        return "Association failed"
    elif status == network.STAT_BEACON_TIMEOUT:
        return "Beacon timeout"
    elif status == network.STAT_CONNECTING:
        return "Connecting"
    elif status == network.STAT_GOT_IP:
        return "Connected"
    elif status == network.STAT_HANDSHAKE_TIMEOUT:
        return "Handshake timeout"
    elif status == network.STAT_IDLE:
        return "Not connected"
    elif status == 8:
        return "Not connected"
    elif status == network.STAT_NO_AP_FOUND:
        return "Network not found"
    elif status == network.STAT_WRONG_PASSWORD:
        return "Wrong password"
    else:
        return f"Unknown {status}"
    
def get_rssi_str():
    global station
    try:
        return str(station.status("rssi"))
    except:
        return "None"

def init():
    collect()
    
    ssid = config.get("ssid")
    password = config.get("password")
    print(f"STA SSID: {ssid}")
    print(f"STA Password: {password}")
    
    global station
    station = network.WLAN(network.STA_IF)
    station.active(True)
    
    if config.get("mode") == "sta":
        if not station.isconnected():
            station.connect(ssid, password)
        
"""        while not station.isconnected():
            print(".", end="")
            sleep_ms(100)
        print("")
        
    print(f"IP Address:\t{station.ifconfig()[0]}")
"""

def disconnect():
    print("wifi_sta.disconnect())")
    global station
    station.disconnect()
    
if __name__ == "__main__":
    config.init()
    init()