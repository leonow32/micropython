# MicroPython 1.24.1 ESP32-S3 Octal SPIRAM
# v1.0.0 2025.04.25

from micropython import const
import machine
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

# Light sensor interrupt persistance (when interrupt is executed)
APERS_EVERYTIME = const(0b00000000) # Every ALS cycle
APERS_1_CYCLE   = const(0b00000001) # Any ALS value outside of threshold range
APERS_2_CYCLE   = const(0b00000010) # 2 consecutive ALS values out of range
APERS_3_CYCLE   = const(0b00000011) # 3 consecutive ALS values out of range
APERS_5_CYCLE   = const(0b00000100)
APERS_10_CYCLE  = const(0b00000101)
APERS_15_CYCLE  = const(0b00000110)
APERS_20_CYCLE  = const(0b00000111)
APERS_25_CYCLE  = const(0b00001000)
APERS_30_CYCLE  = const(0b00001001)
APERS_35_CYCLE  = const(0b00001010)
APERS_40_CYCLE  = const(0b00001011)
APERS_45_CYCLE  = const(0b00001100)
APERS_50_CYCLE  = const(0b00001101)
APERS_55_CYCLE  = const(0b00001110)
APERS_60_CYCLE  = const(0b00001111)

# Proximity sensor interrupt persistance (when interrupt is executed)
PPERS_EVERYTIME = const(0b00000000) # Every proximity cycle
PPERS_1_CYCLE   = const(0b00010000) # Any proximity value outside of threshold range
PPERS_2_CYCLE   = const(0b00100000) # 2 consecutive proximity values out of range
PPERS_3_CYCLE   = const(0b00110000) # 3 consecutive proximity values out of range
PPERS_4_CYCLE   = const(0b01000000)
PPERS_5_CYCLE   = const(0b01010000)
PPERS_6_CYCLE   = const(0b01100000)
PPERS_7_CYCLE   = const(0b01110000)
PPERS_8_CYCLE   = const(0b10000000)
PPERS_9_CYCLE   = const(0b10010000)
PPERS_10_CYCLE  = const(0b10100000)
PPERS_11_CYCLE  = const(0b10110000)
PPERS_12_CYCLE  = const(0b11000000)
PPERS_13_CYCLE  = const(0b11010000)
PPERS_14_CYCLE  = const(0b11100000)
PPERS_15_CYCLE  = const(0b11110000)

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
        self.int_gpio.irq(self.irq_callback, machine.Pin.IRQ_FALLING | machine.Pin.IRQ_RISING)
        self.light_sensor_irq_callback = None
        self.proximity_sensor_irq_callback = None
        self.gesture_sensor_irq_callback = None
        
    def __str__(self):
        return f"APDS9960({self.i2c}, int_gpio={self.int_gpio})"
    
### REGISTER READ/WRITE ###
    
    def register_read(self, register):
        return self.i2c.readfrom_mem(I2C_ADDRESS, register, 1, addrsize=8)[0]
    
    def register16_read(self, register):
        result = self.i2c.readfrom_mem(I2C_ADDRESS, register, 2, addrsize=8)
        output = result[0] | (result[1] << 8)
        return output
    
    def register_write(self, register, value):
        self.i2c.writeto_mem(I2C_ADDRESS, register, bytes([value]), addrsize=8)
        
    def register16_write(self, register, value):
        buffer = bytes([value & 0x00FF, (value & 0xFF00) >> 8])
        self.i2c.writeto_mem(I2C_ADDRESS, register, buffer, addrsize=8)

