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
LDRIVE__100_MA  = const(0b00000000)
LDRIVE__50_MA   = const(0b01000000)
LDRIVE__25_MA   = const(0b10000000)
LDRIVE__12_MA   = const(0b11000000)

# LED boost
LED_BOOST_100_P = const(0b00000000)
LED_BOOST_150_P = const(0b00010000)
LED_BOOST_200_P = const(0b00100000)
LED_BOOST_300_P = const(0b00110000)

# other
I2C_ADDRESS    = const(0x39)
TIMEOUT_MS     = const(50)

class APDS9960:
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
        self.als_irq_callback = None
        self.als_saturation_irq_callback = None
        self.prox_sensor_irq_callback = None
        self.prox_saturation_irq_callback = None
        self.gesture_sensor_irq_callback = None
        
        self.als  = self.ALS(self)
        self.prox = self.Prox(self)
        
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

### COMMON ###
    
    def everything_disable(self):
        self.register_write(REG_ENABLE, 0x00)

### INTERRUPTS ###

    def irq_callback(self, source):
        value = self.register_read(REG_STATUS)
        
        if value & 0b10000000 and self.als_saturation_irq_callback:
            self.als_saturation_irq_callback()
        
        if value & 0b01000000 and self.prox_saturation_irq_callback:
            self.prox_saturation_irq_callback()
            
        if value & 0b00100000 and self.prox_sensor_irq_callback:
            self.prox_sensor_irq_callback()
        
        if value & 0b00010000 and self.als_irq_callback:
            self.als_irq_callback()
        
        if value & 0b00000100 and self.gesture_sensor_irq_callback:
            self.gesture_sensor_irq_callback()
        
        self.irq_clear_all_flags()
        
    # debug
    def irq_read(self):
        value = self.register_read(REG_STATUS)
        print(f"Proximity INT: {(value & 0b00100000) >> 5}")
        print(f"Proximity SAT: {(value & 0b01000000) >> 6}")
        print(f"Light INT:     {(value & 0b00010000) >> 4}")
        print(f"Gesture INT:   {(value & 0b00000100) >> 2}")
        print(f"INT GPIO:      {self.int_gpio.value()}")
    
    def irq_clear_all_flags(self):
        self.register_write(REG_PICLEAR, 0xFF)
        self.register_write(REG_CICLEAR, 0xFF)
        self.register_write(REG_AICLEAR, 0xFF)

### LIGHT SENSOR ###
        
    class ALS:
        
        def __init__(self, outer):
            self.outer = outer
    
        def enable(self):
            value = self.outer.register_read(REG_ENABLE)
            value = value | 0b00001011
            self.outer.register_write(REG_ENABLE, value)
        
        def disable(self):
            value = self.outer.register_read(REG_ENABLE)
            value = value & 0b11110101
            self.outer.register_write(REG_ENABLE, value)
            pass
        
        def enabled_check(self):
            return (self.outer.register_read(REG_ENABLE) & 0b00000010) >> 1
        
        def irq_enable(self):
            """
            Must use light_sensor_irq_persistance_set(x) with x>=1 and x<=15
            """
            value = self.outer.register_read(REG_ENABLE)
            value = value | 0b00010000
            self.outer.register_write(REG_ENABLE, value)
        
        def irq_disable(self):
            value = self.outer.register_read(REG_ENABLE)
            value = value & 0b11101111
            self.outer.register_write(REG_ENABLE, value)
            
        def irq_flag_clear(self):
            self.outer.register_write(REG_AICLEAR, 0xFF)
            
        def irq_callback_get(self):
            return self.outer.als_irq_callback
            
        def irq_callback_set(self, callback):
            self.outer.als_irq_callback = callback
            
        def irq_saturation_callback_get(self):
            return self.outer.als_saturation_irq_callback
            
        def irq_saturation_callback_set(self, callback):
            self.outer.als_saturation_irq_callback = callback
            
        def irq_low_threshold_get(self):
            return self.outer.register16_read(REG_AILTL)
        
        def irq_low_threshold_set(self, value):
            self.outer.register16_write(REG_AILTL, value)
            
        def irq_high_threshold_get(self):
            return self.outer.register16_read(REG_AIHTL)
        
        def irq_high_threshold_set(self, value):
            self.outer.register16_write(REG_AIHTL, value)
            
        def irq_persistance_get(self):
            return self.outer.register_read(REG_PERS) & 0x0F
        
        def irq_persistance_set(self, value):
            """
            Configure when the interrupt is executed. Use APERS_ values.
            """
            var = self.outer.register_read(REG_PERS)
            var = var & 0b11110000
            var = var | value
            self.outer.register_write(REG_PERS, var)
            
        def irq_saturation_enable(self):
            value = self.outer.register_read(REG_CONFIG2)
            value = value | 0b01000000
            self.outer.register_write(REG_CONFIG2, value)
            
        def irq_saturation_disable(self):
            value = self.outer.register_read(REG_CONFIG2)
            value = value & 0b10111111
            self.outer.register_write(REG_CONFIG2, value)
            
        def gain_get(self):
            value = self.outer.register_read(REG_CONTROL) & 0b00000011
            print(value)
            return value
            
        def gain_set(self, again):
            """
            Use AGAIN_ values.
            """
            value = self.outer.register_read(REG_CONTROL)
            value = value & 0b11111100
            value = value | again
            self.outer.register_write(REG_CONTROL, value)
            
        def integration_time_get(self):
            value = self.outer.register_read(REG_ATIME)
            return (256-value) / 2.78
            
        def integration_time_set(self, time_ms):
            """
            Exposure time of a single measurement in milliseconds. Allowable range 1...712 ms.
            """
            if time_ms > 712: time_ms = 712
            if time_ms < 1:   time_ms = 1
            value = int(256 - time_ms / 2.78)
            self.outer.register_write(REG_ATIME, value)
            
        def valid_check(self):
            return self.outer.register_read(REG_STATUS) & 0b00000001
        
        def saturation_check(self):
            return (self.outer.register_read(REG_STATUS) & 0b10000000) >> 7
            
        def read(self):
            c = self.outer.register16_read(REG_CDATAL)
            r = self.outer.register16_read(REG_RDATAL)
            g = self.outer.register16_read(REG_GDATAL)
            b = self.outer.register16_read(REG_BDATAL)
            return (c, r, g, b)

