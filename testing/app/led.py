from machine import Pin
import app.config as config

red_pin = None;
grn_pin = None;
led_inverted = None

def init():
    global led_inverted
    led_inverted = config.get("led-inverted")
    global red_pin
    red_pin = config.get("pin-red")
    red_pin = Pin(red_pin, Pin.OUT)
    red_pin(1 if led_inverted else 0)
    global grn_pin
    grn_pin = config.get("pin-grn")
    grn_pin = Pin(grn_pin, Pin.OUT)
    grn_pin(1 if led_inverted else 0)
    
def set_red(val):
    global red_pin
    if val == 1:
        red_pin(0 if led_inverted else 1)
    else:
        red_pin(1 if led_inverted else 0)
        
def get_red():
    global red_pin
    if red_pin.value() == 1:
        return 0 if led_inverted else 1
    else:
        return 1 if led_inverted else 0

def set_grn(val):
    global grn_pin
    if val == 1:
        grn_pin(0 if led_inverted else 1)
    else:
        grn_pin(1 if led_inverted else 0)
        
def get_grn():
    global grn_pin
    if grn_pin.value() == 1:
        return 0 if led_inverted else 1
    else:
        return 1 if led_inverted else 0

def set(red, grn, blu):
    global red_pin
    global grn_pin
    if red:
        red_pin(0 if led_inverted else 1)
    else:
        red_pin(1 if led_inverted else 0)
    if grn:
        grn_pin(0 if led_inverted else 1)
    else:
        grn_pin(1 if led_inverted else 0)

if __name__ == "__main__":
    config.init()
    init()