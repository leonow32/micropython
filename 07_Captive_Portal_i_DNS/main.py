import _thread
import dns_server
import http_server
import network
import time
from machine import Pin

ap = 123
ip = "192.168.4.1"

def led_task(gpio_num, delay_ms):
    led = Pin(gpio_num, Pin.OUT)
    
    while True:  
        led(not led())
        time.sleep_ms(delay_ms)

def ap_start(ssid):
    global ap
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
        
    print(f"AP SSID: {ssid}")
    
    # IP address, netmask, gateway, DNS
    ap.ifconfig((ip, "255.255.255.0", ip, ip))
    ap.config(essid=ssid, authmode=network.AUTH_OPEN)
    
    while not ap.active():
        print(".", end="")
        sleep_ms(100)
    
    print('AP Config:', ap.ifconfig()[0])

if __name__ == "__main__":
    _thread.start_new_thread(led_task, [21, 1000])
    _thread.start_new_thread(led_task, [47, 500])
    _thread.start_new_thread(led_task, [48, 250])
    _thread.start_new_thread(led_task, [45, 100])
    ap_start("ESP32_HotSpot")
    http_server.init()
    
    #init()
