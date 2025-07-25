import machine

ADDRESS = const(0x38)

EVENT_PRESS   = const(0b00_000000)
EVENT_LIFT    = const(0b01_000000)
EVENT_CONTACT = const(0b10_000000)
EVENT_NONE    = const(0b11_000000)

class FT6336():
    
    def __init__(self, i2c, int_gpio, callback):
        self.i2c = i2c
        self.callback = callback
        self.buffer = bytearray(4)
        int_gpio.init(mode=machine.Pin.IN, pull=machine.Pin.PULL_UP)
        int_gpio.irq(self.irq_handler, machine.Pin.IRQ_FALLING)
        
    def irq_handler(self, source):
        self.i2c.readfrom_mem_into(ADDRESS, 0x03, self.buffer)
        x = ((self.buffer[0] & 0x0F) << 8) | self.buffer[1]
        y = ((self.buffer[2] & 0x0F) << 8) | self.buffer[3]
        event = self.buffer[0] & 0b11000000
        
        self.callback(x, y, event)