### PROXIMITY SENSOR ###
    
    class Prox:
        
        def __init__(self, outer):
            self.outer = outer
    
        def enable(self):
            value = self.outer.register_read(REG_ENABLE)
            value = value | 0b00000101
            self.outer.register_write(REG_ENABLE, value)
        
        def disable(self):
            value = self.outer.register_read(REG_ENABLE)
            value = value & 0b11111011
            self.outer.register_write(REG_ENABLE, value)
        
        def enabled_check(self):
            return (self.outer.register_read(REG_ENABLE) & 0b00000100) >> 2
        
        def irq_enable(self):
            """
            Must use light_sensor_irq_persistance_set(x) with x>=1 and x<=15
            """
            value = self.outer.register_read(REG_ENABLE)
            value = value | 0b00100000
            self.outer.register_write(REG_ENABLE, value)
        
        def irq_disable(self):
            value = self.outer.register_read(REG_ENABLE)
            value = value & 0b11011111
            self.outer.register_write(REG_ENABLE, value)
            
        def irq_flag_clear(self):
            self.outer.register_write(REG_PICLEAR, 0xFF)
            
        def irq_callback_get(self):
            return self.outer.prox_sensor_irq_callback
            
        def irq_callback_set(self, callback):
            self.outer.prox_sensor_irq_callback = callback
            
        def irq_saturation_callback_get(self):
            return self.outer.prox_saturation_irq_callback
            
        def irq_saturation_callback_set(self, callback):
            self.outer.prox_saturation_irq_callback = callback
            
        def irq_saturation_enable(self):
            value = self.outer.register_read(REG_CONFIG2)
            value = value | 0b10000000
            self.outer.register_write(REG_CONFIG2, value)
            
        def irq_saturation_disable(self):
            value = self.outer.register_read(REG_CONFIG2)
            value = value & 0b01111111
            self.outer.register_write(REG_CONFIG2, value)
            
        def irq_low_threshold_get(self):
            return self.outer.register_read(REG_PILT)
        
        def irq_low_threshold_set(self, value):
            """
            Range 0...255
            """
            self.outer.register_write(REG_PILT, value)
            
        def irq_high_threshold_get(self):
            return self.outer.register_read(REG_PIHT)
        
        def irq_high_threshold_set(self, value):
            """
            Range 0...255
            """
            self.outer.register_write(REG_PIHT, value)
            
        def irq_persistance_get(self):
            return self.outer.register_read(REG_PERS) & 0xF0
        
        def irq_persistance_set(self, value):
            """
            Configure when the interrupt is executed. Use PPERS_ values.
            """
            var = self.outer.register_read(REG_PERS)
            var = var & 0b00001111
            var = var | value
            self.outer.register_write(REG_PERS, var)
            
        def gain_get(self):
            return self.outer.register_read(REG_CONTROL) & 0b00001100
            
        def gain_set(self, pgain):
            """
            Use PGAIN_ values.
            """
            value = self.outer.register_read(REG_CONTROL)
            value = value & 0b11110011
            value = value | pgain
            self.outer.register_write(REG_CONTROL, value)
            
        def led_drive_get(self):
            return self.outer.register_read(REG_CONTROL) & 0b11000000
            
        def led_drive_set(self, ldrive):
            """
            Use LDRIVE_ values.
            """
            value = self.outer.register_read(REG_CONTROL)
            value = value & 0b11000000
            value = value | ldrive
            self.outer.register_write(REG_CONTROL, value)
            
        def led_boost_get(self):
            return self.outer.register_read(REG_CONFIG2) & 0b00110000
            
        def led_boost_set(self, led_boost):
            """
            Use LED_BOOST_ values.
            """
            value = self.outer.register_read(REG_CONFIG2)
            value = value & 0b00110000
            value = value | led_boost | 0b00000001
            self.outer.register_write(REG_CONFIG2, value)

    # Proximity Pulse Count Register (0x8E)
        
            
        def valid_check(self):
            return (self.outer.register_read(REG_STATUS) & 0b00000010) >> 1
        
        def saturation_check(self):
            return (self.outer.register_read(REG_STATUS) & 0b01000000) >> 6
        
        def read(self):
            value = self.outer.register_read(REG_PDATA)
            return value

