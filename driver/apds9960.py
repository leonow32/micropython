# MicroPython 1.24.1 ESP32-S3 Octal SPIRAM
# v1.0.0 2025.04.25

from micropython import const
import struct
import time

# Włączenie gesture i light jednocześnie chyba jest niemożliwe
# Po włączeniu gesture sensor light sensor wyłącza się automatcznie

# useful registers
REG_ENABLE     = const(0x80)
REG_ATIME      = const(0x81)
REG_WTIME      = const(0x83)
REG_AILTL      = const(0x84)
REG_AILTH      = const(0x85)
REG_AIHTL      = const(0x86)
REG_AIHTH      = const(0x87)
REG_PILT       = const(0x89)
REG_PIHT       = const(0x8B)
REG_PERS       = const(0x8C)
REG_CONFIG1    = const(0x8D)
REG_PPULSE     = const(0x8E)
REG_CONTROL    = const(0x8F)
REG_CONFIG2    = const(0x90)
REG_ID         = const(0x92)
REG_STATUS     = const(0x93)
REG_CDATAL     = const(0x94)
REG_CDATAH     = const(0x95)
REG_RDATAL     = const(0x96)
REG_RDATAH     = const(0x97)
REG_GDATAL     = const(0x98)
REG_GDATAH     = const(0x99)
REG_BDATAL     = const(0x9A)
REG_BDATAH     = const(0x9B)
REG_PDATA      = const(0x9C)
REG_POFFSET_UR = const(0x9D)
REG_POFFSET_DL = const(0x9E)
REG_CONFIG3    = const(0x9F)
REG_GPENTH     = const(0xA0)
REG_GEXTH      = const(0xA1)
REG_GCONF1     = const(0xA2)
REG_GCONF2     = const(0xA3)
REG_GOFFSET_U  = const(0xA4)
REG_GOFFSET_D  = const(0xA5)
REG_GOFFSET_L  = const(0xA7)
REG_GOFFSET_R  = const(0xA9)
REG_GPULSE     = const(0xA6)
REG_GCONF3     = const(0xAA)
REG_GCONF4     = const(0xAB)
REG_GFLVL      = const(0xAE)
REG_GSTATUS    = const(0xAF)
REG_IFORCE     = const(0xE4)
REG_PICLEAR    = const(0xE5)
REG_CICLEAR    = const(0xE6)
REG_AICLEAR    = const(0xE7)
REG_GFIFO_U    = const(0xFC) # gesture_sensor FIFO UP value
REG_GFIFO_D    = const(0xFD) # gesture_sensor FIFO DOWN value
REG_GFIFO_L    = const(0xFE) # gesture_sensor FIFO LEFT value
REG_GFIFO_R    = const(0xFF) # gesture_sensor FIFO RIGHT value

# Light sensor gain
AGAIN_1X       = const(0b00000000)
AGAIN_4X       = const(0b00000001)
AGAIN_16X      = const(0b00000010)
AGAIN_64X      = const(0b00000011)
                    
# Proximity sensor gain
PGAIN_1X       = const(0b00000000)
PGAIN_2X       = const(0b00000100)
PGAIN_4X       = const(0b00001000)
PGAIN_8X       = const(0b00001100)

# LED current
LED_100_MA     = const(0b00000000)
LED_50_MA      = const(0b01000000)
LED_25_MA      = const(0b10000000)
LED_12_MA      = const(0b11000000)

# other
I2C_ADDRESS    = const(0x39)
TIMEOUT_MS     = const(50)

class APDS9960():
    """
    Create an object to support APDS9960.
    - i2c: instance of I2C object.
    - device_address: address of the memory chip on I2C bus.
    """
    
    def __init__(self, i2c, int_gpio):
        time.sleep_ms(40)
        self.i2c = i2c
        self.int_gpio = int_gpio
        self.int_gpio.init(mode=machine.Pin.IN, pull=machine.Pin.PULL_UP)
        self.int_gpio.irq(self.irq_handler, machine.Pin.IRQ_FALLING | machine.Pin.IRQ_RISING)
        
    def __str__(self):
        return f"APDS9960({self.i2c}, {self.int_gpio}"
    
