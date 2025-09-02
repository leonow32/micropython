import machine

STATE_INIT = const(0)

class I2C_Observer():
    
    def __init__(self, sda_pin, scl_pin):
        self.sda = sda_pin
        self.scl = scl_pin
        self.state = STATE_INIT
        
        self.sda.init(mode=machine.Pin.IN, pull=machine.Pin.PULL_UP)
        self.scl.init(mode=machine.Pin.IN, pull=machine.Pin.PULL_UP)
        
        # Tutaj trzeba sprawdzic czy w chwili inicjalizacji linia SDA i SCL sa w stanie wysokim
        self.sda.irq(self.sda_falling, machine.Pin.IRQ_FALLING)
        
    def sda_falling(self, source):
        
        pass
    
    def sda_rising(self, source):
        pass
    
    def scl_rising(self, source):
        pass
    
    def scl_falling(self, source):
        pass
        
    
if __name__ == "__main__":
    import mem_used
    
    sda = machine.Pin(1)
    scl = machine.Pin(2)
    
    observer = I2C_Observer(sda, scl)

    mem_used.print_ram_used()
