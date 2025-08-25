# MicroPython 1.24.1 ESP32-S3 Octal SPIRAM

import _thread
import esp32
import gc
import neopixel
import network
import socket
import sys
import time
import wifi_config
from machine import Pin

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
        station.connect(wifi_config.ssid, wifi_config.password)
        while not station.isconnected():
            print(".", end="")
            time.sleep_ms(250)
        print()    
    
    global ip
    ip = station.ifconfig()[0]
    print(f"Adres IP: {ip}")

def index_html():
    gc.collect()
    content = ""
    with open("index.html", encoding="utf-8") as file:
        content += file.read()
    
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
    
    content = content.replace("AA", str(esp32.mcu_temperature()))
    content = content.replace("BBB", str(station.status("rssi")))
    content = content.replace("CCCCCCCCC", color)
    
    return content

def task():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("", 80))
    sock.listen()
    
    while True:
        try:
            gc.collect()
            
            # Pause here and wait for any request
            conn, addr = sock.accept()
            request = conn.recv(1024)
            
            # Response for empty request
            if request == b"":
                conn.send("HTTP/1.1 400 Bad Request\r\n")
                conn.send("Connection: close\r\n")
                conn.sendall("\r\n")
                conn.close()
                continue
            
            # Save only the first line of the request
            request = request.splitlines()[0]
            print(f"HTTP Request from {addr[0]}: {request}")
            
            # Prepare response
            if (b"GET / HTTP" in request):
                conn.send(f"HTTP/1.1 307 Temporary Redirect\r\n")
                conn.send(f"Location: http://{ip}/index.html\r\n")
                conn.send("Connection: close\r\n")
                conn.sendall("\r\n")
                
            elif b"index.html " in request:
                conn.send("HTTP/1.1 200 OK\r\n")
                conn.send("Content-Type: text/html\r\n")
                conn.send("Connection: close\r\n")
                conn.send("\r\n")
                conn.sendall(index_html())
                
            elif b"color" in request:
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
                
            else:
                print("Unknown request")
                conn.send("HTTP/1.1 404 Not Found\r\n")
                conn.sendall("\r\n")
            
            conn.close()
            
        except Exception as e:
            sys.print_exception(e)   

led = neopixel.NeoPixel(Pin(38, Pin.OUT), 1)
led[0] = (0, 0, 0)
led.write()
wifi_connect()

_thread.start_new_thread(led_task, [21, 1000])
_thread.start_new_thread(led_task, [47, 500])
_thread.start_new_thread(led_task, [48, 250])
_thread.start_new_thread(led_task, [45, 100])
_thread.start_new_thread(task, ())
