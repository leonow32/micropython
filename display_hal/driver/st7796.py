# MicroPython 1.28.0 ESP32-S3 Octal SPIRAM

from machine import Pin, SPI
import framebuf
import time

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
        self.width    = 320 if (rotate == 0 or rotate == 180) else 480
        self.height   = 480 if (rotate == 0 or rotate == 180) else 320
        self.mono     = False
        self.array    = bytearray(self.width * self.height * 2)
        super().__init__(self.array, self.width, self.height, framebuf.RGB565)
        
        self.rst(0)
        time.sleep_ms(15)
        self.rst(1)
        time.sleep_ms(15)
        
        self.write_cmd(0x3A)             # COLMOD: Pixel Format Set
        self.write_data(0x05)            # 16-bit pixel format
        
        self.write_cmd(0x36)             # Memory Access Control
        if rotate == 0:
            self.write_data(0b01001000); # MY=0 MX=1 MV=0 ML=0 BGR=1 MH=0 Dummy=0 Dummy=0
        elif rotate == 90:
            self.write_data(0b00101100); # MY=0 MX=0 MV=1 ML=0 BGR=1 MH=1 Dummy=0 Dummy=0
        elif rotate == 180:
            self.write_data(0b10001000); # MY=1 MX=0 MV=0 ML=0 BGR=1 MH=0 Dummy=0 Dummy=0
        elif rotate == 270:
            self.write_data(0b11101100); # MY=1 MX=1 MV=1 ML=0 BGR=1 MH=1 Dummy=0 Dummy=0
            
        self.write_cmd(0x2B)             # Row range 0..479
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(self.height-1 >> 8)
        self.write_data(self.height-1 & 0xFF)
        
        self.write_cmd(0x2A)             # Col range 0..319
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(self.width-1 >> 8)
        self.write_data(self.width-1 & 0xFF)
        
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
        red    = red & 0xF8
        green1 = (green & 0xE0) >> 5
        green2 = (green & 0x1C) << 11
        blue   = (blue & 0xF8) << 5
        color  = red | green1 | green2 | blue
        return color

if __name__ == "__main__":
    import mem_used
    from machine import Pin, PWM, SPI
    pwm = PWM(Pin(16), freq=50000, duty_u16=65535)
    spi = SPI(2, baudrate=80_000_000, polarity=0, phase=0, sck=Pin(15), mosi=Pin(7), miso=None)
    display = ST7796(spi, cs=Pin(4), dc=Pin(6), rst=Pin(5), rotate=0)       # ok
#     display = ST7796(spi, cs=Pin(4), dc=Pin(6), rst=Pin(5), rotate=90)    # ok
#     display = ST7796(spi, cs=Pin(4), dc=Pin(6), rst=Pin(5), rotate=180)     # ok
#     display = ST7796(spi, cs=Pin(4), dc=Pin(6), rst=Pin(5), rotate=270)
    print(display)
    
    display.fill(BLUE)
    display.rect(0, 0, 128, 64, WHITE)
    display.text('abcdefghijklm', 1, 2, RED)
    display.text('nopqrstuvwxyz', 1, 10, YELLOW)
    display.text('ABCDEFGHIJKLM', 1, 18, GREEN)
    display.text('NOPQRSTUVWXYZ', 1, 26, CYAN)
    display.text('0123456789+-*/', 1, 34, BLUE)
    display.text('!@#$%^&*(),.<>?', 1, 42, MAGENTA)
    display.refresh()
    
    mem_used.print_ram_used()
