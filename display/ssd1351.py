# MicroPython 1.24.1 ESP32-S3 Octal SPIRAM
# Works also with SSD1306 128x64

from machine import Pin, SPI
import framebuf

class SSD1351(framebuf.FrameBuffer):
    
    @micropython.native
    def __init__(self, spi, cs, dc, rotate=0):
        self.spi    = spi
        self.cs     = cs
        self.dc     = dc
        self.cs.init(mode=Pin.OUT, value=1)
        self.dc.init(mode=Pin.OUT, value=1)
        
        self.rotate = rotate
        self.width  = 128
        self.height = 128
        self.mono   = False
        self.array  = bytearray(self.width * self.height * 2)
        super().__init__(self.array, self.width, self.height, framebuf.RGB565)
        
        self.cmd_write(0xFD)  # Set lock command
        self.data_write(0x12)

        self.cmd_write(0xFD)  # Set lock command
        self.data_write(0xB1) # Command A2,B1,B3,BB,BE,C1 accessible if in unlock state

        self.cmd_write(0xAE)  # Display disable

        self.cmd_write(0xA4)  # Normal Display mode

        self.cmd_write(0x15)  # Set column address
        self.data_write(0x00) # Column address start value
        self.data_write(0x7F) # Column address end value

        self.cmd_write(0x75)  # Set row address
        self.data_write(0x00) # Row address start value
        self.data_write(0x7F) # Row address end value

        self.cmd_write(0xB3)  # Clock divider
        self.data_write(0xF1)

        self.cmd_write(0xCA)  # Set mux ratio
        self.data_write(0x7F)

        self.cmd_write(0xA0)  # Set re-map & data format
        
        if rotate == 0:
            self.data_write(0b00100101)
        elif rotate == 90:
            self.data_write(0b00110100)
        elif rotate == 180:
            self.data_write(0b00110111)
        elif rotate == 270:
            self.data_write(0b00100110)
        else:
            raise Exception("Wrong rotation value")

        self.cmd_write(0xA1)  # Set display start line
        self.data_write(0x00)

        self.cmd_write(0xA2)  # Set display offset
        self.data_write(0x00)

        self.cmd_write(0xAB)  # Function selection
        self.data_write(0x01)

        self.cmd_write(0xB4)  # segment low voltage
        self.data_write(0xA0)
        self.data_write(0xB5)
        self.data_write(0x55)

        self.cmd_write(0xC1)  # Contrast
        self.data_write(255)
        self.data_write(255)
        self.data_write(255)

        self.cmd_write(0xC7)  # Master contrast current
        self.data_write(0x0F)
        self.data_write(0x0F)
        self.data_write(0x0F)

        self.cmd_write(0xB1)  # Reset precharge
        self.data_write(0x32)

        self.cmd_write(0xB2)  # Display enhancement
        self.data_write(0xA4)
        self.data_write(0x00)
        self.data_write(0x00)

        self.cmd_write(0xBB)  # Precharge voltage
        self.data_write(0x17)

        self.cmd_write(0xB6)  # Second precharge
        self.data_write(0x01)

        self.cmd_write(0xBE)  # VCOMH voltage
        self.data_write(0x05)

        self.cmd_write(0xA6)  # Display mode reset

        self.cmd_write(0xAF)  # Display on
        
        self.cmd_write(0x5C)  # RAM Write
        self.dc(1)
        
    @micropython.viper
    def __str__(self):
        return f"SSD1351(spi={self.spi}, cs={self.cs}, dc={self.dc}, rotate={self.rotate})"

    @micropython.viper
    def data_write(self, data: uint):
        self.dc(1)
        self.cs(0)
        self.spi.write(bytes([data]))
        self.cs(1)
        
    @micropython.viper
    def cmd_write(self, cmd: uint):
        self.dc(0)
        self.cs(0)
        self.spi.write(bytes([cmd]))
        self.cs(1)
    
    @micropython.viper
    def enable(self):
        self.cmd_write(0xAF)
        self.cmd_write(0x5C) # RAM Write
        self.dc(1)
        
    @micropython.viper
    def disable(self):
        self.cmd_write(0xAE)
        self.cmd_write(0x5C) # RAM Write
        self.dc(1)
    
    @micropython.viper
    def contrast_set(self, value):
        self.cmd_write(0xC1)
        self.data_write(value)
        self.data_write(value)
        self.data_write(value)
        self.cmd_write(0x5C) # RAM Write
        self.dc(1)
        
    @micropython.viper
    def color(self, r: int, g: int, b: int) -> int:
        r = r & 0xF8
        b = (b & 0xF8) << 5
        gh = (g & 0xE0) << 8
        gl = (g & 0x1C) >> 3
        result = gh | b | r | gl
        return result
    
    @micropython.viper
    def refresh(self):
        self.cs(0)
        self.spi.write(self.array)
        self.cs(1)
        
    @micropython.viper
    def simulate(self):
        print("Not implemented")
    