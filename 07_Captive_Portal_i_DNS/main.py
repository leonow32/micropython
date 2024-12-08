
import _thread
import dns_server
import http_server
import network
import time
from machine import Pin

ip = "192.168.0.1"

def led_task(gpio_num, delay_ms):
    led = Pin(gpio_num, Pin.OUT)
    
    while True:  
        led(not led())
        time.sleep_ms(delay_ms)

def ap_start(ssid):
    global ap
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
        
    # IP address, netmask, gateway, DNS
    ap.ifconfig((ip, "255.255.255.0", ip, ip))
    ap.config(essid=ssid, authmode=network.AUTH_OPEN)
    
#     while not ap.active():
#         print(".", end="")
#         sleep_ms(100)
    
    print(f"Access Point: {ssid} {ap.ifconfig()[0]}")

if __name__ == "__main__":    
    button = Pin(0, Pin.IN, Pin.PULL_UP)
    if button() != 1:   
        _thread.start_new_thread(led_task, [21, 1000])
        _thread.start_new_thread(led_task, [47, 500])
        _thread.start_new_thread(led_task, [48, 250])
        _thread.start_new_thread(led_task, [45, 100])
        
        ap_start("ESP32_HotSpot")
        dns_server.init()
        #http_server.init()
    
