# MicroPython 1.28.0 ESP32-S3 Octal SPIRAM

from machine import Pin, SPI
import framebuf
import time

WIDTH   = const(320)
HEIGHT  = const(480)

RED     = const(0b000_00000_11111_000)
YELLOW  = const(0b111_00000_11111_111)
GREEN   = const(0b111_00000_00000_111)
CYAN    = const(0b111_11111_00000_111)
BLUE    = const(0b000_11111_00000_000)
MAGENTA = const(0b000_11111_11111_000)
WHITE   = const(0b111_11111_11111_111)
BLACK   = const(0b000_00000_00000_000)

class ST7796(framebuf.FrameBuffer):
    
    @micropython.native
    def __init__(self, spi, cs, dc, rst, rotate=0):
        self.spi = spi
        self.cs  = cs
        self.dc  = dc
        self.rst = rst
        self.cs.init(mode=Pin.OUT, value=1)
        self.dc.init(mode=Pin.OUT, value=1)
        self.rst.init(mode=Pin.OUT, value=1)
        
        self.rotate   = rotate
        self.width    = 320 if rotate == 0  or rotate == 180 else 480
        self.height   = 480 if rotate == 90 or rotate == 270 else 320
        self.mono     = False
        self.array    = bytearray(WIDTH * HEIGHT * 2)
        super().__init__(self.array, WIDTH, HEIGHT, framebuf.RGB565)
        
        self.rst(0)
        time.sleep_ms(15)
        self.rst(1)
        time.sleep_ms(15)
        
        self.write_cmd(0x3A)             # COLMOD: Pixel Format Set
        self.write_data(0x05)            # 16-bit pixel format
        
        self.write_cmd(0x36)             # Memory Access Control
        self.write_data(0b01001000);     # MY=0 MX=1 MV=0 ML=0 BGR=1 MH=0 Dummy Dummy
        
        self.write_cmd(0x2B)             # Row range 0..479
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0x01)
        self.write_data(0xDF)
        
        self.write_cmd(0x2A)             # Col range 0..319
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0x01)
        self.write_data(0x3F)
        
        self.write_cmd(0x11)             # Sleep Out
        self.write_cmd(0x29)             # Display ON
        
    @micropython.viper
    def __str__(self):
        return f"ST7796(spi={self.spi}, cs={self.cs}, dc={self.dc}, rst={self.rst}, rotate={self.rotate})"
            
    @micropython.viper
    def write_data(self, data):
        self.dc(1)
        self.cs(0)
        self.spi.write(bytes([data]))
        self.cs(1)
        
    @micropython.viper
    def write_cmd(self, data):
        self.dc(0)
        self.cs(0)
        self.spi.write(bytes([data]))
        self.cs(1)
        
    @micropython.viper
    def refresh(self):
        self.cs(0)
        self.dc(0)
        self.spi.write(bytes([0x2C]))
        self.dc(1)
        self.spi.write(self.array)
        self.cs(1)
        
    @micropython.viper
    def color(self, red: uint, green: uint, blue: uint) -> uint:
#         red   = int(red)
#         green = int(green)
#         blue  = int(blue)
#         
#         if red > 255:
#             red = 255
#         if green > 255:
#             green = 255
#         if blue > 255:
#             blue = 255
        
        red    = red & 0xF8
        green1 = (green & 0xE0) >> 5
        green2 = (green & 0x1C) << 11
        blue   = (blue & 0xF8) << 5
        color  = red | green1 | green2 | blue
        return color

if __name__ == "__main__":
    spi = SPI(2, baudrate=80_000_000, polarity=0, phase=0, sck=Pin(15), mosi=Pin(7), miso=None)
    display = ST7796(spi, cs=Pin(4), dc=Pin(6), rst=Pin(5))
    
    display.rect(0, 0, 128, 64, WHITE)
    display.text('abcdefghijklm', 1, 2, RED)
    display.text('nopqrstuvwxyz', 1, 10, YELLOW)
    display.text('ABCDEFGHIJKLM', 1, 18, GREEN)
    display.text('NOPQRSTUVWXYZ', 1, 26, CYAN)
    display.text('0123456789+-*/', 1, 34, BLUE)
    display.text('!@#$%^&*(),.<>?', 1, 42, MAGENTA)
    display.refresh()
    
