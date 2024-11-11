import network
import socket
import requests
import time

ssid = "Extronic2.4"
password = "LeonInstruments"

def wifi_connect():
    station = network.WLAN(network.STA_IF)
    station.active(True)
    if not station.isconnected():
        print("Łączenie z siecią", end="")
        station.connect(ssid, password)
        while not station.isconnected():
            print(".", end="")
            time.sleep_ms(250)
        print()    
    
    print(f"Adres IP: {station.ifconfig()[0]}")
    
def download_file():
    
    result = requests.get(url="https://retro.hackaday.com")
    result = result.content.decode(encoding="utf-8")
    #if result.code 
    #print(result.content)
    return result

        
if __name__ == "__main__":    

    wifi_connect()
    result = download_file()
   