### REGISTER READ/WRITE ###
    
    def read_register(self, register):
        return self.i2c.readfrom_mem(I2C_ADDRESS, register, 1, addrsize=8)[0]
    
    def read_register16(self, register):
        result = self.i2c.readfrom_mem(I2C_ADDRESS, register, 2, addrsize=8)
        output = result[0] | (result[1] << 8)
        return output
    
    def write_register(self, register, value):
        self.i2c.writeto_mem(I2C_ADDRESS, register, bytes([value]), addrsize=8)
        
    def write_register16(self, register, value):
        buffer = bytes([value & 0x00FF, (value & 0xFF00) >> 8])
        self.i2c.writeto_mem(I2C_ADDRESS, register, buffer, addrsize=8)

### INTERRUPTS ###

    def irq_handler(self, source):
        print(f"IRQ, {source}, input_state={source.value()}")
        
    def irq_read(self):
        value = self.read_register(REG_STATUS)
        print(f"Proximity INT: {(value & 0b00100000) >> 5}")
        print(f"Light INT:     {(value & 0b00010000) >> 4}")
        print(f"Gesture INT:   {(value & 0b00000100) >> 2}")
        print(f"INT GPIO:      {self.int_gpio.value()}")
    
    def irq_clear_all_flags(self):
        self.write_register(REG_PICLEAR, 0xFF)
        self.write_register(REG_CICLEAR, 0xFF)
        self.write_register(REG_AICLEAR, 0xFF)

### LIGHT SENSOR ###
    
    def light_sensor_enable(self):
        value = self.read_register(REG_ENABLE)
        value = value | 0b00001011
        self.write_register(REG_ENABLE, value)
    
    def light_sensor_disable(self):
        value = self.read_register(REG_ENABLE)
        value = value & 0b11110101
        self.write_register(REG_ENABLE, value)
        pass
    
    def light_sensor_enabled_check(self):
        return (self.read_register(REG_ENABLE) & 0b00000010) >> 1
    
    def light_sensor_irq_enable(self):
        value = self.read_register(REG_ENABLE)
        value = value | 0b00010000
        self.write_register(REG_ENABLE, value)
    
    def light_sensor_irq_disable(self):
        value = self.read_register(REG_ENABLE)
        value = value & 0b11101111
        self.write_register(REG_ENABLE, value)
        
    def light_sensor_irq_flag_clear(self):
        self.write_register(REG_AICLEAR, 0xFF)
    
    def light_sensor_irq_low_threshold_get(self):
        value = self.read_register16(REG_AILTL)
        return value
    
    def light_sensor_irq_low_threshold_set(self, value):
        self.write_register16(REG_AILTL, value)
        
    def light_sensor_irq_high_threshold_get(self):
        value = self.read_register16(REG_AIHTL)
        return value
    
    def light_sensor_irq_high_threshold_set(self, value):
        self.write_register16(REG_AIHTL, value)
        
    def light_sensor_gain_get(self):
        value = self.read_register(REG_CONTROL) & 0b00000011
        print(value)
        return value
        
    def light_sensor_gain_set(self, again):
        value = self.read_register(REG_CONTROL)
        value = value & 0b11111100
        value = value | again
        self.write_register(REG_CONTROL, value)
        
    def light_sensor_integration_time_get(self):
        value = self.read_register(REG_ATIME)
        return (256-value) / 2.78
        
    def light_sensor_integration_time_set(self, time_ms):
        if time_ms > 712: time_ms = 712
        if time_ms < 1:   time_ms = 1
        value = int(256 - time_ms / 2.78)
        self.write_register(REG_ATIME, value)
        
    def light_sensor_valid_check(self):
        return self.read_register(REG_STATUS) & 0b00000001
        
    def light_sensor_read(self):
        c = self.read_register16(REG_CDATAL)
        r = self.read_register16(REG_RDATAL)
        g = self.read_register16(REG_GDATAL)
        b = self.read_register16(REG_BDATAL)
        
        print(f"C: {c:04X} {c}")
        print(f"R: {r:04X} {r}")
        print(f"G: {g:04X} {g}")
        print(f"B: {b:04X} {b}")
    
