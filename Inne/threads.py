import _thread
import time
import mem_used
from machine import Pin

def led_task(gpio_num, delay_ms):
    led = Pin(gpio_num, Pin.OUT)
    
    while True:  
        led(not led())
        time.sleep_ms(delay_ms)

_thread.start_new_thread(led_task, [21, 1000])
_thread.start_new_thread(led_task, [47, 500])
_thread.start_new_thread(led_task, [48, 250])
_thread.start_new_thread(led_task, [45, 100])

mem_used.print_ram_used()