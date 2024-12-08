import _thread
import esp32
import gc
import neopixel
import socket
import time

from machine import Pin
from app.wifi_ap import local_ip

led = neopixel.NeoPixel(Pin(38, Pin.OUT), 1)
led[0] = (0, 0, 0)
led.write()

def led_task(gpio_num, delay_ms):
    led = Pin(gpio_num, Pin.OUT)
    
    while True:  
        led(not led())
        time.sleep_ms(delay_ms)

def index_html():
    gc.collect()
    content = ""
    
    with open("index.html", encoding="utf-8") as file:
        content += file.read()  
    
    #content = content.replace("AA", str(esp32.mcu_temperature()))
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
    
    sock.setblocking(False)
    
    while True:
        try:
            gc.collect()
            
            conn, addr = sock.accept()
            conn.settimeout(3.0)
            
            request = conn.recv(1024)
            conn.settimeout(None)
            
            if request == b"":
                conn.send("HTTP/1.1 400 Bad Request\r\n")
                conn.send("Connection: close\r\n")
                conn.send("\r\n")
                conn.close()
                continue
            
            # Save only the first line of the request
            #request = request.split(b'\r\n')
            #print(f"HTTP Request from {addr[0]}: {request[0]}")
            request = request.splitlines()[0]
            print(f"HTTP Request from {addr[0]}: {request}")
            
            # Prepare response
            print("HTTP Response: ", end="")
            
            if (b"GET / HTTP" in request):
                conn.send(f"HTTP/1.1 307 Temporary Redirect\r\n")
                conn.send(f"Location: http://{local_ip}/index.html\r\n")
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
                response = index_html()
                conn.sendall(response)
                
                led.write()
                
            elif b'connectivitycheck' in request:
                print("Connectivity check")
                #response = b"HTTP/1.1 204 No Content\r\n\r\n"
                conn.send("HTTP/1.1 204 No Content\r\n")
                conn.send("\r\n")
                
            else:
                #print("Unknown request")
                #response = "HTTP/1.1 404 Not Found\r\n"
                #global local_ip
                #response = f"HTTP/1.1 307 Temporary Redirect\r\nLocation: http://{local_ip}/index.html\r\n\r\n"
                print("Unknown request")
                conn.send("HTTP/1.1 307 Temporary Redirect\r\n")
                conn.send(f"Location: http://{local_ip}/index.html\r\n")
                conn.send("\r\n")
            
            #conn.sendall(response)
            conn.close()
                       
        except:
            time.sleep_ms(100)

def init():
    _thread.start_new_thread(led_task, [21, 1000])
    _thread.start_new_thread(led_task, [47, 500])
    _thread.start_new_thread(led_task, [48, 250])
    _thread.start_new_thread(led_task, [45, 100])
    _thread.start_new_thread(task, [])

if __name__ == "__main__":
    init()

