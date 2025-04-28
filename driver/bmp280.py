# MicroPython 1.24.1 ESP32-S3 Octal SPIRAM
# v1.0.0 2025.04.25

from micropython import const
import struct
import time

# useful registers
REG_ID        = const(0xD0)
REG_RESET     = const(0xE0)
REG_STATUS    = const(0xF3)
REG_CTRL_MEAS = const(0xF4)
REG_CONFIG    = const(0xF5)

# mode setting
MODE_SLEEP    = const(0b00000_00)
MODE_FORCED   = const(0b00000_01)   # single measurement, then sleep
MODE_NORMAL   = const(0b00000_11)   # periodic measurement

# osrs_t setting - temperature oversampling
OSRT_T_SKIP   = const(0b000_00000)
OSRT_T_X1     = const(0b001_00000) # resolution 16 bit (0.0050 'C)
OSRT_T_X2     = const(0b010_00000) # resolution 17 bit (0.0025 'C)
OSRT_T_X4     = const(0b011_00000) # resolution 18 bit (0.0012 'C)
OSRT_T_X8     = const(0b100_00000) # resolution 19 bit (0.0006 'C)
OSRT_T_X16    = const(0b101_00000) # resolution 20 bit (0.0003 'C)

# osrs_p setting - pressure oversampling
OSRT_P_SKIP   = const(0b000_000_00)
OSRT_P_X1     = const(0b000_001_00) # resolution 16 bit (2.62 Pa)
OSRT_P_X2     = const(0b000_010_00) # resolution 17 bit (1.31 Pa)
OSRT_P_X4     = const(0b000_011_00) # resolution 18 bit (0.66 Pa)
OSRT_P_X8     = const(0b000_100_00) # resolution 19 bit (0.33 Pa)
OSRT_P_X16    = const(0b000_101_00) # resolution 20 bit (0.16 Pa)

# t_sb setting - time between sampling
T_SB_05MS     = const(0b000_00000)
T_SB_62MS     = const(0b001_00000)
T_SB_125MS    = const(0b010_00000)
T_SB_250MS    = const(0b011_00000)
T_SB_500MS    = const(0b100_00000)
T_SB_1000MS   = const(0b101_00000)
T_SB_2000MS   = const(0b110_00000)
T_SB_4000MS   = const(0b111_00000)

# filter coefficient
FILTER_OFF    = const(0b000_000_00)
FILTER_2      = const(0b000_001_00)
FILTER_4      = const(0b000_010_00)
FILTER_8      = const(0b000_011_00)
FILTER_16     = const(0b000_100_00)

TIMEOUT_MS    = const(100)

class BMP280():
    """
    Create an object to support BMP280 temperature and humidity sensor.
    - i2c: instance of I2C object.
    - device_address: address of the memory chip on I2C bus.
    """
    
    def __init__(self, i2c, device_address):
        time.sleep_ms(40)
        self.i2c = i2c
        self.device_address = device_address
        
        self.reset()
        self.wait_for_ready()
        
        calib = self.i2c.readfrom_mem(self.device_address, 0x88, 24, addrsize=8)
        self.T1 = struct.unpack("<H", calib[0:2])[0]
        self.T2 = struct.unpack("<h", calib[2:4])[0]
        self.T3 = struct.unpack("<h", calib[4:6])[0]
        self.P1 = struct.unpack("<H", calib[6:8])[0]
        self.P2 = struct.unpack("<h", calib[8:10])[0]
        self.P3 = struct.unpack("<h", calib[10:12])[0]
        self.P4 = struct.unpack("<h", calib[12:14])[0]
        self.P5 = struct.unpack("<h", calib[14:16])[0]
        self.P6 = struct.unpack("<h", calib[16:18])[0]
        self.P7 = struct.unpack("<h", calib[18:20])[0]
        self.P8 = struct.unpack("<h", calib[20:22])[0]
        self.P9 = struct.unpack("<h", calib[22:24])[0]
        
    def __str__(self):
        return f"BMP280({str(self.i2c)}, device_address=0x{self.device_address:02X})"
    
    def status_get(self):
        """
        Return status byte.
        - Bit 3: measurement in progress.
        - Bit 0: calibration data is being copied from NVM.
        """
        return self.i2c.readfrom_mem(self.device_address, REG_STATUS, 1, addrsize=8)[0]
    
    def measure(self):
        """
        Start measurement process. Use it only in forced mode. No need in normaln mode.
        """
        config = self.read_register(REG_CTRL_MEAS)
        config = config & 0b11111100
        config = config | MODE_FORCED
        self.write_register(REG_CTRL_MEAS, config)
    
    def wait_for_ready(self):
        """
        Wait as long as status register is equal to 0. This function may throw
        ETIMEDOUT exception if memory does not acknowledge in requirewd time, specified
        by TIMEOUT.
        """
        timeout = TIMEOUT_MS
        while timeout:
            if (self.status_get() & 0b00000001) == 0:
                return
            else:
                timeout -= 1;
                time.sleep_ms(1)
        
        raise OSError(errno.ETIMEDOUT, "Measurement time expired")
    
    def read(self):
        """
        Reas the result of the measurement. Result is given as a dictionary with "temp" and "pres" keys.
        """
        
        buffer = bytearray(6)
        self.i2c.readfrom_mem_into(self.device_address, 0xF7, buffer, addrsize=8)
        
        raw_pressure = (buffer[0] << 12) | (buffer[1] << 4) | (buffer[2] >> 4)
        raw_temperature = (buffer[3] << 12) | (buffer[4] << 4) | (buffer[5] >> 4)
        
        var1 = (raw_temperature / 16384 - self.T1 / 1024) * self.T2
        var2 = ((raw_temperature / 131072 - self.T1 / 8192) * (raw_temperature / 131072 - self.T1 / 8192)) * self.T3
        t_fine = var1 + var2
        temperature = (var1 + var2) / 5120
        
