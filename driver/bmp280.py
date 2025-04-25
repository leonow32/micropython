# MicroPython 1.24.1 ESP32-S3 Octal SPIRAM
# v1.0.0 2025.04.25

import time

# TIMEOUT     = const(10)

# write nie inkrementuje adresu automatycznie


class BMP280():
    """
    Create an object to support BMP280 temperature and humidity sensor.
    - i2c: instance of I2C object.
    """
    
    def __init__(self, i2c, device_address):
        time.sleep_ms(40)
        self.i2c = i2c
        self.device_address = device_address
#         self.i2c.writeto(device_address, b"\xBE\x08\x00")
#         time.sleep_ms(10)
        
    def __str__(self):
        return f"BMP280({str(self.i2c)})"
    
    def status_get(self):
        """
        Return status byte.
        - Bit 7: measurement in progress.
        - Bit 3: sensor calibrated.
        """
        pass
    
    def measure(self):
        """
        Start measurement process. After start you need to wait as long as bit 8 of ststur register is high.
        """
        pass
    
    def wait_for_ready(self):
        """
        Wait as long as bit 8 of ststur register is high. This function may throw
        ETIMEDOUT exception if memory does not acknowledge in requirewd time, specified
        by TIMEOUT.
        """
        
        pass
    
    def read(self):
        """
        Reas the result of the measurement. Result is given as a dictionary with "temp" and "humi" keys.
        """
        pass
        

    def reset(self):
        pass
    
    def dump(self):
        """
        Read and print all the information.
        """
        pass
    
if __name__ == "__main__":
    import mem_used
    import machine
        
    i2c = machine.I2C(0) # use default pinout and clock frequency
    sensor = BMP280(i2c)
    print(sensor)
       
    sensor.dump()
    
    mem_used.print_ram_used()