###############
# OTHER
###############

    def wait_time_get(self):
        value = self.read_register(REG_WTIME)
        return (256-value) / 2.78
        
    def wait_time_set(self, time_ms):
        if time_ms > 712: time_ms = 712
        if time_ms < 1:   time_ms = 1
        value = int(256 - time_ms / 2.78)
        self.write_register(REG_WTIME, value)

    def gesture_sensor_enable(self):
        value = self.read_register(REG_ENABLE)
        value = value | 0b01000001
        self.write_register(REG_ENABLE, value)
    
    def gesture_sensor_disable(self):
        value = self.read_register(REG_ENABLE)
        value = value & 0b10111111
        self.write_register(REG_ENABLE, value)
        pass
    
    def proximity_sensor_enable(self):
        pass
    
    def proximity_sensor_disable(self):
        pass
    
    def id_get(self):
        return self.i2c.readfrom_mem(I2C_ADDRESS, REG_ID, 1)[0]
    
    def status_get(self):
        """
        Return status byte.
        - Bit ...: ...
        """
        return self.read_register(REG_STATUS)

    def read_gfifo(self):
        fifo_level = self.read_register(REG_GFLVL)
        gest_status = self.read_register(REG_GSTATUS)
        u = self.read_register(REG_GFIFO_U)
        d = self.read_register(REG_GFIFO_D)
        l = self.read_register(REG_GFIFO_L)
        r = self.read_register(REG_GFIFO_R)
        
        print(f"FIFO: {fifo_level}")
        print(f"Status: {gest_status}")
        print(f"GFIFO_U: {u}")
        print(f"GFIFO_D: {d}")
        print(f"GFIFO_L: {l}")
        print(f"GFIFO_R: {r}")
        pass

    def dump(self):
        """
        Read and print all the information.
        """
        buffer = self.i2c.readfrom_mem(I2C_ADDRESS, 0x00, 256)
        
        print("     0  1  2  3  4  5  6  7  8  9  A  B  C  D  E  F")
        for i in range(len(buffer)):
            if i % 16 == 0:
                print(f"{i:02X}: ", end = "")
            print(f"{buffer[i]:02X}", end="\n" if i % 16 == 15 else " ")
    
if __name__ == "__main__":
    import mem_used
    import machine
        
    i2c = machine.I2C(0) # use default pinout and clock frequency
    int_gpio = machine.Pin(16)
    dut = APDS9960(i2c, int_gpio)
#     print(dut)
    
#     dut.dump()
#     print(f"ID: {dut.id_get():02X}")
    
#     dut.write_register(REG_CONFIG1, 0b01100000)   # don't enable long wait
#     dut.write_register(REG_CONFIG2, 0b00000001)   # disable saturation interrupts
#     dut.write_register(REG_CONFIG3, 0b00000000)   # jakieś wzmocnienia fotodiod proximity_sensor
#     dut.write_register(REG_ENABLE, 0b01111111)
    dut.light_sensor_read()
    
    dut.light_sensor_enable()
    
#     dut.light_sensor_irq_low_threshold_set(100)
#     dut.light_sensor_irq_high_threshold_set(200)
    
    print(f"light_sensor_irq_low_threshold_get()  = {dut.light_sensor_irq_low_threshold_get()}")
    print(f"light_sensor_irq_high_threshold_get() = {dut.light_sensor_irq_high_threshold_get()}")
    
    mem_used.print_ram_used()

