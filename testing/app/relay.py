from machine import Pin
import app.config as config

relay_pin = None;

def init():
    global relay_pin
    relay_pin = config.get("pin-relay")
    relay_pin = Pin(relay_pin, Pin.OUT)
    relay_pin(0)
    
def set(state):
    global relay_pin
    relay_pin(state)
    
def get():
    global relay_pin
    state = relay_pin.value()
    return state

def toggle():
    global relay_pin
    if relay_pin.value():
        relay_pin(0)
    else:
        relay_pin(1)

if __name__ == "__main__":
    config.init()
    init()