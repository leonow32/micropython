import _thread
from gc import collect
from time import sleep_ms
from app.wifi_ap import local_ip

import usocket as socket
import app.button as button
import app.config as config
import app.ens210 as ens210
import app.relay as relay
import app.hlw8110 as hlw8110
import app.wifi_sta as wifi_sta
import app.ws2812 as led
#import app.led as led

def index_html():
    print("index.html")
    collect()
    
    content = None
    with open("app/index.html") as file:
        content = file.read()
    
    voltage_str = f"{hlw8110.get_voltage_str()} V"
    current_str = f"{hlw8110.get_current_str()} A"
    power_str = f"{hlw8110.get_power_active_str()} W"
    temperature_str = f"{ens210.get_temperature_str()} &deg;C"
    humidity_str = f"{ens210.get_humidity_str()} %"
    temperature_AHT20_str = f"{ens210.get_temperature_AHT20_str()} &deg;C"
    humidity_AHT20_str = f"{ens210.get_humidity_AHT20_str()} %"
    
    if relay.get() == 0:
        relay_str = "OFF"
        relay_box = "box_red"
    else:
        relay_str = "ON "
        relay_box = "box_grn"
    
    content = content.replace("AAA.A", voltage_str)
    content = content.replace("B.BBB", current_str)
    content = content.replace("CCCC", power_str)
    content = content.replace("DD.D", temperature_str)
    content = content.replace("EE.E", humidity_str)
    content = content.replace("FFF", relay_str)
    content = content.replace("GGGGGGG", relay_box)
    content = content.replace("HH.H", temperature_AHT20_str)
    content = content.replace("II.I", humidity_AHT20_str)
    return content

def config_html():
    print("config.html")
    collect()
    
    content = None
    with open("app/config.html") as file:
        content = file.read()
        
    content = content.replace("AAA", config.get("ssid"))
    content = content.replace("BBB", config.get("password"))
    content = content.replace("CCC", "checked" if (config.get("mode") == "sta") else "")
    content = content.replace("DDD", "checked" if (config.get("mode") == "ap") else "")
    content = content.replace("EEE", wifi_sta.get_status_str())
    content = content.replace("FFF", wifi_sta.get_ip_str())
    content = content.replace("GGG", wifi_sta.get_rssi_str())
    return content

def raw_txt():
    print("raw.txt")
    voltage_str = "{:.1f}".format(hlw8110.get_voltage())
    current_str = "{:.3f}".format(hlw8110.get_current())
    power_str = "{:.2f}".format(hlw8110.get_power_active())
    temperature_str = "{:}".format(ens210.get_temperature_str())
    humidity_str = "{:}".format(ens210.get_humidity_str())
    button_str = "{:}".format(button.get())
    relay_str = "{:}".format(relay.get())
    led_red_str = "{:}".format(led.get_red())
    led_grn_str = "{:}".format(led.get_grn())
    
    content = \
             "Socket GEN4 HV1\r\n" + \
             "Volage:\t\t" + voltage_str + " V \r\n" + \
             "Current:\t" + current_str + " A \r\n" + \
             "Power:\t\t" + power_str + " W \r\n" \
             "Temperature:\t" + temperature_str + " 'C \r\n" + \
             "Humidity:\t" + humidity_str + " % \r\n" + \
             "Button:\t\t" + button_str + " \r\n" + \
             "Relay:\t\t" + relay_str + " \r\n" + \
             "LED red:\t" + led_red_str + " \r\n" + \
             "LED green:\t" + led_grn_str + " \r\n"
    
    return content

def style_css():
    print("style.css")
    collect()
    
    content = None
    with open("app/style.css") as file:
        content = file.read()
    
    return content

def get_data():
    print("get_data() = ", end="")
    if relay.get() == 0:
        relay_str = "OFF|box_red|"
    else:
        relay_str = "ON|box_grn|"
    content = f"{hlw8110.get_voltage_str()} V|"
    content += f"{hlw8110.get_current_str()} A"
    content += f"|{hlw8110.get_power_active_str()} W|"
    content += f"{ens210.get_temperature_str()} &deg;C|"
    content += f"{ens210.get_humidity_str()} %|"
    content += relay_str
    content += f"{ens210.get_temperature_AHT20_str()} &deg;C|"
    content += f"{ens210.get_humidity_AHT20_str()} %|"
    print(content)
    return content

def get_status():
    print("get_status() = ", end="")
    content = f"{wifi_sta.get_status_str()}|{wifi_sta.get_ip_str()}|{wifi_sta.get_rssi_str()}"
    print(content)
    return content

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
    try:
        sock.bind(('', 80))
    except:
        pass
    sock.listen(5)
    sock.setblocking(False)
    
    while True:
        try:
            collect()
            
            conn, addr = sock.accept()
            conn.settimeout(3.0)
            
            request = conn.recv(1024)
            conn.settimeout(None)
            
            # Save only the first line of the request
            request = request.split(b'\r\n')
            print(f"HTTP Request from {addr[0]}: {request[0]}")
            
            # Prepare response
            print("HTTP Response: ", end="")
            
            if (b'GET / HTTP' in request[0]) or (b'GET /index.html HTTP' in request[0]):
                conn.send('HTTP/1.1 200 OK\n')
                conn.send('Content-Type: text/html\n')
                conn.send('Connection: close\n\n')
                response = index_html()
                
            elif b'GET /config.html ' in request[0]:
                response = config_html()
                
            elif b'style.css ' in request[0]:
                response = style_css()
            
            elif b'favicon.ico' in request[0]:
                print("favicon.ico - ignoring")
                response = "favicon"
                
            elif b'raw.txt' in request[0]:
                response = raw_txt()
                
            elif b'?' in request[0]:
                args = parse_params(request[0])
                
                if "relay" in args:
                    if args["relay"] == "on":
                        relay.set(1)
                        led.set(0, 1, 0)
                    if args["relay"] == "off":
                        relay.set(0)
                        led.set(1, 0, 0)
                    response = index_html()
                        
                if "ssid" in args:
                    config.set("ssid", args["ssid"])
                    config.save()
                
                if "password" in args:
                    config.set("password", args["password"])
                    config.save()
                    
                if "mode" in args:
                    config.set("mode", args["mode"])
                    config.save()
                    wifi_sta.disconnect()
                    if config.get("mode") == "sta":
                        wifi_sta.init()
                    response = config_html()
                
            elif b'get_data' in request[0]:
                response = get_data()
                
            elif b'get_status' in request[0]:
                response = get_status()
                
            elif b'connectivitycheck' in request[0]:
                print("Connectivity check")
                response = b"HTTP/1.1 204 No Content\r\n\r\n"
                
            else:
                print("Unknown request")
                #response = "HTTP/1.1 404 Not Found\r\n"
                global local_ip
                response = f"HTTP/1.1 307 Temporary Redirect\r\nLocation: http://{local_ip}/index.html\r\n\r\n"
            
            conn.sendall(response)
            conn.close()
                       
        except:
            sleep_ms(100)

def init():
    pass

def run_task():
    _thread.start_new_thread(task, ())

if __name__ == "__main__":
    config.init()
    button.init()
    ens210.init()
    ens210.run_task()
    relay.init()
    led.init()
    hlw8110.init()
    wifi_sta.init()
    init()

