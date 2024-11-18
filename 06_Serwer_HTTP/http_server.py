import _thread
import gc
import network
import socket
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

def index_html():
    print("index.html")
    gc.collect()
    content = "To jest plik index.html"
    return content

def test_txt():
    print("index.html")
    gc.collect()
    content = "To jest plik index.html"
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

def simple():
    print("simple()")
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.bind(("", 80))
    except:
        pass
    
    
    print("sock.listen(5)")
    sock.listen(5)
    #sock.setblocking(False)
    

    gc.collect()
    
    conn, addr = sock.accept()
    print(f"conn = {conn}")
    print(f"addr = {addr}")
    
    conn.settimeout(3.0)
    
    request = conn.recv(1024)
    print(request)
    
    #conn.settimeout(None)
    
    # Save only the first line of the request
    request = request.split(b'\r\n')
    print(f"HTTP Request from {addr[0]}: {request[0]}")
    print(request)
    
    # Prepare response
    print("HTTP Response: ", end="")
    
    if (b'GET / HTTP' in request[0]) or (b'GET /index.html HTTP' in request[0]):
        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-Type: text/html\n')
        conn.send('Connection: close\n\n')
        response = index_html()
        
    elif b'config.html' in request[0]:
        response = config_html()
        
    elif b'test.txt' in request[0]:
        response = test_txt()
    
    elif b'favicon.ico' in request[0]:
        print("favicon.ico - ignoring")
        response = "favicon"
        
    else:
        print("Unknown request")
        #response = "HTTP/1.1 404 Not Found\r\n"
        global local_ip
        response = f"HTTP/1.1 307 Temporary Redirect\r\nLocation: http://{local_ip}/index.html\r\n\r\n"
    
    conn.sendall(response)
    conn.close()
                       



def task():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.bind(("", 80))
    except:
        pass
    sock.listen(5)
    #sock.setblocking(False)
    
    while True:
        try:
            gc.collect()
            
            conn, addr = sock.accept()
            conn.settimeout(3.0)
            request = conn.recv(1024)
            conn.settimeout(None)
            
            # Save only the first line of the request
            request = request.split(b'\r\n')
            print(f"-- HTTP Request from {addr[0]}: {request[0]}")
            print(request)
            
            # Prepare response
            print("HTTP Response: ", end="")
            
            if (b'GET / HTTP' in request[0]) or (b'GET /index.html HTTP' in request[0]):
                conn.send('HTTP/1.1 200 OK\n')
                conn.send('Content-Type: text/html\n')
                conn.send('Connection: close\n\n')
                response = index_html()
                
            elif b'config.html' in request[0]:
                response = config_html()
                
            elif b'test.txt' in request[0]:
                response = test_txt()
            
            elif b'favicon.ico' in request[0]:
                print("favicon.ico - ignoring")
                response = "favicon"
                
            else:
                print("Unknown request")
                #response = "HTTP/1.1 404 Not Found\r\n"
                global local_ip
                response = f"HTTP/1.1 307 Temporary Redirect\r\nLocation: http://{local_ip}/index.html\r\n\r\n"
            
            conn.sendall(response)
            conn.close()
                       
        except:
            print(".", end="")
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

