from machine import Pin
import app.config as config

button_pin = None

def init():
    global button_pin
    button_pin = config.get("pin-button")
    button_pin = Pin(button_pin, Pin.IN, Pin.PULL_UP)
    
def get():
    global button_pin
    if button_pin.value():
        return 0
    else:
        return 1
    
if __name__ == "__main__":
    config.init()
    init()
