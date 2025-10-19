# MicroPython 1.24.1 ESP32-S3 Octal SPIRAM
# Works also with SSD1306 128x64

from machine import Pin, SPI
from micropython import const
import framebuf
import mem_used

SSD1351_COLUMN_RANGE = const( 0x15 )
SSD1351_ROW_RANGE = const( 0x75 )
SSD1351_RAM_WRITE = const( 0x5C )
SSD1351_RAM_READ = const( 0x5D )
SSD1351_REMAP_COLOR_DEPTH = const( 0xA0 )
SSD1351_SET_DISPLAY_START_LINE = const( 0xA1 )
SSD1351_SET_DISPLAY_OFFSET = const( 0xA2 )
SSD1351_SET_DISPLAY_MODE_OFF = const( 0xA4 )
SSD1351_SET_DISPLAY_MODE_ON = const( 0xA5 )
SSD1351_SET_DISPLAY_MODE_RESET = const( 0xA6 )
SSD1351_SET_DISPLAY_MODE_INVERT = const( 0xA7 )
SSD1351_FUNCTION_SELECTION = const( 0xAB )
SSD1351_NOP = const( 0xAD )
SSD1351_SLEEP_MODE_ON = const( 0xAE )
SSD1351_SLEEP_MODE_OFF = const( 0xAF )
SSD1351_NOP2 = const( 0xB0 )
SSD1351_SET_RESET_PRECHARGE = const( 0xB1 )
SSD1351_DISPLAY_ENHANCEMENT = const( 0xB2 )
SSD1351_CLOCK_DIVIDER_OSC_FREQ = const( 0xB3 )
SSD1351_SET_SEGMENT_LOW_VOLTAGE = const( 0xB4 )
SSD1351_SET_GPIO = const( 0xB5 )
SSD1351_SET_SECOND_PRECHARGE = const( 0xB6 )
SSD1351_LOOKUP_TABLE = const( 0xB8 )
SSD1351_USE_BUILTIN_LINEAR_LUT = const( 0xB9 )
SSD1351_SET_PRECHARGE_VOLTAGE = const( 0xBB )
SSD1351_SET_VCOMH_VOLTAGE = const( 0xBE )
SSD1351_SET_CONTRAST = const( 0xC1 )
SSD1351_MASTER_CONTRAST_CURRENT = const( 0xC7 )
SSD1351_SET_MUX_RATIO = const( 0xCA )
SSD1351_NOP3 = const( 0xD1 )
SSD1351_NOP4 = const( 0xE3 )
SSD1351_SET_LOCK_COMMAND = const( 0xFD )
SSD1351_HORIZONTAL_SCROLL = const( 0x96 )
SSD1351_STOP_MOVING = const( 0x9E )
SSD1351_START_MOVING = const( 0x9F )

