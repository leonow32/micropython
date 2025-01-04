import mem_used
import neopixel
import random
from machine import Pin, Timer

def timer_interrupt(souce):
    print(f"-- Przerwanie od {souce} --")
    
    global led
    led[0] = (0, 0, 0)
    led.write()

def button_interrupt(souce):
    print(f"-- Przerwanie od {souce} --")
    
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    
    global led
    led[0] = (r, g, b)
    led.write()
    
    print(f"Wylosowany kolor to: {led[0]}")
    
    Timer(0, mode=Timer.ONE_SHOT, period=2000, callback=timer_interrupt)

if __name__ == "__main__":
    global led
    led = neopixel.NeoPixel(Pin(38, Pin.OUT), 1)
    button = Pin(0, Pin.IN, Pin.PULL_UP)
    button.irq(trigger=Pin.IRQ_FALLING, handler=button_interrupt)
    mem_used.print_ram_used()