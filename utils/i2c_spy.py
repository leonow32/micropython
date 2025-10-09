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
#         self.scl.irq(self.scl_irq, machine.Pin.IRQ_FALLING | machine.Pin.IRQ_RISING)
        self.sda.irq(self.sda_irq, machine.Pin.IRQ_FALLING)
        self.scl.irq(self.scl_irq, machine.Pin.IRQ_FALLING)
        self.scl_edge = 0
        
    def sda_irq(self, source):
        if(source()):
            self.sda_rise_cnt += 1
        else:
            self.sda_fall_cnt += 1
#         pass
#         print(source)
#         self.sda_fall_cnt += 1
#         print("D-", end="")
    
    def sda_rising(self, source):
        self.sda_rise_cnt += 1
#         print("D+", end="")
    
    def scl_irq(self, source):
        # Przerwanie od zbocza rosnącego
        if(self.scl_edge):
            self.scl_rise_cnt += 1
            self.scl.irq(self.scl_irq, machine.Pin.IRQ_FALLING)
        
        # Przerwanie od zbocza opadającego
        else:
            self.scl_fall_cnt += 1
            self.scl.irq(self.scl_irq, machine.Pin.IRQ_RISING)

    
    def scl_rising(self, source):
        self.scl_rise_cnt += 1
#         print("C+", end="")
        
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
    data = i2c.readfrom(0x50, 1)
    
    for byte in data:
        print(f"{byte:02X} ", end="")
    print()
    
    spy.debug_print()

if __name__ == "__main__":
    import mem_used
    import sys
    
    if sys.implementation._machine == "Raspberry Pi Pico W with RP2040":
        print(sys.implementation._machine)
        spy_sda = machine.Pin(14)
        spy_scl = machine.Pin(15)
        
        i2c = machine.I2C(0, freq=1000)
        print(i2c)
    else:
        print("Not supported microcontroller")
        spy_sda = machine.Pin(1)
        spy_scl = machine.Pin(2)
    
    spy = SpyI2C(spy_sda, spy_scl)

    mem_used.print_ram_used()
