# MicroPython 1.24.1 ESP32-S3 Octal SPIRAM

import network
import ntptime
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
    
def print_system_time():
    Y, M, D, h, m, s, w, _ = time.localtime()
    days = ["Poniedziałek", "Wtorek", "Środa", "Czwartek", "Piątek", "Sobota", "Niedziela"]
    print(f"{Y}.{M:02}.{D:02} {h:02}:{m:02}:{s:02} {days[w]}")
  
print("Czas przed synchronizacją: ", end="")
print_system_time()
wifi_connect()
ntptime.settime()
print("Czas po synchronizacji:    ", end="")
print_system_time()
