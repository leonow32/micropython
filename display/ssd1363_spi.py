# MicroPython 1.24.1 ESP32 Pico

from machine import Pin, SPI
import framebuf

class SSD1363_SPI(framebuf.FrameBuffer):
    
    @micropython.native
    def __init__(self, spi, cs, dc, rotate=0,):
        self.spi    = spi
        self.cs     = cs
        self.dc     = dc
        self.cs.init(mode=Pin.OUT, value=1)
        self.dc.init(mode=Pin.OUT, value=1)
        
        self.rotate = rotate
        self.width  = 256
        self.height = 128
        self.array  = bytearray(self.width * self.height // 2)
        super().__init__(self.array, self.width, self.height, framebuf.GS4_HMSB)
        
        self.cmd_write(0xFD) # Command Lock
        self.data_write(0x12)
        
        self.cmd_write(0xAE) # Set Display Off
        
        self.cmd_write(0xB3) # Set Display Clock Divide Ratio/Oscillator Frequency
        self.data_write(0x90) # Creatway
#         self.data_write(0x30) # Midas
        
        self.cmd_write(0xCA) # Set Multiplex Ratio
        self.data_write(0x7F)
        
        self.cmd_write(0xA2) # Set Display Offset
        self.data_write(0x00) # Creatway
#         self.data_write(0x20) # Midas
        
        self.cmd_write(0xA1) # Set Display Start Line
        self.data_write(0x00)
        
        self.cmd_write(0xA0) # Set Re-Map & Dual COM Line Mode
        self.data_write(0x36) # Creatway
        self.data_write(0x01) # Creatway
#         self.data_write(0x32) # Midas
#         self.data_write(0x00) # Midas
        
        self.cmd_write(0xB5) # Set GPIO - Creatway
        self.data_write(0x00)
        
        self.cmd_write(0xAB) # Function Selection - Creatway
        self.data_write(0x01)
        
        self.cmd_write(0xB4) # Set Segment Low Voltage - Creatway
        self.data_write(0xA0)
        self.data_write(0xDD)
        
        self.cmd_write(0xC1) # Set Contrast Current
        self.data_write(0xCF)
        
        self.cmd_write(0xC7) # Master Contrast Current Control
        self.data_write(0x0F)
        
        self.cmd_write(0xB9) # Select Gray Scale Table
        
        self.cmd_write(0xB1) # Set Phase Length
        self.data_write(0xE2)
        
        self.cmd_write(0xD1) # Enhance Driving Scheme Capability
        self.data_write(0x82)
        self.data_write(0x20)
        
        self.cmd_write(0x15)  # Set Column Address
        self.data_write(0x1C) # 28  - Creatway
        self.data_write(0x5B) # 133 - Creatway
#         self.data_write(0x08) # 8  - Midas
#         self.data_write(0x47) # 71 - Midas
#         self.data_write(0x04) # moje prawa krawędź
#         self.data_write(0x23) # moje, lewa krawędź -> 32 kolumny
        
        self.cmd_write(0x75)  # Set Row Address
        self.data_write(0x00) # 0
        self.data_write(0x5F) # 95
        # 5F to linia na samej górze wyświetlacza
        
        self.cmd_write(0xBB) # Set Pre-Charge Voltage
        self.data_write(0x1F)
        
        self.cmd_write(0xB6) # Set Second Pre-Charge Period
        self.data_write(0x08)
        
        self.cmd_write(0xBE) # Set VCOMH Deselect Level
        self.data_write(0x07)
        
        self.cmd_write(0xA6) # Set Display Mode to not onverted
        
        self.cmd_write(0xAF) # Set Display On
    
    @micropython.viper
    def __str__(self):
        return f"SSD1363_SPI(spi={self.spi}, cs={self.cs}, dc={self.dc}, rotate={self.rotate})"
    
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
        
    @micropython.viper
    def disable(self):
        self.cmd_write(0xAE)
    
    @micropython.viper
    def contrast(self, value):
        self.cmd_write(0x81)
        self.cmd_write(value)
    
    @micropython.viper
    def refresh(self):
        pass
        # Set column address range from 0x00 to 0x7F, set page address range from 0x00 to 0x07
#         for cmd in (0x21, 0x00, 0x7F, 0x22, 0x00, 0x07):
#             self.cmd_write(cmd)

#         self.cmd_write(0x5C)  # Set Column Address
        
#         self.i2c.writevto(self.address, (b"\x80\x5C\x40", self.array))
        
    @micropython.native
    def simulate(self):
        pass
#         for y in range(self.height):
#             print(f"{y}\t", end="")
#             for x in range(self.width):
#                 bit  = 1 << (y % 8)
#                 byte = int(self.array[(y // 8) * self.width + x])
#                 pixel = "#" if byte & bit else "."
#                 print(pixel, end="")
#             print("")

if __name__ == "__main__":
    from machine import Pin, I2C
    import mem_used
#     from image.down_32x32 import *
#     from image.up_32x32 import *
#     from font.extronic16_unicode import *
#     from font.extronic16B_unicode import *

    spi = SPI(1, baudrate=10_000_000, polarity=0, phase=0)
    print(spi)
    
    display = SSD1363_SPI(spi, cs=Pin(9), dc=Pin(10), rotate=0)
    print(display)
    
    print("----")

#     display.fill_rect( 0,   0, 40, 20, display.color(0xFF, 0x00, 0x00))
#     display.fill_rect( 0,  20, 40, 20, display.color(0xFF, 0xFF, 0x00))
#     display.fill_rect( 0,  40, 40, 20, display.color(0x00, 0xFF, 0x00))
#     display.fill_rect( 0,  60, 40, 20, display.color(0x00, 0xFF, 0xFF))
#     display.fill_rect( 0,  80, 40, 20, display.color(0x00, 0x00, 0xFF))
#     display.fill_rect( 0, 100, 40, 20, display.color(0xFF, 0x00, 0xFF))
#     
# 
#     display.refresh()
    
    
#     hal = DisplayHAL(display)
#     print(hal)
    
#     hal.rect(0, 0, 128, 64, 1)
#     hal.line(2, 2, 125, 61, 1)
#     hal.circle(64, 32, 30, 1)
#     hal.text('abcdefghijklm',  1,  2, 1)
#     hal.text('nopqrstuvwxyz',  1, 10, 1)
#     hal.text("abcdefghijkl",  50, 20, 1,  extronic16_unicode, "center")
#     hal.text("abcdefghijkl",  50, 40, 0, extronic16B_unicode, "center")
#     hal.image(up_32x32,       96,  0, 0)
#     hal.image(down_32x32,     96, 32, 0)
   
    
#     hal.refresh()
#     hal.simulate()

    mem_used.print_ram_used()