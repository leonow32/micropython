from machine import Pin, SPI
import framebuf
import time

WIDTH   = const(480)
HEIGHT  = const(320)

RED     = const(0b000_00000_11111_000)
YELLOW  = const(0b111_00000_11111_111)
GREEN   = const(0b111_00000_00000_111)
CYAN    = const(0b111_11111_00000_111)
BLUE    = const(0b000_11111_00000_000)
MAGENTA = const(0b000_11111_11111_000)
WHITE   = const(0b111_11111_11111_111)
BLACK   = const(0b000_00000_00000_000)

class ST7796(framebuf.FrameBuffer):
    
    def __init__(self, spi, cs, dc, rst):
        self.spi = spi
        self.cs  = cs
        self.dc  = dc
        self.rst = rst
        self.array = bytearray(WIDTH * HEIGHT * 2)
        super().__init__(self.array, WIDTH, HEIGHT, framebuf.RGB565)
        
        self.rst(0)
        time.sleep_ms(15)
        self.rst(1)
        time.sleep_ms(15)
        
        self.write_cmd(0x3A)             # COLMOD: Pixel Format Set
        self.write_data(0x05)            # 16-bit pixel format
        
        self.write_cmd(0x36)             # Memory Access Control
        self.write_data(0b11101100);     # MY=1 MX=1 MV=1 ML=0 BGR=1 MH=1 Dummy Dummy orientacja pozioma
        
        self.write_cmd(0x2B)             # Row range 0..319
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0x01)
        self.write_data(0x3F)
        
        self.write_cmd(0x2A)             # Col range 0..479
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0x01)
        self.write_data(0xDF)
        
        self.write_cmd(0x11)             # Sleep Out
        self.write_cmd(0x29)             # Display ON
            
    def write_data(self, data):
        self.dc(1)
        self.cs(0)
        self.spi.write(bytes([data]))
        self.cs(1)
        
    def write_cmd(self, data):
        self.dc(0)
        self.cs(0)
        self.spi.write(bytes([data]))
        self.cs(1)
        
    def refresh(self):
        self.cs(0)
        self.dc(0)
        self.spi.write(bytes([0x2C]))
        self.dc(1)
        self.spi.write(self.array)
        self.cs(1)
        
    def color(self, red, green, blue):
        red   = int(red)
        green = int(green)
        blue  = int(blue)
        
        if red > 255:
            red = 255
        if green > 255:
            green = 255
        if blue > 255:
            blue = 255
        
        red    = red & 0xF8
        green1 = (green & 0xE0) >> 5
        green2 = (green & 0x1C) << 11
        blue   = (blue & 0xF8) << 5
        color  = red | green1 | green2 | blue
        return color

if __name__ == "__main__":
    cs  = Pin(4,  Pin.OUT, value=1)
    dc  = Pin(6, Pin.OUT, value=1)
    rst = Pin(5, Pin.OUT, value=1)
    spi = SPI(2, baudrate=80_000_000, polarity=0, phase=0, sck=Pin(15), mosi=Pin(7), miso=None)
    #spi = SPI(1, baudrate=80_000_000, polarity=0, phase=0)
    print(spi)
    display = ST7796(spi, cs, dc, rst)
    
    display.rect(0, 0, 128, 64, WHITE)
    display.text('abcdefghijklm', 1, 2, RED)
    display.text('nopqrstuvwxyz', 1, 10, YELLOW)
    display.text('ABCDEFGHIJKLM', 1, 18, GREEN)
    display.text('NOPQRSTUVWXYZ', 1, 26, CYAN)
    display.text('0123456789+-*/', 1, 34, BLUE)
    display.text('!@#$%^&*(),.<>?', 1, 42, MAGENTA)
    display.refresh()
    