### INTERRUPTS ###

    def irq_callback(self, source):
        value = self.register_read(REG_STATUS)
        
        if self.light_sensor_irq_callback and (value & 0b00010000) >> 4:
            self.light_sensor_irq_callback()
            self.register_write(REG_CICLEAR, 0xFF)
            
        if self.proximity_sensor_irq_callback and (value & 0b00100000) >> 5:
            self.proximity_sensor_irq_callback()
            self.register_write(REG_PICLEAR, 0xFF)
            
        if self.gesture_sensor_irq_callback and (value & 0b00000100) >> 2:
            self.gesture_sensor_irq_callback()
            # TODO czy to tu powinno byc?
            self.register_write(REG_AICLEAR, 0xFF)
        
        self.irq_clear_all_flags()
        
    # debug
    def irq_read(self):
        value = self.register_read(REG_STATUS)
        print(f"Proximity INT: {(value & 0b00100000) >> 5}")
        print(f"Light INT:     {(value & 0b00010000) >> 4}")
        print(f"Gesture INT:   {(value & 0b00000100) >> 2}")
        print(f"INT GPIO:      {self.int_gpio.value()}")
    
    def irq_clear_all_flags(self):
        self.register_write(REG_PICLEAR, 0xFF)
        self.register_write(REG_CICLEAR, 0xFF)
        self.register_write(REG_AICLEAR, 0xFF)

### LIGHT SENSOR ###
    
    def light_sensor_enable(self):
        value = self.register_read(REG_ENABLE)
        value = value | 0b00001011
        self.register_write(REG_ENABLE, value)
    
    def light_sensor_disable(self):
        value = self.register_read(REG_ENABLE)
        value = value & 0b11110101
        self.register_write(REG_ENABLE, value)
        pass
    
    def light_sensor_enabled_check(self):
        return (self.register_read(REG_ENABLE) & 0b00000010) >> 1
    
    def light_sensor_irq_enable(self):
        """
        Must use light_sensor_irq_persistance_set(x) with x>=1 and x<=15
        """
        value = self.register_read(REG_ENABLE)
        value = value | 0b00010000
        self.register_write(REG_ENABLE, value)
    
    def light_sensor_irq_disable(self):
        value = self.register_read(REG_ENABLE)
        value = value & 0b11101111
        self.register_write(REG_ENABLE, value)
        
    def light_sensor_irq_flag_clear(self):
        self.register_write(REG_AICLEAR, 0xFF)
        
    def light_sensor_irq_callback_get(self):
        return self.light_sensor_irq_callback
        
    def light_sensor_irq_callback_set(self, callback):
        self.light_sensor_irq_callback = callback
        
    def light_sensor_irq_low_threshold_get(self):
        return self.register16_read(REG_AILTL)
    
    def light_sensor_irq_low_threshold_set(self, value):
        self.register16_write(REG_AILTL, value)
        
    def light_sensor_irq_high_threshold_get(self):
        return self.register16_read(REG_AIHTL)
    
    def light_sensor_irq_high_threshold_set(self, value):
        self.register16_write(REG_AIHTL, value)
        
    def light_sensor_irq_persistance_get(self):
        return self.register_read(REG_PERS) & 0x0F
    
    def light_sensor_irq_persistance_set(self, value):
        """
        Configure when the interrupt is executed. Use APERS_ values.
        """
        var = self.register_read(REG_PERS)
        var = var & 0b11110000
        var = var | value
        self.register_write(REG_PERS, var)
        
    def light_sensor_gain_get(self):
        value = self.register_read(REG_CONTROL) & 0b00000011
        print(value)
        return value
        
    def light_sensor_gain_set(self, again):
        """
        Use AGAIN_ values.
        """
        value = self.register_read(REG_CONTROL)
        value = value & 0b11111100
        value = value | again
        self.register_write(REG_CONTROL, value)
        
    def light_sensor_integration_time_get(self):
        value = self.register_read(REG_ATIME)
        return (256-value) / 2.78
        
    def light_sensor_integration_time_set(self, time_ms):
        """
        Exposure time of a single measurement in milliseconds. Allowable range 1...712 ms.
        """
        if time_ms > 712: time_ms = 712
        if time_ms < 1:   time_ms = 1
        value = int(256 - time_ms / 2.78)
        self.register_write(REG_ATIME, value)
        
    def light_sensor_valid_check(self):
        return self.register_read(REG_STATUS) & 0b00000001
        
    def light_sensor_read(self):
        c = self.register16_read(REG_CDATAL)
        r = self.register16_read(REG_RDATAL)
        g = self.register16_read(REG_GDATAL)
        b = self.register16_read(REG_BDATAL)
        return (c, r, g, b)

