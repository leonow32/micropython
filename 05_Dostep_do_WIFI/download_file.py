import network
import requests
import time
from config import ssid, password

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
    
def download_file(url):
    print(f"dowanload_file({url})")
    result = requests.get(url)

    if result.status_code == 200:
        lines = result.text.splitlines()
        for line in lines:
            print(line)
    else:
        print(f"Error {result.status_code}")
        
if __name__ == "__main__":    

    wifi_connect()
    #result = download_file("https://retro.hackaday.com/about.html")
    #result = download_file("https://ep.com.pl/robots.txt")
    result = download_file("https://raw.githubusercontent.com/leonow32/micropython_kurs/refs/heads/main/09_Kolorowy_wyswietlacz_TFT_z_panelem_dotykowym/ft6336.py")
   

