# MicroPython 1.24.1 ESP32-S3 Octal SPIRAM

import network
import requests
import time
import wifi_config

def wifi_connect():
    station = network.WLAN(network.STA_IF)
    station.active(True)
    if not station.isconnected():
        print("Łączenie z siecią", end="")
        station.connect(wifi_config.ssid, wifi_config.password)
        while not station.isconnected():
            print(".", end="")
            time.sleep_ms(250)
        print()    
    
    print(f"Adres IP: {station.ifconfig()[0]}")
    
def download_file(url):
    result = requests.get(url)

    if result.status_code == 200:
        return result.text
    else:
        return f"Error {result.status_code}"
        
if __name__ == "__main__":    
    wifi_connect()
    data = download_file("https://raw.githubusercontent.com/leonow32/micropython/refs/heads/main/Kurs_Elektronika_Praktyczna/05_Wyswietlacz_OLED/ssd1309.py")
    print(data)
