import _thread
from machine import Pin
from neopixel import NeoPixel
import app.config as config
from time import sleep_ms

np = None;
led_request_red = False
led_request_grn = False

def task():
    while True:
        global led_request_red
        if led_request_red:
            led_request_red = False
            global np
            np[0] = (255, 0, 0)
            np.write()
            
        global led_request_grn
        if led_request_grn:
            led_request_grn = False
            global np
            np[0] = (0, 255, 0)
            np.write()
            
        sleep_ms(250)
            
def init():
    pin = config.get("pin-ws2812")
    gpio = Pin(pin, Pin.OUT)
    global np
    np = NeoPixel(gpio, 1)
    np[0] = (0, 0, 0)
    np.write()
    
def run_task():
    _thread.start_new_thread(task, ())
    
def set_red(val):
    global np
    if val == 1:
        np[0] = (255, 0, 0)
    else:
        np[0] = (0, 0, 0)
    np.write() 
        
def get_red():
    global np
    if np[0][0] > 0:
        return 1
    else:
        return 0

def set_grn(val):
    global np
    if val == 1:
        np[0] = (0, 255, 0)
    else:
        np[0] = (0, 0, 0)
    np.write() 
        
def get_grn():
    global np
    if np[0][1] > 0:
        return 1
    else:
        return 0
    
def set(red, grn, blu):
    if red == 1:
        global led_request_red
        led_request_red = True
        
        #red = 255
    if grn == 1:
        global led_request_grn
        led_request_grn = True
        
    """
        grn = 255
    if blu == 1:
        blu = 255
    global np
    np[0] = (red, grn, blu)
    np.write()
    """

if __name__ == "__main__":
    config.init()
    init()
