# MicroPython 1.24.1 ESP32-S3 Octal SPIRAM
# v1.0.0 2025.04.04

import time

I2C_ADDRESS = const(0x38)
TIMEOUT     = const(10)

class BMP280():
    """
    Create an object to support BMP280 temperature and humidity sensor.
    - i2c: instance of I2C object.
    """
    
    def __init__(self, i2c):
        time.sleep_ms(40)
        self.i2c = i2c
        self.i2c.writeto(I2C_ADDRESS, b"\xBE\x08\x00")
        time.sleep_ms(10)
        
    def __str__(self):
        return f"BMP280({str(self.i2c)})"
    
    def status_get(self):
        """
        Return status byte.
        - Bit 7: measurement in progress.
        - Bit 3: sensor calibrated.
        """
        buffer = self.i2c.readfrom(I2C_ADDRESS, 1)
        return buffer[0]
    
    def measure(self):
        """
        Start measurement process. After start you need to wait as long as bit 8 of ststur register is high.
        """
        self.i2c.writeto(I2C_ADDRESS, b"\xAC\x33\x00")
    
    def wait_for_ready(self):
        """
        Wait as long as bit 8 of ststur register is high. This function may throw
        ETIMEDOUT exception if memory does not acknowledge in requirewd time, specified
        by TIMEOUT.
        """
        
        timeout = TIMEOUT
        while timeout:
            buffer = self.i2c.readfrom(I2C_ADDRESS, 1)
            if buffer[0] & 0b10000000:
                timeout -= 1;
                time.sleep_ms(10)
                continue
            else:
                return
        
        raise OSError(errno.ETIMEDOUT, "Measurement time expired")
    
    def read(self):
        """
        Reas the result of the measurement. Result is given as a dictionary with "temp" and "humi" keys.
        """
        self.wait_for_ready()
        buffer = self.i2c.readfrom(I2C_ADDRESS, 7)
        
        # Check CRC
        # Initial value of CRC is 0xFF.
        # CRC polynomial is X^8 + X^5 + X^4 + 1 => 0b00110001 (0x31)
        crc = 0xFF
        for byte in buffer[:-1]:
            crc ^= byte
            for i in range(8):
                if crc & 0x80:
                    crc <<= 1
                    crc &= 0xFF
                    crc ^= 0x31
                else:
                    crc <<= 1
                    crc &= 0xFF
        
        if crc != buffer[-1]:
            raise Exception(0, "CRC value incorrect")
        
        # Calculate humidity
        humidity    = (buffer[1] << 12) | (buffer[2] << 4) | ((buffer[3] & 0xF0) >> 4)
        humidity    = (humidity * 100) / (2**20)
        
        # Calculate temperature
        temperature = ((buffer[3] & 0x0F) << 16) | (buffer[4] << 8) | (buffer[5] << 0)
        temperature = (temperature * 200) / (2**20) - 50
        
        return {"temp": temperature, "humi": humidity}

    def reset(self):
        self.i2c.writeto(I2C_ADDRESS, b"\xBA")
    
    def dump(self):
        """
        Read and print all the information.
        """
        status = self.status_get()
        print(f"Busy:        {(status & 0b10000000) >> 7}")
        print(f"Calibrated:  {(status & 0b00001000) >> 3}")
        self.measure()
        result = self.read()
        print(f"Temperature: {result["temp"]} 'C")
        print(f"Humidity:    {result["humi"]} %")
        pass
    
if __name__ == "__main__":
    import mem_used
    import machine
        
    i2c = machine.I2C(0) # use default pinout and clock frequency
    sensor = BMP280(i2c)
    print(sensor)
       
    sensor.dump()
    
    mem_used.print_ram_used()