#         print(f"t_fine = {t_fine}")
#         print(f"temperature = {temperature}")
        
        # pressure
        var1 = (t_fine / 2) - 64000
        var2 = var1 * var1 * self.P6 / 32768
        var2 = var2 + var1 * self.P5 * 2
        var2 = (var2 / 4) + (self.P4 * 65536)
        var1 = (self.P3 * var1 * var1 / 524288 + self.P2 * var1) / 524288
        var1 = (1 + var1 / 32768) * self.P1

        if var1 == 0:
            pressure = 0
#             return 0
        else:
            p = 1048576 - raw_pressure
            p = (p - (var2 / 4096)) * 6250 / var1
            var1 = self.P9 * p * p / 2147483648
            var2 = p * self.P8 / 32768
            p = p + (var1 + var2 + self.P7) / 16

            pressure = p / 100
            
#         print(f"pressure: {pressure}")
        
        return {"temp": temperature, "pres": pressure}
        
    
    def read_register(self, register, length=1):
        return self.i2c.readfrom_mem(self.device_address, register, length, addrsize=8)[0]
    
    def write_register(self, register, value):
        self.i2c.writeto_mem(self.device_address, register, bytes([value]), addrsize=8)

    def config(self, osrs_t, osrs_p, mode, t_sb, filter):
        self.write_register(REG_CTRL_MEAS, osrs_t | osrs_p | mode)
        self.write_register(REG_CONFIG,    t_sb | filter)
    
    def reset(self):
        self.write_register(REG_RESET, 0xB6)
    
    def dump(self):
        """
        Read and print all the information.
        """
        buffer = self.i2c.readfrom_mem(self.device_address, 0x00, 256)
        
        print("     0  1  2  3  4  5  6  7  8  9  A  B  C  D  E  F")
        for i in range(len(buffer)):
            if i % 16 == 0:
                print(f"{i:02X}: ", end = "")
            print(f"{buffer[i]:02X}", end="\n" if i % 16 == 15 else " ")
        
        status = self.status_get()
        print(f"measuring:    {(status & 0b00001000) >> 3}")
        print(f"im_updating:  {(status & 0b00000001) >> 0}")
        
        result = self.read()
        print(f"Temperature: {result["temp"]} 'C")
        print(f"Pressure:    {result["pres"]} hPa")
        
        print(f"T1 = {self.T1}")
        print(f"T2 = {self.T2}")
        print(f"T3 = {self.T3}")
        print(f"P1 = {self.P1}")
        print(f"P2 = {self.P2}")
        print(f"P3 = {self.P3}")
        print(f"P4 = {self.P4}")
        print(f"P5 = {self.P5}")
        print(f"P6 = {self.P6}")
        print(f"P7 = {self.P7}")
        print(f"P8 = {self.P8}")
        print(f"P9 = {self.P9}")
        
    
if __name__ == "__main__":
    import mem_used
    import machine
        
    i2c = machine.I2C(0) # use default pinout and clock frequency
    sensor = BMP280(i2c, 0x77)
    print(sensor)
       
    
    sensor.reset()
    print(f"status: {sensor.status_get():02X}")
    print(f"status: {sensor.status_get():02X}")
    print(f"status: {sensor.status_get():02X}")
    print(f"status: {sensor.status_get():02X}")
    print(f"status: {sensor.status_get():02X}")
#     sensor.dump()
    print(sensor.read())

    
    
    # demo of forced mode
    """
    sensor.config(OSRT_T_X16, OSRT_P_X16, MODE_FORCED, T_SB_05MS, FILTER_OFF)
    button = machine.Pin(0, machine.Pin.IN, machine.Pin.PULL_UP)
    while True:
        if button() == 0:
            print("Single shot")
            sensor.measure()
        
        result = sensor.read()
        print(f"{result["temp"]:.4f} 'C \t {result["pres"]:.2f} hPa")
        time.sleep_ms(100)
    """
    
    # demo of normal mode
    sensor.config(OSRT_T_X16, OSRT_P_X16, MODE_NORMAL, T_SB_05MS, FILTER_OFF)
    while True:    
        result = sensor.read()
        print(f"{result["temp"]:.4f} 'C \t {result["pres"]:.2f} hPa")
        time.sleep_ms(100)
    
    mem_used.print_ram_used()


