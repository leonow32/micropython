# MicroPython 1.24.1 ESP32 Pico

from machine import Pin, SPI
import framebuf

RED     = const(0b000_00000_11111_000)
YELLOW  = const(0b111_00000_11111_111)
GREEN   = const(0b111_00000_00000_111)
CYAN    = const(0b111_11111_00000_111)
BLUE    = const(0b000_11111_00000_000)
MAGENTA = const(0b000_11111_11111_000)
WHITE   = const(0b111_11111_11111_111)
BLACK   = const(0b000_00000_00000_000)

class SSD1351(framebuf.FrameBuffer):
    
    @micropython.native
    def __init__(self, spi, cs, dc, rotate=0):
        print("Init begin")
        
        self.spi     = spi
        self.cs      = cs
        self.dc      = dc
        self.cs.init(mode=Pin.OUT, value=1)
        self.dc.init(mode=Pin.OUT, value=1)
        
        self.rotate  = rotate
        self.width   = 128
        self.height  = 128
        self.mono    = False
        self.array   = bytearray(self.width * self.height * 2)
        super().__init__(self.array, self.width, self.height, framebuf.RGB565)
        
        self.cs(0)
        self.dc(0)

        self.transmit(b"\xFD\x12") # Set lock command
        self.transmit(b"\xFD\xB1") # Set lock command
        self.transmit(b"\xAE") # Display disable
        self.transmit(b"\xA4") # Normal Display mode
        self.transmit(b"\x15\x00\x7F") # Set column address range
        self.transmit(b"\x75\x00\x7F") # Set row address
        self.transmit(b"\xB3\xF1") #
        self.transmit(b"\xCA\x7F") #
        self.transmit(b"\xA0\x25") # Set re-map & data format
        self.transmit(b"\xA1\x00") # Set display start line
        self.transmit(b"\xA2\x00") # Set display offset
        self.transmit(b"\xAB\x01") # Function selection
        self.transmit(b"\xB4\xA0\xB5\x55") # segment low voltage
        self.transmit(b"\xC1\xFF\xFF\xFF") # Contrast
        self.transmit(b"\xC7\x0F") # Master contrast current
        self.transmit(b"\xB1\x32") # Reset precharge
        self.transmit(b"\xB2\xA4\x00\x00") # Display enhancement
        self.transmit(b"\xBB\x17") # Precharge voltage
        self.transmit(b"\xB6\x01") # Second precharge
        self.transmit(b"\xBE\x05") # VCOMH voltage
        self.transmit(b"\xA6") # Display mode reset
        self.transmit(b"\xAF") # Display on
        self.transmit(b"\x5C") # RAM Write
        
        self.cs(1)
        self.dc(1)
        
        print("Init end")
    
    @micropython.viper
    def __str__(self):
        return f"SSD1351(spi={self.spi}, cs={self.cs}, dc={self.dc}, rotate={self.rotate})"
    
    @micropython.native
    def transmit(self, buffer):
        self.spi.write(buffer[0:1])
        if len(buffer) > 1:
            self.dc(1)
            self.spi.write(buffer[1:])
            self.dc(0)
    
    @micropython.viper
    def enable(self):
        self.transmit("\xAF")
        
    @micropython.viper
    def disable(self):
        self.transmit(b"\xAE")
    
    @micropython.viper
    def contrast_set(self, value):
        self.transmit(bytearray([0xC1, value, value, value]))
        self.transmit(b"\x5C") # RAM Write
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

if __name__ == "__main__":
    from machine import Pin, SPI
    import mem_used
    import measure_time
    import display_hal
    from image.down_32x32 import *
    from image.up_32x32 import *
    from font.extronic16_unicode import *
    from font.extronic16B_unicode import *

    spi     = SPI(1, baudrate=10_000_000, polarity=0, phase=0) # use default pinout
    cs      = Pin(27)
    dc      = Pin(15)
    display = SSD1351(spi, cs, dc, rotate=0)
    hal     = display_hal.DisplayHAL(display)
    print(hal)
    
    hal.rect(0, 0, 128, 128, hal.color(0xFF, 0xFF, 0xFF))
    hal.line(2, 2, 125, 125, hal.color(0xFF, 0x00, 0x00))
    hal.circle(64, 64, 32, hal.color(0x00, 0xFF, 0x00))
    hal.text('abcdefghijklm',  1,  2, hal.color(0x00, 0xFF, 0xFF))
    hal.text('nopqrstuvwxyz',  1, 10, hal.color(0x00, 0x00, 0xFF))
    hal.text("abcdefghijkl",  50, 20, hal.color(0xFF, 0x00, 0xFF), extronic16_unicode, "center")
    hal.text("abcdefghijkl",  50, 40, hal.color(0xFF, 0xFF, 0x00), extronic16B_unicode, "center")
    hal.image(up_32x32,       96,  0, hal.color(0xFF, 0x00, 0x00))
    hal.image(down_32x32,     96, 32, hal.color(0x00, 0xFF, 0x00))
   
    
    hal.refresh()
#     hal.simulate()

    mem_used.print_ram_used()
    