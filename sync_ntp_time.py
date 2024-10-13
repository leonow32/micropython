import network
import ntptime
import time

ssid = "Extronic2.4"
password = "LeonInstruments"

def wifi_connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Connecting to network", end="")
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            print(".", end="")
            time.sleep_ms(250)
        print()    
    
    print(wlan.ifconfig()[0])
    
def download_time():
    ntptime.settime()

def print_local_time():
    time_tuple = time.localtime()
    year    = time_tuple[0]
    month   = time_tuple[1]
    day     = time_tuple[2]
    hours   = time_tuple[3]
    minutes = time_tuple[4]
    seconds = time_tuple[5]
    print(f"{year}.{month:02}.{day:02} {hours:02}:{minutes:02}:{seconds:02}")
    
if __name__ == "__main__":    
    print("Time before sync: ", end="")
    print_local_time()
    wifi_connect()
    download_time()
    print("Time after sync:  ", end="")
    print_local_time()