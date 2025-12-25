# MicroPython 1.26.1 ESP32-S3 Octal SPIRAM

import _thread
import esp32
import machine
import network
import time
import wifi_config
import sys
from umqtt.robust import MQTTClient

client_id = machine.unique_id().hex().upper()
print(f"Client ID: {client_id}")

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
       
def mqtt_publish(topic, payload):
    client.publish(f"0000000_Elektronika_Praktyczna/{topic}", payload)

def mqtt_callback(topic, payload):  
    print(f"{topic} > {payload}")

def mqtt_listener_task(delay_ms):
    while True:  
        time.sleep_ms(delay_ms)
        try:
            client.check_msg()
        except Exception as e:
            sys.print_exception(e)
    
def temperature_task(delay_ms):
    while True:
        client.publish(f"0000000_Elektronika_Praktyczna/sensor_{client_id}", str(esp32.mcu_temperature()))
        time.sleep_ms(delay_ms)
 
wifi_connect()
client = MQTTClient(client_id, "test.mosquitto.org")  
client.set_callback(mqtt_callback)  
client.connect()
# client.subscribe("0000000_Elektronika_Praktyczna")
client.subscribe("0000000_Elektronika_Praktyczna/test")
# client.subscribe("0000000_Elektronika_Praktyczna/#")

print("Oczekiwanie na wiadomości z MQTT")
_thread.start_new_thread(mqtt_listener_task, [1000])
_thread.start_new_thread(temperature_task, [5000])
