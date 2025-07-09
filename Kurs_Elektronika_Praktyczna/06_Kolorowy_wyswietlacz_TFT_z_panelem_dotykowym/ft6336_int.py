import machine

ADDRESS = const(0x38)

EVENT_PRESS   = const(0b00_000000)
EVENT_LIFT    = const(0b01_000000)
EVENT_CONTACT = const(0b10_000000)
EVENT_NONE    = const(0b11_000000)

class FT6336():
    
    def __init__(self, i2c, int_gpio, int_cb):
        self.i2c = i2c
        self.int_cb = int_cb
        int_gpio.init(mode=machine.Pin.IN, pull=machine.Pin.PULL_UP)
        int_gpio.irq(self.irq_callback, machine.Pin.IRQ_FALLING)
        
    def irq_callback(self, source):
        buffer = self.i2c.readfrom_mem(ADDRESS, 0x03, 4)
        x = ((buffer[0] & 0x0F) << 8) | buffer[1]
        y = ((buffer[2] & 0x0F) << 8) | buffer[3]
        event = buffer[0] & 0b11000000
        
        self.int_cb(x, y, event)
