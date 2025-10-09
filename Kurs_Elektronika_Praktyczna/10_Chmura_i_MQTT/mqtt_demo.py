# MicroPython 1.24.1 ESP32-S3 Octal SPIRAM

import _thread
import network
import time
import wifi_config
from umqtt.robust import MQTTClient

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
       
def mqtt_callback(topic, payload):  
    print(f"{topic} > {payload}")

def listener_task(delay_ms):
    while True:  
        time.sleep_ms(delay_ms)
        client.check_msg()

def send_demo():
    client.publish("0000test", "To jest test wysylania wiadomosci z ESP32")
 
wifi_connect()
client = MQTTClient(client_id="My-ESP32-S3", server="test.mosquitto.org")  
client.set_callback(mqtt_callback)  
client.connect()  
client.subscribe("0000test")
client.subscribe("0000test/qwerty")

print("Oczekiwanie na wiadomości z MQTT")
_thread.start_new_thread(listener_task, [1000])
    
