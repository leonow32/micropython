import _thread
import time

ADDRESS = const(0x38)

EVENT_PRESS   = const(0b00_000000)
EVENT_LIFT    = const(0b01_000000)
EVENT_CONTACT = const(0b10_000000)
EVENT_NONE    = const(0b11_000000)

class FT6336():
    
    def __init__(self, i2c, period, callback):
        self.i2c = i2c
        _thread.start_new_thread(self.task, (period, callback))
            
    def task(self, period, callback):
        while True:
            time.sleep_ms(period)
            
            buffer = self.i2c.readfrom_mem(ADDRESS, 0x03, 4)
            x = ((buffer[0] & 0x0F) << 8) | buffer[1]
            y = ((buffer[2] & 0x0F) << 8) | buffer[3]
            event = buffer[0] & 0b11000000
            
            callback(x, y, event)
