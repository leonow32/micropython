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
GRAY    = const(0b000_10000_10000_100)
BLACK   = const(0b000_00000_00000_000)

class ILI9341(framebuf.FrameBuffer):
    
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
#         self.width    = 320 if (rotate == 0 or rotate == 180) else 240
#         self.height   = 240 if (rotate == 0 or rotate == 180) else 320
        self.width    = 320
        self.height   = 240
        self.mono     = False
        self.array    = bytearray(self.width * self.height * 2)
        super().__init__(self.array, self.width, self.height, framebuf.RGB565)
        
        self.rst(0)
        time.sleep_ms(15)
        self.rst(1)
        time.sleep_ms(15)
        
        self.write_cmd(0xC0);               # Power control 1
        self.write_data(0x23);              # VRH[5:0]

        self.write_cmd(0xC1);               # Power control 2
        self.write_data(0x10);              # SAP[2:0]; BT[3:0]

        self.write_cmd(0xC5);               # VCM control
        self.write_data(0x3e);              # Contrast
        self.write_data(0x28);

        self.write_cmd(0xC7);               # VCM control2
        self.write_data(0x86);              # --

        self.write_cmd(0x36);               # Memory Access Control
        self.write_data(0x48);

        self.write_cmd(0x3A);               # Pixel Format Set
        self.write_data(0x55);

        self.write_cmd(0xB1);               # Frame Rate Control (In Normal Mode/Full Colors)
        self.write_data(0x00);
        self.write_data(0x18);

        self.write_cmd(0xB6);               # Display Function Control
        self.write_data(0x08);
        self.write_data(0b11000010);        # ISC[3:0]=2 GS=1 SS=0 (mirror Y)
        self.write_data(0x27);

        self.write_cmd(0x11);               # Exit Sleep
        time.sleep_ms(120)

        self.write_cmd(0x29);               # Display on

        self.write_cmd(0x2C);               # Memory Write
        
        """
        
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
        """
        
    @micropython.viper
    def __str__(self):
        return f"ILI9341(spi={self.spi}, cs={self.cs}, dc={self.dc}, rst={self.rst}, rotate={self.rotate})"
            
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
        
    @micropython.native
    def refresh(self):
        self.write_cmd(0x2B)             # Row range 0..479
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(self.width-1 >> 8)
        self.write_data(self.width-1 & 0xFF)
        
        self.write_cmd(0x2A)             # Col range 0..319
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(self.height-1 >> 8)
        self.write_data(self.height-1 & 0xFF)
        
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
    from machine import Pin, PWM, SPI
    from display_hal.driver.st7796 import *
    pwm = PWM(Pin(16), freq=50000, duty_u16=65535)
    spi = SPI(2, baudrate=80_000_000, polarity=0, phase=0, sck=Pin(15), mosi=Pin(7), miso=None)
    display = ILI9341(spi, cs=Pin(4), dc=Pin(6), rst=Pin(5), rotate=0)
    
    print(display)
    
    display.fill(BLUE)
#     display.vline(0, 0, 100, YELLOW)

    display.pixel(100, 100, WHITE)
    display.pixel(103, 100, WHITE)
# 
#     display.pixel(0, 100, WHITE)
#     display.pixel(0, 101, WHITE)
    
#     display.rect(0, 0, 100, 100, BLUE)
#     display.rect(0, 0, display.width, display.height, YELLOW)
    display.refresh()