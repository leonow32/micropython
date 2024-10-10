from machine import Pin, Timer
from neopixel import NeoPixel
from random import randint

led = NeoPixel(Pin(38, Pin.OUT), 1)

def timer_interrupt(timer):
    print('-- timer_interrupt --')
    print(timer)
    
    global led
    led[0] = (0, 0, 0)
    led.write()

def button_interrupt(pin):
    print('-- button_interrupt --')
    print(pin)
    
    r = randint(0, 255)
    g = randint(0, 255)
    b = randint(0, 255)
    
    global led
    led[0] = (r, g, b)
    led.write()
    
    print(f'Color: {led[0]}')
    
    Timer(0, mode=Timer.ONE_SHOT, period=2000, callback=timer_interrupt)

if __name__ == "__main__":
    button = Pin(0, Pin.IN, Pin.PULL_UP)
    button.irq(trigger=Pin.IRQ_FALLING, handler=button_interrupt)