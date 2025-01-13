# MicroPython 1.24.1 ESP32-S3 Octal SPIRAM

import _thread
import time
import mem_used
from machine import Pin

def test_task(text):   
    while True:  
        lock.acquire()
        print(f"{time.ticks_ms()} - {text}")
        lock.release()
        #time.sleep_ms(1000)
        

lock = _thread.allocate_lock()
_thread.start_new_thread(test_task, ["."])
_thread.start_new_thread(test_task, ["X"])

#mem_used.print_ram_used()
