import _thread
import esp32
import gc
import neopixel
import network
import socket
import sys
import time
from machine import Pin
from config import ssid, password

led = neopixel.NeoPixel(Pin(38, Pin.OUT), 1)
led[0] = (0, 0, 0)
led.write()

def led_task(gpio_num, delay_ms):
    led = Pin(gpio_num, Pin.OUT)
    
    while True:  
        led(not led())
        time.sleep_ms(delay_ms)

def wifi_connect():
    global station
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

def index_html():
    print("-- index.html")
    gc.collect()
    content = ""
    #content = "HTTP/1.1 200 OK\r\nContent-Type: text/HTML\r\nConnection: close\r\n\r\n"
    with open("index.html", encoding="utf-8") as file:
        content += file.read()  
    
    content = content.replace("AA", str(esp32.mcu_temperature()))
    content = content.replace("BBB", str(station.status("rssi")))
    
    if led[0] == (0x40, 0x00, 0x00):
        color = "Czerwony"
    elif led[0] == (0x40, 0x40, 0x00):
        color = "Żółty"
    elif led[0] == (0x00, 0x40, 0x00):
        color = "Zielony"
    elif led[0] == (0x00, 0x40, 0x40):
        color = "Błękitny"
    elif led[0] == (0x00, 0x00, 0x40):
        color = "Niebieski"
    elif led[0] == (0x40, 0x00, 0x40):
        color = "Fioletowy"
    elif led[0] == (0x40, 0x40, 0x40):
        color = "Biały"
    else:
        color = "Czarny"
    
    content = content.replace("CCCCCCCCC", color)
    
    return content

def task():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    sock.bind(("", 80))
#     try:
#         sock.bind(("", 80))
#     except:
#         pass
    sock.listen()
    #sock.listen(5)
    #sock.setblocking(False)
    #sock.setblocking(True)
    
    while True:
        try:
            gc.collect()
            
            # Pause here and wait for any request
            conn, addr = sock.accept()
            
            #conn.settimeout(3.0)
            #conn.settimeout(0)
            #conn.settimeout(None)
            request = conn.recv(1024)
            #conn.settimeout(None)
            
            if request == b"":
                print("Empty request")
                continue
            
            # Save only the first line of the request
            request = request.splitlines()[0]
            print(f"-- HTTP Request from {addr[0]}: {request}")
            #print(request)
            
            # Prepare response
            print("-- HTTP Response: ", end="")
            
            if (b"GET / HTTP" in request):
                response = index_html()
                conn.send("HTTP/1.1 200 OK\n")
                conn.send("Content-Type: text/html\n")
                conn.send("Connection: close\n\n")
            
            elif b"index.html " in request:
                response = index_html()
                conn.send("HTTP/1.1 200 OK\n")
                conn.send("Content-Type: text/html\n")
                conn.send("Connection: close\n\n")
                
            elif b"color" in request:
                if b"red" in request:
                    led[0] = (0x40, 0, 0)
                elif b"yellow" in request:
                    led[0] = (0x40, 0x40, 0)
                elif b"green" in request:
                    led[0] = (0, 0x40, 0)
                elif b"cyan" in request:
                    led[0] = (0, 0x40, 0x40)
                elif b"blue" in request:
                    led[0] = (0, 0x0, 0x40)
                elif b"magenta" in request:
                    led[0] = (0x40, 0x00, 0x40)
                elif b"white" in request:
                    led[0] = (0x40, 0x40, 0x40)
                else:
                    led[0] = (0x00, 0x00, 0x00)
                    
                led.write()
                response = index_html()   
                conn.send("HTTP/1.1 200 OK\n")
                conn.send("Content-Type: text/html\n")
                conn.send("Connection: close\n\n")
                
            else:
                print("Unknown request")
                response = "HTTP/1.1 404 Not Found\n"
                conn.send("Connection: close\n\n")
            
            conn.send(response)
            conn.close()
            
        except Exception as e:
            print(f"Exception {e}")
            sys.print_exception(e)
            print("time.sleep_ms(100)", end="")
            time.sleep_ms(100)

def init():
    _thread.start_new_thread(task, ())

if __name__ == "__main__":
    _thread.start_new_thread(led_task, [21, 1000])
    _thread.start_new_thread(led_task, [47, 500])
    _thread.start_new_thread(led_task, [48, 250])
    _thread.start_new_thread(led_task, [45, 100])
    wifi_connect()
    init()

