import _thread
from machine import UART
from time import sleep_ms
import app.config as config

uart = None
voltage = 0
current = 0
power_active = 0
VOLTAGE_COEF = 0
CURRENT_COEF = 0
POWER_COEF   = 0

def init():
    global uart
    global VOLTAGE_COEF
    global CURRENT_COEF
    global POWER_COEF
    VOLTAGE_COEF = config.get("hlw-v")
    CURRENT_COEF = config.get("hlw-i")
    POWER_COEF = config.get("hlw-p")
    tx_pin = config.get("pin-tx")
    rx_pin = config.get("pin-rx")
    uart = UART(1, baudrate=9600, parity=0, tx=tx_pin, rx=rx_pin) # parity even!!!!!

def checksum_calculate(data):
    result = 0;
    for byte in data:
        result = (result + byte) & 0xFF
    result = ~result & 0xFF
    return result

def checksum_verify(data):
    return data[-1] == checksum_calculate(data[:-1])

def read(address):    
    global uart
    buffer_send = bytes([
        0xA5,    # start
        address  # register address in read mode (7th bit = 0)
    ])
    uart.write(buffer_send)
    sleep_ms(50)

    buffer_recv = uart.read()
    buffer = buffer_send + buffer_recv
    
    if checksum_verify(buffer):
        return buffer_recv[:-1]
    else:
        return "E"
    
def read_voltage():
    try:
        buffer = read(0x26)
        value = buffer[0] * 65536 + buffer[1] * 256 + buffer[2]
        value = value / VOLTAGE_COEF
        return value
    except:
        return -1
    
def get_voltage():
    return voltage

def get_voltage_str():
    if voltage is None:
        return "None"
    else:
        return f"{voltage:.1f}"

def read_current():
    try:
        buffer = read(0x24)
        value = buffer[0] * 65536 + buffer[1] * 256 + buffer[2]
        value = value / CURRENT_COEF
        return value
    except:
        return -1
    
def get_current():
    return current

def get_current_str():
    if current is None:
        return "None"
    else:
        return f"{current:.2f}"

def read_power_active():
    try:
        buffer = read(0x2C)
        value = buffer[0] * 16777216 + buffer[1] * 65536 + buffer[2] * 256 + buffer[3]
        if value > 0xFF000000:
            value = 0
        value = value / POWER_COEF
        return value
    except:
        return -1
    
def get_power_active():
    return power_active

def get_power_active_str():
    if power_active is None:
        return "None"
    else:
        return f"{power_active:.2f}"

def task():
    global voltage
    global current
    global power_active
    while True:
        temp = read_voltage()
        if temp != -1:
            voltage = temp
        sleep_ms(300)
        
        temp = read_current()
        if temp != -1:
            current = temp
        sleep_ms(300)
        
        temp = read_power_active()
        if temp != -1:
            power_active = temp
        sleep_ms(300)
        
def debug_print():
    global voltage
    global current
    global power_active
    print(f"Voltage: {voltage} V")
    print(f"Current: {current} A")
    print(f"Power:   {power_active} W")

def run_task():
    _thread.start_new_thread(task, ())
    
if __name__ == "__main__":
    config.init()
    init()
    run_task()