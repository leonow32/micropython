
import aht20
import bmp280
import ds1307
import json
import machine
import mem_used
import ssd1309
import time
from font.galaxy16_digits import *
from font.galaxy24_digits import *

button    = machine.Pin(0, machine.Pin.IN)
i2c       = machine.I2C(0, freq=100000)
display   = ssd1309.SSD1309(i2c)
rtc       = ds1307.DS1307(i2c)
sensor_th = aht20.AHT20(i2c)
sensor_p  = bmp280.BMP280(i2c, 0x77)

sensor_p.config(bmp280.OSRT_T_X16, bmp280.OSRT_P_X16, bmp280.MODE_NORMAL, bmp280.T_SB_05MS, bmp280.FILTER_OFF)

print(i2c)

def increment_counter():
    data = {}
        
    try:
        with open("counter.json") as file:
            data = json.load(file)
    except:
        print("Plik counter.json nie istnieje")
        data["min"] = 0
        data["hrs"] = 0
        data["day"] = 0
        
    data["min"] += 1
    if data["min"] == 60:
        data["min"] = 0
        data["hrs"] += 1
    if data["hrs"] == 24:
        data["hrs"] = 0
        data["day"] += 1

    with open("counter.json", "w") as file:
        json.dump(data, file, separators=(",\n", ":"))

def print_time():
    try:
        rtc.copy_time_to_system()
        rtc.print()
        time_tuple = time.localtime()
        display.fill(0)
        display.print_text(galaxy24_digits, f"{time_tuple[3]}:{time_tuple[4]:02}", 127, 10, "C")
        display.print_text(galaxy16_digits, f"{time_tuple[2]}.{time_tuple[1]:02}.{time_tuple[0]}", 127, 38, "C")
        display.refresh()
    except:
        pass

def print_sensors():
    try:
        sensor_th.measure()
        th = sensor_th.read()
        p  = sensor_p.read()
        
        temp = round(th['temp'], 1)
        humi = round(th['humi'], 1)
        pres = round(p['pres'], 0)
        
        print(f"Temperature: {temp} 'C")
        print(f"Humidity:    {humi} %")
        print(f"Pressure: {pres} hPa")
        
        display.fill(0)
        display.print_text(galaxy16_digits, f"{humi} %",   0,  0, "C")
        display.print_text(galaxy24_digits, f"{temp} 'C",  0, 20, "C")
        display.print_text(galaxy16_digits, f"{pres} hPa", 0, 48, "C")
        display.refresh()
    except:
        pass

if button():
    while True:
        
        increment_counter()
        
        print_sensors()
        time.sleep_ms(10)
        machine.lightsleep(20_000)
        
        print_time()
        time.sleep_ms(10)
        machine.lightsleep(40_000)
        
        #mem_used.print_ram_used()
        #time.sleep(60)
#         time.sleep_ms(10)
#         machine.lightsleep(60_000)
else:
    print("Exit")