### GESTURE SENSOR ###
    
    def gesture_sensor_enable(self):
        value = self.outer.register_read(REG_ENABLE)
        value = value | 0b01000001
        self.outer.register_write(REG_ENABLE, value)
    
    def gesture_sensor_disable(self):
        value = self.outer.register_read(REG_ENABLE)
        value = value & 0b10111111
        self.outer.register_write(REG_ENABLE, value)
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
        return self.outer.register_read(REG_STATUS)

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


# RP2040
if __name__ == "__main__":
    import mem_used
    
    def proximity_data_print(source):
        valid  = dut.prox.valid_check()
        result = dut.prox.read()
        print(f"Proximity: {result:3d}, valid: {valid}")
    
    def proximity_irq():
        value = dut.prox.read()
        low_threshold  = dut.prox.irq_low_threshold_get()
        high_threshold = dut.prox.irq_high_threshold_get()
        if value >= high_threshold:
            ledr(1)
            ledy(0)
            ledg(0)
        elif value <= low_threshold:
            ledr(0)
            ledy(0)
            ledg(1)
        else:
            ledr(0)
            ledy(1)
            ledg(0)
            
        dut.prox.irq_flag_clear()
        
    i2c  = machine.I2C(0) # use default pinout and clock frequency
    irq  = machine.Pin(16)
    ledr = machine.Pin(18, machine.Pin.OUT)
    ledy = machine.Pin(19, machine.Pin.OUT)
    ledg = machine.Pin(20, machine.Pin.OUT)
    dut  = APDS9960(i2c, irq)
    tim  = machine.Timer(mode=machine.Timer.PERIODIC, period=1000, callback=proximity_data_print)
    
    dut.everything_disable()
    dut.irq_clear_all_flags()

    dut.prox.gain_set(PGAIN_8X)
    dut.prox.led_drive_set(LDRIVE__100_MA)
    dut.prox.led_boost_set(LED_BOOST_300_P)
    dut.prox.irq_low_threshold_set(100)
    dut.prox.irq_high_threshold_set(200)
    dut.prox.irq_persistance_set(PPERS_15_CYCLE)
    dut.prox.irq_callback_set(proximity_irq)
#     dut.prox.irq_enable()
    dut.prox.enable()
    dut.prox.enable()

    mem_used.print_ram_used()


"""
# ESP32-S3
if __name__ == "__main__":
    import mem_used
    import neopixel
    
    def proximity_data_print(source):
#         dut.irq_read()
        valid  = dut.prox.valid_check()
        result = dut.prox.read()
        print(f"Proximity: {result:3d}, valid: {valid}")
        
    def proximity_irq():
        value = dut.prox.read()
        low_threshold  = dut.prox.irq_low_threshold_get()
        high_threshold = dut.prox.irq_high_threshold_get()
        if value >= high_threshold:
            led[0] = (10, 0, 0)
        elif value <= low_threshold:
            led[0] = (0, 10, 0)
        else:
            led[0] = (0, 0, 10)
            
        led.write()
        dut.prox.irq_flag_clear()
        
    i2c = machine.I2C(0) # use default pinout and clock frequency
    irq = machine.Pin(16)
    dut = APDS9960(i2c, irq)
    led = neopixel.NeoPixel(machine.Pin(48, machine.Pin.OUT), 1)
    tim = machine.Timer(0, mode=machine.Timer.PERIODIC, period=1000, callback=proximity_data_print)

    print(dut)
    
    ut.everything_disable()
    dut.irq_clear_all_flags()

    dut.prox.gain_set(PGAIN_8X)
    dut.prox.led_drive_set(LDRIVE__100_MA)
    dut.prox.led_boost_set(LED_BOOST_300_P)
    dut.prox.irq_low_threshold_set(100)
    dut.prox.irq_high_threshold_set(200)
    dut.prox.irq_persistance_set(PPERS_15_CYCLE)
    dut.prox.irq_callback_set(proximity_irq)
#     dut.prox.irq_enable()
    dut.prox.enable()

    print(f"Enable register: {dut.register_read(0x80):08b}")

    mem_used.print_ram_used()
"""
