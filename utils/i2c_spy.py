import machine
import time

STATE_INIT = const(0)
STATE_IDLE = const(1)

class SpyI2C():
    
    def __init__(self, sda_pin, scl_pin):
        self.sda = sda_pin
        self.scl = scl_pin
        self.state = STATE_INIT
        
        self.sda_fall_cnt = 0
        self.sda_rise_cnt = 0
        self.scl_fall_cnt = 0
        self.scl_rise_cnt = 0
        
        self.sda.init(mode=machine.Pin.IN, pull=machine.Pin.PULL_UP)
        self.scl.init(mode=machine.Pin.IN, pull=machine.Pin.PULL_UP)
        
        # Tutaj trzeba sprawdzic czy w chwili inicjalizacji linia SDA i SCL sa w stanie wysokim
            
        # W tym momencie SDA i SCL są w stanie wysokim
        self.state = STATE_IDLE
#         self.sda.irq(self.sda_irq, machine.Pin.IRQ_FALLING | machine.Pin.IRQ_RISING)
        self.scl.irq(self.scl_irq, machine.Pin.IRQ_FALLING | machine.Pin.IRQ_RISING)
#         self.sda.irq(self.sda_irq, machine.Pin.IRQ_FALLING)
#         self.scl.irq(self.scl_irq, machine.Pin.IRQ_FALLING)
        self.scl_edge = 0
        
    def sda_irq(self, source):
        if(source()):
            self.sda_rise_cnt += 1
        else:
            self.sda_fall_cnt += 1
    
    def scl_irq(self, source):
        # Przerwanie od zbocza rosnącego
        if(self.scl_edge):
            self.scl_edge = 0
            self.scl_rise_cnt += 1
            self.scl.irq(self.scl_irq, machine.Pin.IRQ_FALLING)
        
        # Przerwanie od zbocza opadającego
        else:
            self.scl_edge = 1
            self.scl_fall_cnt += 1
            self.scl.irq(self.scl_irq, machine.Pin.IRQ_RISING)
        
    def debug_print(self):
        print(f"SDA rise {self.sda_rise_cnt:2d}, fall {self.sda_fall_cnt:2d}")
        print(f"SCL rise {self.scl_rise_cnt:2d}, fall {self.scl_fall_cnt:2d}")
        
    def debug_clear(self):
        self.sda_fall_cnt = 0
        self.sda_rise_cnt = 0
        self.scl_fall_cnt = 0
        self.scl_rise_cnt = 0
        
    def time_print(self):
        Y, M, D, h, m, s, _, _ = time.gmtime()
        print(f"{Y}.{M:02}.{D:02} {h:02}:{m:02}:{s:02}")

def test():
    spy.debug_clear()
    i2c.writeto(0x3C, b"\xFF")

    time.sleep_ms(100)
    spy.debug_print()

if __name__ == "__main__":
    import mem_used
    import sys
    
    print(sys.implementation._machine)
    print(sys.platform)
    
    if "rp2" == sys.platform:
        spy_sda = machine.Pin(14)
        spy_scl = machine.Pin(15)
        i2c = machine.I2C(0, freq=1000)
    elif "ESP32S3" in sys.implementation._machine:
        raise Exception("Not ready")
    elif "ESP32" in sys.implementation._machine:
        spy_sda = machine.Pin(25)
        spy_scl = machine.Pin(26)
        i2c = machine.I2C(0, sda=machine.Pin(19), scl=machine.Pin(18), freq=5_000)
    else:
        raise Exception("Microcontroller not supported")
    
    print(i2c)
    
    spy = SpyI2C(spy_sda, spy_scl)
    test()

    mem_used.print_ram_used()
