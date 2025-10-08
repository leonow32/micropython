# MicroPython 1.24.1 ESP32-S3 Octal SPIRAM

import _thread
import esp32
import gc
import neopixel
import socket
import sys
import time
import wifi_ap
from machine import Pin


def index_html():
    #gc.collect()
    
    with open("index.html", encoding="utf-8") as file:
        content = file.read()  
    
    content = content.replace("AA", str(esp32.mcu_temperature()))
    #content = content.replace("BBB", str(ap.status("rssi")))
    
    if led[0] == (0x10, 0x00, 0x00):
        color = "Czerwony"
    elif led[0] == (0x10, 0x10, 0x00):
        color = "Żółty"
    elif led[0] == (0x00, 0x10, 0x00):
        color = "Zielony"
    elif led[0] == (0x00, 0x10, 0x10):
        color = "Błękitny"
    elif led[0] == (0x00, 0x00, 0x10):
        color = "Niebieski"
    elif led[0] == (0x10, 0x00, 0x10):
        color = "Fioletowy"
    elif led[0] == (0x10, 0x10, 0x10):
        color = "Biały"
    else:
        color = "Czarny"
    
    content = content.replace("CCCCCCCCC", color)
    
    return content

def task():
    #sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock = socket.socket()
    
#     try:
#         sock.bind(('', 80))
#     except:
#         pass
    sock.bind(("", 80))
    
    #sock.listen(5)
    sock.listen()
    
    #sock.setblocking(False)
    
    while True:
        try:
            gc.collect()
            
            conn, addr = sock.accept()
            #conn.settimeout(3.0)
            
            request = conn.recv(1024)
            #conn.settimeout(None)
            
            if request == b"":
                print(f"HTTP - from {addr[0]} EMPTY request")
                conn.send("HTTP/1.1 400 Bad Request\r\n")
                conn.send("Connection: close\r\n")
                conn.send("\r\n")
                conn.close()
                continue
            
            # Zapisz tylko pierwszą linię zapytania, a resztę odrzuć
            request = request.splitlines()[0]
            print(f"HTTP - from {addr[0]} request {request}")
            
            # Prepare response
            print("HTTP - response: ", end="")
            
            if (b"GET / HTTP" in request):
                conn.send("HTTP/1.1 307 Temporary Redirect\r\n")
                conn.send(f"Location: http://{wifi_ap.get_ip()}/index.html\r\n")
                conn.send("Connection: close\r\n")
                conn.send("\r\n")
                
            elif b"index.html " in request:
                print("index.html")
                conn.send("HTTP/1.1 200 OK\r\n")
                conn.send("Content-Type: text/html\r\n")
                conn.send("Connection: close\r\n")
                conn.send("\r\n")
                conn.send(index_html())

            elif b'favicon.ico' in request:
                print("favicon.ico - ignoring")
                conn.send("HTTP/1.1 404 Not Found\r\n")
                conn.send("\r\n")
              
            elif b"color" in request:
                print("color")
                if b"red" in request:
                    led[0] = (0x10, 0x00, 0x00)
                elif b"yellow" in request:
                    led[0] = (0x10, 0x10, 0x00)
                elif b"green" in request:
                    led[0] = (0x00, 0x10, 0x00)
                elif b"cyan" in request:
                    led[0] = (0x00, 0x10, 0x10)
                elif b"blue" in request:
                    led[0] = (0x00, 0x00, 0x10)
                elif b"magenta" in request:
                    led[0] = (0x10, 0x00, 0x10)
                elif b"white" in request:
                    led[0] = (0x10, 0x10, 0x10)
                else:
                    led[0] = (0x00, 0x00, 0x00)
                
                conn.send("HTTP/1.1 200 OK\r\n")
                conn.send("Content-Type: text/html\r\n")
                conn.send("Connection: close\r\n")
                conn.send("\r\n")
                conn.send(index_html())
                
                led.write()
                
            elif b'connectivitycheck' in request:
                print("Connectivity check")
                conn.send("HTTP/1.1 204 No Content\r\n")
                conn.send("\r\n")
                
            else:
                print("Unknown request")
                conn.send("HTTP/1.1 307 Temporary Redirect\r\n")
                conn.send(f"Location: http://{wifi_ap.get_ip()}/index.html\r\n")
                conn.send("\r\n")
            
            conn.close()
                       
        except Exception as e:
            #sys.print_exception(e)
            time.sleep_ms(100)

def init():
    global led
    led = neopixel.NeoPixel(Pin(38, Pin.OUT), 1)
    led[0] = (0, 0, 0)
    led.write()
    
    _thread.start_new_thread(task, [])
