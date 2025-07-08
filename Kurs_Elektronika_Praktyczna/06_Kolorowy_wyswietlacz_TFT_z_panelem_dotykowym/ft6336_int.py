import machine
# import time

ADDRESS = const(0x38)

EVENT_PRESS   = const(0b00_000000)
EVENT_LIFT    = const(0b01_000000)
EVENT_CONTACT = const(0b10_000000)
EVENT_NONE    = const(0b11_000000)

class FT6336():
    
    def __init__(self, i2c, int_gpio, int_cb):
        self.i2c = i2c
        self.int_cb = int_cb
        self.int_gpio = int_gpio
        self.int_gpio.init(mode=machine.Pin.IN, pull=machine.Pin.PULL_UP)
        self.int_gpio.irq(self.irq_callback, machine.Pin.IRQ_FALLING)
        
    # This function is executed at ever falling edge of INT GPIO 
    def irq_callback(self, source):
        # read X, Y, event
#         x = 0
#         y = 0
#         event = EVENT_NONE
        
        buffer = self.i2c.readfrom_mem(ADDRESS, 0x03, 4)
        x = ((buffer[0] & 0x0F) << 8) | buffer[1]
        y = ((buffer[2] & 0x0F) << 8) | buffer[3]
        event = buffer[0] & 0b11000000
        
        # call the callback
        self.int_cb(x, y, event)

    def read(self):
        buffer = self.i2c.readfrom_mem(ADDRESS, 0x03, 4)
        x = ((buffer[0] & 0x0F) << 8) | buffer[1]
        y = ((buffer[2] & 0x0F) << 8) | buffer[3]
        pressed = (buffer[0] & 0b11000000 == 0x80)
        return x, y, pressed
        