# BLACK = const(0b0000000000000000)
# RED = const(0b1111100000000000)
# GREEN = const(0b0000011111100000)
# YELLOW = const(0b1111111111100000)
# BLUE = const(0b0000000000011111)
# MAGENTA = const(0b1111100000011111)
# CYAN = const(0b0000011111111111)
# WHITE = const(0b1111111111111111)
# GRAY = const(0b1000010000010000)
# LIGHTRED = const(0b1111110000010000)
# LIGHTGREEN = const(0b1000011111110000)
# LIGHTYELLOW = const(0b1111111111110000)
# LIGHTBLUE = const(0b1000010000011111)
# LIGHTMAGENTA = const(0b1111110000011111)
# LIGHTCYAN = const(0b1000011111111111)
# LIGHTGRAY = const(0b1100011000011000)

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
    def __init__(self, spi, cs, dc, flip_x=False, flip_y=False):
        self.spi     = spi
        self.cs      = cs
        self.dc      = dc
        self.cs.init(mode=Pin.OUT, value=1)
        self.dc.init(mode=Pin.OUT, value=1)
        
        self.flip_x  = flip_x
        self.flip_y  = flip_y
        self.width   = 128
        self.height  = 128
        self.array   = bytearray(self.width * self.height * 2)
        super().__init__(self.array, self.width, self.height, framebuf.RGB565)
        
        self.cmd(SSD1351_SET_LOCK_COMMAND)
        self.data(0x12)

        self.cmd(SSD1351_SET_LOCK_COMMAND)  # Command lock
        self.data(0xB1)                     # Command A2,B1,B3,BB,BE,C1 accessible if in unlock state

        self.cmd(SSD1351_SLEEP_MODE_ON)     # Display off

        self.cmd(SSD1351_SET_DISPLAY_MODE_OFF) # Normal Display mode

        self.cmd(SSD1351_COLUMN_RANGE)      # Set column address
        self.data(0x00) # Column address start value
        self.data(0x7F) # Column address end value

        self.cmd(SSD1351_ROW_RANGE) # Set row address
        self.data(0x00)             # Row address start value
        self.data(0x7F)             # Row address end value

        self.cmd(SSD1351_CLOCK_DIVIDER_OSC_FREQ)
        self.data(0xF1)

        self.cmd(SSD1351_SET_MUX_RATIO)
        self.data(0x7F)

        self.cmd(SSD1351_REMAP_COLOR_DEPTH) # Set re-map & data format
        self.data(0b01110101)               # Vertical address increment 0b01110101
                                            #// bit 0 - 1: kursor od lewej do prawej, 1 od góry do dołu
                                            #    // bit 1 - lustrzane odbicie Y
                                            #    // bit 2 - zamiana kolorów
                                            #    // bit 3 - nieużywany
                                            #    // bit 4 - lustrzane odbicie X
                                            #    // bit 5 - naprzemienne linie (nie używać)
                                            #    // bit 67 - format koloru

        self.cmd(SSD1351_SET_DISPLAY_START_LINE) # Set display start line
        self.data(0x00)

        self.cmd(SSD1351_SET_DISPLAY_OFFSET) # Set display offset
        self.data(0x00)

        self.cmd(SSD1351_FUNCTION_SELECTION)
        self.data(0x01)

        self.cmd(SSD1351_SET_SEGMENT_LOW_VOLTAGE)
        self.data(0xA0)
        self.data(0xB5)
        self.data(0x55)

        self.cmd(SSD1351_SET_CONTRAST)
        self.data(255)
        self.data(255)
        self.data(255)

        self.cmd(SSD1351_MASTER_CONTRAST_CURRENT)
        self.data(0x0F)

        self.cmd(SSD1351_SET_RESET_PRECHARGE)
        self.data(0x32)

        self.cmd(SSD1351_DISPLAY_ENHANCEMENT)
        self.data(0xA4)
        self.data(0x00)
        self.data(0x00)

        self.cmd(SSD1351_SET_PRECHARGE_VOLTAGE)
        self.data(0x17)

        self.cmd(SSD1351_SET_SECOND_PRECHARGE)
        self.data(0x01)

        self.cmd(SSD1351_SET_VCOMH_VOLTAGE)
        self.data(0x05)

        self.cmd(SSD1351_SET_DISPLAY_MODE_RESET)

        self.cmd(SSD1351_SLEEP_MODE_OFF) # Display on