### PROXIMITY SENSOR ###
    
    def proximity_sensor_enable(self):
        value = self.register_read(REG_ENABLE)
        value = value | 0b00000101
        self.register_write(REG_ENABLE, value)
    
    def proximity_sensor_disable(self):
        value = self.register_read(REG_ENABLE)
        value = value & 0b11111011
        self.register_write(REG_ENABLE, value)
    
    def proximity_sensor_enabled_check(self):
        return (self.register_read(REG_ENABLE) & 0b00000100) >> 2
    
    def proximity_sensor_irq_enable(self):
        """
        Must use light_sensor_irq_persistance_set(x) with x>=1 and x<=15
        """
        value = self.register_read(REG_ENABLE)
        value = value | 0b00100000
        self.register_write(REG_ENABLE, value)
    
    def proximity_sensor_irq_disable(self):
        value = self.register_read(REG_ENABLE)
        value = value & 0b11011111
        self.register_write(REG_ENABLE, value)
        
    def proximity_sensor_irq_flag_clear(self):
        self.register_write(REG_PICLEAR, 0xFF)
        
    def proximity_sensor_irq_callback_get(self):
        return self.proximity_sensor_irq_callback
        
    def proximity_sensor_irq_callback_set(self, callback):
        self.light_sensor_irq_callback = callback
        
    def proximity_sensor_irq_low_threshold_get(self):
        return self.register_read(REG_PILT)
    
    def proximity_sensor_irq_low_threshold_set(self, value):
        """
        Range 0...255
        """
        self.register_write(REG_PILT, value)
        
    def proximity_sensor_irq_high_threshold_get(self):
        return self.register_read(REG_PIHT)
    
    def proximity_sensor_irq_high_threshold_set(self, value):
        """
        Range 0...255
        """
        self.register_write(REG_PIHT, value)
        
    def proximity_sensor_irq_persistance_get(self):
        return self.register_read(REG_PERS) & 0xF0
    
    def proximity_sensor_irq_persistance_set(self, value):
        """
        Configure when the interrupt is executed. Use PPERS_ values.
        """
        var = self.register_read(REG_PERS)
        var = var & 0b00001111
        var = var | value
        self.register_write(REG_PERS, var)
        
    def proximity_sensor_gain_get(self):
        return (self.register_read(REG_CONTROL) & 0b00001100) >> 2
        
    def proximity_sensor_gain_set(self, pgain):
        """
        Use PGAIN_ values.
        """
        value = self.register_read(REG_CONTROL)
        value = value & 0b11110011
        value = value | pgain
        self.register_write(REG_CONTROL, value)

# Proximity Pulse Count Register (0x8E)
    
        
    def proximity_sensor_valid_check(self):
        return (self.register_read(REG_STATUS) & 0b00000010) >> 1
    
    def proximity_sensor_read(self):
        value = self.register_read(REG_PDATA)
        return value

### GESTURE SENSOR ###
    
    def gesture_sensor_enable(self):
        value = self.register_read(REG_ENABLE)
        value = value | 0b01000001
        self.register_write(REG_ENABLE, value)
    
    def gesture_sensor_disable(self):
        value = self.register_read(REG_ENABLE)
        value = value & 0b10111111
        self.register_write(REG_ENABLE, value)
        pass

###############
# OTHER
###############

    def wait_time_get(self):
        value = self.register_read(REG_WTIME)
        return (256-value) / 2.78
        
    def wait_time_set(self, time_ms):
        if time_ms > 712: time_ms = 712
        if time_ms < 1:   time_ms = 1
        value = int(256 - time_ms / 2.78)
        self.register_write(REG_WTIME, value)
    
    def id_get(self):
        return self.i2c.readfrom_mem(I2C_ADDRESS, REG_ID, 1)[0]
    
    def status_get(self):
        """
        Return status byte.
        - Bit ...: ...
        """
        return self.register_read(REG_STATUS)

    def read_gfifo(self):
        fifo_level = self.register_read(REG_GFLVL)
        gest_status = self.register_read(REG_GSTATUS)
        u = self.register_read(REG_GFIFO_U)
        d = self.register_read(REG_GFIFO_D)
        l = self.register_read(REG_GFIFO_L)
        r = self.register_read(REG_GFIFO_R)
        
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
