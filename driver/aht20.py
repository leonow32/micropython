# MicroPython 1.24.1 ESP32-S3 Octal SPIRAM
# v1.0.0 2025.04.03

import time


I2C_ADDRESS = const(0x38)
CMD_INIT  = const(0b1011_1110) # 0xBE
CMD_TRIG  = const(0b1010_1100) # 0xAC
CMD_RESET = const(0b1011_1010) # 0xBA
TIMEOUT   = const(10)

def print_hex(buffer):
    for byte in buffer:
        print(f"{byte:02X} ", end="")
    print()

class AHT20():
    """
    Create an object to support AHT temperature and humidity sensor.
    - i2c: instance of I2C object.
    """
    
    def __init__(self, i2c):
        time.sleep_ms(40)
        self.i2c = i2c
        self.i2c.writeto(I2C_ADDRESS, b"\xBE\x08\x00")
        time.sleep_ms(10)
        
    def __str__(self):
        return f"AHT20({str(self.i2c)})"      
    
    def measure(self):
        self.i2c.writeto(I2C_ADDRESS, b"\xAC\x33\x00")
    
    def wait_for_ready(self):
        timeout = TIMEOUT
        while timeout:
            buffer = self.i2c.readfrom(I2C_ADDRESS, 1)
            if buffer[0] & 0b10000000:
                print("Measurement in progress")
                time.sleep_ms(10)
                timeout -= 1;
                continue
            else:
                return
        
        raise OSError(errno.ETIMEDOUT, "Measurement time expired")
    
    def read(self):
        self.wait_for_ready()
    
        buffer = self.i2c.readfrom(I2C_ADDRESS, 7)
        
        print_hex(buffer)
        
        # Check CRC
        # Initial value of CRC is 0xFF.
        # The CRC polynomial: X^8 + X^5 + X^4 + 1 => 0b00110001 (0x31)
        """
          static uint8_t crc8( uint8_t *data, int len ) {
            // calculate CRC8 (Dallas/Maxim)
            // The initial value of CRC is 0xFF.
            // The CRC polynomial: X^8 + X^5 + X^4 + 1 => 0b00110001 (0x31)
            uint8_t crc = 0xff;
            for ( uint8_t j=0; j < len; j++ ) {
               crc ^= data[j];
               for ( uint8_t i=0; i < 8; i++ ) {
                 if (crc & 0x80) {
                   crc = (crc << 1) ^ 0x31;
                 } else {
                   crc = crc << 1;
                }
              }
            }
            return crc;
          }

        """
        
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
                    
        print(f"CRC = {crc:02X}")
        
        
        # Calculate humidity
        humidity    = (buffer[1] << 12) | (buffer[2] << 4) | ((buffer[3] & 0xF0) >> 4)
        humidity    = (humidity * 100) / (2**20)
        
        # Calculate temperature
        temperature = ((buffer[3] & 0x0F) << 16) | (buffer[4] << 8) | (buffer[5] << 0)
        temperature = (temperature * 200) / (2**20) - 50
        
        print(f"Temperature: {temperature} 'C")
        print(f"Humidity: {humidity} %")
        return

    def reset(self):
        self.i2c.writeto(I2C_ADDRESS, b"\xBA")
    
    def dump(self):
        pass
    
if __name__ == "__main__":
    import mem_used
    import machine
    
    def print_hex(buffer):
        for byte in buffer:
            print(f"{byte:02X} ", end="")
        print()
    
    i2c = machine.I2C(0) # use default pinout and clock frequency
    sensor = AHT20(i2c)
    print(sensor)
    
    sensor.measure()
    sensor.read()

    mem_used.print_ram_used()

