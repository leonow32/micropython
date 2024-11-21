import _thread
import gc
import network
import socket
import sys
import time
from machine import Pin

ssid = "Extronic2.4"
password = "LeonInstruments"

def led_task(gpio_num, delay_ms):
    led = Pin(gpio_num, Pin.OUT)
    
    while True:  
        led(not led())
        time.sleep_ms(delay_ms)

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

def style_css():
    print("-- style.css")
    gc.collect()
    
    content = ""
    with open("style.css") as file:
        content = file.read()
    
    return content

def index_html():
    print("-- index.html")
    gc.collect()
    content = ""
    
    with open("index.html") as file:
        content = file.read()
        
    
        
    
    return content

def test_txt():
    print("-- test.txt")
    gc.collect()
    content = "To jest plik test.txt"
    return content

def time_txt():
    print("-- time.txt")
    content = f"""
HTTP/1.1 200 OK
Content-Type: text/plain
Connection: close

Teraz jest czas
{str(time.ticks_ms())}
ms
        
    """
    #content = str(time.ticks_ms())
    return content

def time_html():
    print("-- time.html")
    content = f"""
HTTP/1.1 200 OK
Content-Type: text/html
Connection: close

Teraz jest czas
{str(time.ticks_ms())}
ms

    """
    #content = str(time.ticks_ms())
    return content

# czy to potrzebne?
def parse_params(data):
    print("parse_params()")
    parameters = {}
    
    # Remove everything before '?'
    temp = data.find(b'?') + 1
    data = data[temp:]
    
    # Remove everything after ' '
    temp = data.find(b' ')
    data = data[:temp]
    
    # Split lines
    data = data.split(b'&')
    
    for item in data:
        temp = item.split(b'=')
        temp[0] = temp[0].decode()
        temp[1] = temp[1].decode()
        parameters[temp[0]] = temp[1]
        print(f"{temp[0]} = {temp[1]}")
    
    return parameters

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
            
            # Save only the first line of the request
            print(f"-- HTTP Request from {addr[0]}: {request[0:60]}")
            #print(request)
            
            # Prepare response
            print("-- HTTP Response: ", end="")
            
            if (b"GET / HTTP" in request):
                response = index_html()
                
            elif b"style.css" in request:
                response = style_css()
            
            elif b"index.html" in request:
                response = index_html()
            
            elif b"test.txt" in request:
                response = test_txt()
                
            elif b"time.txt" in request:
                response = time_txt()
                
            elif b"time.html" in request:
                response = time_html()
            
            #elif b"favicon.ico" in request:
            #    response = "favicon"
                
            else:
                print("Unknown request")
                response = "HTTP/1.1 404 Not Found\r\n"
                #global local_ip
                #response = f"HTTP/1.1 307 Temporary Redirect\r\nLocation: http://{local_ip}/index.html\r\n\r\n"
            
            #conn.send("HTTP/1.1 200 OK\n")
            #conn.send("Content-Type: text/plain\n")
            #conn.send("Connection: close\n\n")
            conn.send(response)
            conn.close()
                       
        except Exception as e:
            print(f"Exception {e}")
            sys.print_exception(e)
            print("time.sleep_ms(100)", end="")
            time.sleep_ms(100)

def init():
    pass

def run_task():
    _thread.start_new_thread(task, ())

if __name__ == "__main__":
    _thread.start_new_thread(led_task, [21, 1000])
    _thread.start_new_thread(led_task, [47, 500])
    _thread.start_new_thread(led_task, [48, 250])
    _thread.start_new_thread(led_task, [45, 100])
    wifi_connect()
    #simple()
    run_task()