#         config = (
#             0xAE,                     # Display off
#             0x20, 0x00,               # Set memory addressing mode to horizontal addressing mode
#             0x40,                     # Set display start line to 0
#             0xA0 if flip_x else 0xA1, # Set segment remap
#             0xA8, 0x3F,               # Set multiplex ratio to 63
#             0xC0 if flip_y else 0xC8, # Set COM scan direction
#             0xD3, 0x00,               # Set display offset to 0
#             0xDA, 0x12,               # Set COM pins hardware config to enable COM left/right remap, sequential COM pin config
#             0xD5, 0x80,               # Set clock and oscillator frequency to freq=8, clock=0
#             0xD9, 0xF1,               # Set pre-charge period to phase_2=F, phase_1=1
#             0xDB, 0x3C,               # Set VCOMH to max
#             0x81, 0xFF,               # Set contrast to 255 (max)
#             0xA4,                     # Use image in GDDRAM memory
#             0xA6,                     # Display not inverted
#             0x8D, 0x14,               # SSD1306 only - charge pump enable
#             0xAF,                     # Display on
#         )
#         
#         for cmd in config:
#             self.write_cmd(cmd)
    
    @micropython.viper
    def __str__(self):
        return f"SSD1351(spi={self.spi}, cs={self.cs}, dc={self.dc}, flip_x={self.flip_x}, flip_y={self.flip_y})"

    def data(self, data):
        self.dc(1)
        self.cs(0)
        self.spi.write(bytes([data]))
        self.cs(1)
        
    def cmd(self, cmd):
        self.dc(0)
        self.cs(0)
        self.spi.write(bytes([cmd]))
        self.cs(1)
    
    @micropython.viper
    def enable(self):
        self.write_cmd(0xAF)
        
    @micropython.viper
    def disable(self):
        self.write_cmd(0xAE)
    
    @micropython.viper
    def contrast(self, value):
        self.write_cmd(0x81)
        self.write_cmd(value)
    
    @micropython.viper
    def refresh(self):
        self.cs(0)
        self.dc(0)
        self.spi.write(bytes([SSD1351_RAM_WRITE]))
        self.dc(1)
        self.spi.write(self.array)
        self.cs(0)
        
    @micropython.native
    def simulate(self):
        print("Not implemented")

if __name__ == "__main__":
    from machine import Pin, SPI
#     from sh1106 import *
#     from ssd1309 import *
    import mem_used
#     from image.down_32x32 import *
#     from image.up_32x32 import *
#     from font.extronic16_unicode import *
#     from font.extronic16B_unicode import *

    spi = SPI(1, baudrate=10_000_000, polarity=0, phase=0) # use default pinout
    print(spi)
    
    cs = Pin(27)
    dc = Pin(15)
    

    display = SSD1351(spi, cs, dc, flip_x=True, flip_y=True)

    display.fill_rect( 0,   0, 40, 20, RED)
    display.fill_rect( 0,  20, 40, 20, YELLOW)
    display.fill_rect( 0,  40, 40, 20, GREEN)
    display.fill_rect( 0,  60, 40, 20, CYAN)
    display.fill_rect( 0,  80, 40, 20, BLUE)
    display.fill_rect( 0, 100, 40, 20, MAGENTA)
    
#     display.fill_rect( 0,   0, 40, 20, 0b10000_000000_00000)
#     display.fill_rect( 0,  20, 40, 20, 0b01000_000000_00000)
#     display.fill_rect( 0,  40, 40, 20, 0b00100_000000_00000)
#     display.fill_rect( 0,  60, 40, 20, 0b00010_000000_00000)
#     display.fill_rect( 0,  80, 40, 20, 0b00001_000000_00000)
    
#     display.fill_rect(40,   0, 40, 20, 0b00000_100000_00000)
#     display.fill_rect(40,  20, 40, 20, 0b00000_010000_00000)
#     display.fill_rect(40,  40, 40, 20, 0b00000_001000_00000)
#     display.fill_rect(40,  60, 40, 20, 0b00000_000100_00000)
#     display.fill_rect(40,  80, 40, 20, 0b00000_000010_00000)
#     display.fill_rect(40, 100, 40, 20, 0b00000_000001_00000)
#     
#     display.fill_rect(80,   0, 40, 20, 0b00000_000000_10000)
#     display.fill_rect(80,  20, 40, 20, 0b00000_000000_01000)
#     display.fill_rect(80,  40, 40, 20, 0b00000_000000_00100)
#     display.fill_rect(80,  60, 40, 20, 0b00000_000000_00010)
#     display.fill_rect(80,  80, 40, 20, 0b00000_000000_00001)
    
#     display.fill_rect(0, 20, 20, 20, 0b00000_111111_00000)
#     display.fill_rect(0, 40, 20, 20, 0b00000_000000_11111)
    display.refresh()
    
    
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