import _thread
import app.config as config
from machine import Pin, I2C
from time import sleep_ms

ens210_address  = 0x43
aht20_address = 0x38

i2c = None
temperature = None
humidity = None
temperature_AHT20 = None
humidity_AHT20 = None

def init():
    global i2c
    sda_pin = config.get("pin-sda")
    scl_pin = config.get("pin-scl")
    i2c = I2C(0, scl=Pin(scl_pin), sda=Pin(sda_pin), freq=100000)
    
def crc7(value):
    CRC7POLY = 0x89
    CRC7IVEC = 0x7F
    CRC7WIDTH = 7
    DATA7WIDTH = 17
    DATA7MASK = 0x1FFFF
    DATA7MSB  = 0b10000000000000000
    
    pol = CRC7POLY
    pol = pol << (DATA7WIDTH - CRC7WIDTH - 1)   
    bit = DATA7MSB
    value = (value << CRC7WIDTH)
    bit = (bit << CRC7WIDTH)
    pol = (pol << CRC7WIDTH)
    value |= CRC7IVEC
          
    while bit & (DATA7MASK << CRC7WIDTH):
        if bit & value:
            value = 0xFFFFFFFF & (pol ^ value)
        bit >>= 1        
        pol >>= 1
    return value

def measure():
    # write 03 to register 22
    buffer = bytes([0x22, 0x03])
    i2c.writeto(ens210_address, buffer)
    
    buffer = bytes([0xAC, 0x33, 0x00])
    i2c.writeto(aht20_address, buffer)

def read():
    # read 6 bytes from register 30
    buffer = bytes([0x30])
    i2c.writeto(ens210_address, buffer)
    buffer = i2c.readfrom(ens210_address, 6)
    
    t_val = (buffer[2] << 16) + (buffer[1] << 8) + (buffer[0])
    t_data = (t_val>>0 ) & 0xffff
    t_valid= (t_val>>16) & 0x1
    t_crc = (t_val>>17) & 0x7f
    t_payl = (t_val>>0 ) & 0x1ffff
    
    if t_valid != 1:
        raise OSError("Data not valid")
    
    if t_crc != crc7(t_payl):
        raise OSError("Wrong CRC")
    
    global temperature
    temperature = t_data / 64 - 273.15
    
    h_val= (buffer[5]<<16) + (buffer[4]<<8) + (buffer[3]<<0)
    h_data = (h_val>>0 ) & 0xffff
    h_valid= (h_val>>16) & 0x1
    h_crc = (h_val>>17) & 0x7f
    h_payl = (h_val>>0 ) & 0x1ffff
    
    if h_valid != 1:
        raise OSError("Data not valid")
    
    if h_crc != crc7(h_payl):
        raise OSError("Wrong CRC")
    
    global humidity
    humidity = h_data / 512
    
    # AHT20
    buffer = i2c.readfrom(aht20_address, 7)
    global temperature_AHT20
    temperature_AHT20 = ((buffer[3] & 0x0F) << 16) | (buffer[4] << 8) | (buffer[5] << 0)
    temperature_AHT20 = (temperature_AHT20 * 200) / (2**20) - 50
    global humidity_AHT20
    humidity_AHT20    = (buffer[1] << 12) | (buffer[2] << 4) | ((buffer[3] & 0xF0) >> 4)
    humidity_AHT20    = (humidity_AHT20 * 100) / (2**20)

def task():
    mode = True
    while True:
        sleep_ms(500)
        if mode:
            measure()
            mode = False
        else:
            read()
            mode = True
        
def get_temperature():
    return temperature
    
def get_temperature_str():
    if temperature is None:
        return "None"
    else:
        return f"{temperature:.1f}"
    
def get_temperature_AHT20_str():
    if temperature_AHT20 is None:
        return "None"
    else:
        return f"{temperature_AHT20:.1f}"

def get_humidity():
    return humidity

def get_humidity_str():
    if humidity is None:
        return "None"
    else:
        return f"{humidity:.1f}"
    
def get_humidity_AHT20_str():
    if humidity_AHT20 is None:
        return "None"
    else:
        return f"{humidity_AHT20:.1f}"

def run_task():
    _thread.start_new_thread(task, ())
    
if __name__ == "__main__":
    config.init()
    init()
    run_task()
