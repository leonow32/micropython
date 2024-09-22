import _thread
import app.button as button
import app.config as config
import app.relay as relay
import app.ws2812 as led
from time import sleep_ms

def task():
    previous_state = 0
    initialized = False
    
    while True:
        sleep_ms(100)
        
        if not initialized:
            while button.get():
                pass
            led.set(1, 0, 0)
            relay.set(0)
            initialized = True
        
        if button.get() == 1 and previous_state == 0:
            previous_state = 1
            
        if button.get() == 0 and previous_state == 1:
            previous_state = 0
            if relay.get() == 1:
                relay.set(0)
                led.set_red(1)
            else:
                relay.set(1)
                led.set_grn(1)

def init():
    pass

def run_task():
    _thread.start_new_thread(task, ())
    
if __name__ == "__main__":
    config.init()
    button.init()
    led.init()
    led.set(1, 1, 0)
    relay.init()
    init()
    run_task()
