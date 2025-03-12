from machine import Pin, I2C
import _thread
import time
import mem_used

ADDRESS = const(0x38)

class FT6336():
    
    def __init__(self, i2c, period = 0, callback = None):
        self.i2c = i2c
        if callback:
            _thread.start_new_thread(self.task, (period, callback))
        
    def read(self):
        buffer = self.i2c.readfrom_mem(ADDRESS, 0x03, 4)
        x = ((buffer[0] & 0x0F) << 8) | buffer[1]
        y = ((buffer[2] & 0x0F) << 8) | buffer[3]
        pressed = (buffer[0] & 0b11000000 == 0x80)
        return x, y, pressed
            
    def task(self, period, callback):
        time.sleep_ms(period)
        prev = False
        
        while True:
            result = self.read()
            if result[2]:
                prev = True
                callback(result)
            elif prev and not result[2]:
                prev = False
                callback(result)
            time.sleep_ms(period)

if __name__ == "__main__":
    def debug(result_tuple):
        x, y, pressed = result_tuple
        print(f"{x:3d} {y:3d} {pressed}")
    
    i2c = I2C(0) # use default pinout and clock frequency
    print(i2c)   # print pinout and clock frequency
    
    #ft6336 = FT6336(i2c)
    ft6336 = FT6336(i2c, 100, debug)
    
    mem_used.print_ram_used()