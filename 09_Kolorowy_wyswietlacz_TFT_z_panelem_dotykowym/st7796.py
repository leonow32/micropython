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
        self.write_data(0b01001000);     # MY=0 MX=1 MV=0 ML=0 BGR=1 MH=0 Dummy Dummy orientacja pionowa
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

if __name__ == "__main__":
    cs  = Pin(17, Pin.OUT, value=1)
    dc  = Pin(15, Pin.OUT, value=1)
    rst = Pin(16, Pin.OUT, value=1)
    spi = SPI(2, baudrate=80_000_000, polarity=0, phase=0, sck=Pin(5), mosi=Pin(6), miso=Pin(4))
    display = ST7796(spi, cs, dc, rst)
    
    display.rect(0, 0, 128, 64, WHITE)
    display.text('abcdefghijklm', 1, 2, RED)
    display.text('nopqrstuvwxyz', 1, 10, YELLOW)
    display.text('ABCDEFGHIJKLM', 1, 18, GREEN)
    display.text('NOPQRSTUVWXYZ', 1, 26, CYAN)
    display.text('0123456789+-*/', 1, 34, BLUE)
    display.text('!@#$%^&*(),.<>?', 1, 42, MAGENTA)
    display.refresh()
    
