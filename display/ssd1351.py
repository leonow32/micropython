# MicroPython 1.24.1 ESP32-S3 Octal SPIRAM
# Works also with SSD1306 128x64

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
        
        self.cmd_write(0xFD) # Set lock command
        self.data_write(0x12)

        self.cmd_write(0xFD)  # Set lock command
        self.data_write(0xB1)                     # Command A2,B1,B3,BB,BE,C1 accessible if in unlock state

        self.cmd_write(0xAE)     # Display disable

        self.cmd_write(0xA4) # Normal Display mode

        self.cmd_write(0x15)      # Set column address
        self.data_write(0x00) # Column address start value
        self.data_write(0x7F) # Column address end value

        self.cmd_write(0x75) # Set row address
        self.data_write(0x00)             # Row address start value
        self.data_write(0x7F)             # Row address end value

        self.cmd_write(0xB3)
        self.data_write(0xF1)

        self.cmd_write(0xCA)
        self.data_write(0x7F)

        self.cmd_write(0xA0) # Set re-map & data format
        self.data_write(0b00100101)               # Vertical address increment 0b01110101
                                            #// bit 0 - 1: kursor od lewej do prawej, 1 od góry do dołu
                                            #    // bit 1 - lustrzane odbicie Y
                                            #    // bit 2 - zamiana kolorów
                                            #    // bit 3 - nieużywany
                                            #    // bit 4 - lustrzane odbicie X
                                            #    // bit 5 - naprzemienne linie (nie używać)
                                            #    // bit 67 - format koloru

        self.cmd_write(0xA1) # Set display start line
        self.data_write(0x00)

        self.cmd_write(0xA2) # Set display offset
        self.data_write(0x00)

        self.cmd_write(0xAB) # Function selection
        self.data_write(0x01)

        self.cmd_write(0xB4) # segment low voltage
        self.data_write(0xA0)
        self.data_write(0xB5)
        self.data_write(0x55)

        self.cmd_write(0xC1) # Contrast
        self.data_write(255)
        self.data_write(255)
        self.data_write(255)

        self.cmd_write(0xC7) # Master contrast current
        self.data_write(0x0F)

        self.cmd_write(0xB1) # Reset precharge
        self.data_write(0x32)

        self.cmd_write(0xB2) # Display enhancement
        self.data_write(0xA4)
        self.data_write(0x00)
        self.data_write(0x00)

        self.cmd_write(0xBB) # Precharge voltage
        self.data_write(0x17)

        self.cmd_write(0xB6) # Second precharge
        self.data_write(0x01)

        self.cmd_write(0xBE) # VCOMH voltage
        self.data_write(0x05)

        self.cmd_write(0xA6) # Display mode reset

        self.cmd_write(0xAF) # Display on
        
        self.cmd_write(0x5C) # RAM Write
        self.dc(1)
        
    @micropython.viper
    def __str__(self):
        return f"SSD1351(spi={self.spi}, cs={self.cs}, dc={self.dc}, rotate={self.rotate})"

    def data_write(self, data):
        self.dc(1)
        self.cs(0)
        self.spi.write(bytes([data]))
        self.cs(1)
        
    def cmd_write(self, cmd):
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
    