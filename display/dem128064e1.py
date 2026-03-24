# MicroPython 1.27.0 Raspberry Pi Pico 2

from machine import Pin, SPI
import time
import framebuf

DEFAULT_CONTRAST = const(8)

class DEM128064E1(framebuf.FrameBuffer):
    
    @micropython.native
    def __init__(self, spi, cs, dc, rst):
        self.spi = spi
        self.cs  = cs
        self.dc  = dc
        self.rst = rst
        self.cs.init(mode=Pin.OUT, value=1)
        self.dc.init(mode=Pin.OUT, value=1)
        self.rst.init(mode=Pin.OUT, value=0)
        
        time.sleep_ms(5)
        self.rst(1)
        time.sleep_ms(5)
        
        self.width   = 128
        self.height  = 64
        self.mono    = True
        self.array   = bytearray(self.width * self.height // 8)
        super().__init__(self.array, self.width, self.height, framebuf.MONO_VLSB)
        
        config = (
            0xAF, # Display on
            0xA0, # ADC select: normal
            0xC8, # Commom output mode select: normal
            0xA6, # Display normal
            0XA4, # Normal display
            0xA2, # Bias set: 1/9
            0x40, # Set start line
            0x2F, # Power control set
            0x27, # Set (Rb/Ra)
            0x81, # Set the V0 output voltage in next byte
            DEFAULT_CONTRAST,   # Value of V0
        )
        
        for cmd in config:
            self.cmd_write(cmd)
    
    @micropython.viper
    def __str__(self):
        return f"DEM128064E1(spi={self.spi}, cs={self.cs}, dc={self.dc}, rst={self.rst})"
    
    @micropython.native
    def data_write(self, data):
        self.dc(1)
        self.cs(0)
        self.spi.write(bytes([data]))
        self.cs(1)
        
    @micropython.native
    def cmd_write(self, cmd):
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
    def contrast_set(self, value):
        self.cmd_write(0x81)
        self.cmd_write(value)
    
    @micropython.native
    def color(self, r, g, b):
        return 1 if r | g | b else 0
    
    @micropython.native
    def refresh(self):
        self.cs(0)

        for page in range(8):
            header = bytes([
                0xB0 | page, # Set page number
                0x00 ,       # Set x cursor, low nibble
                0x10 ,       # Set x cursor, high nibble
            ])
            
            self.dc(0)
            self.spi.write(header)
            self.dc(1)
            self.spi.write(self.array[page*(self.width):(page+1)*(self.width)])
            
        self.cs(1)
        
    @micropython.native
    def simulate(self):
        for y in range(self.height):
            print(f"{y}\t", end="")
            for x in range(self.width):
                bit  = 1 << (y % 8)
                byte = int(self.array[(y // 8) * self.width + x])
                pixel = "#" if byte & bit else "."
                print(pixel, end="")
            print("")

if __name__ == "__main__":
    spi = SPI(0, baudrate=1_000_000, polarity=0, phase=0, sck=Pin(2), mosi=Pin(3), miso=Pin(4))
    display = DEM128064E1(spi, cs=Pin(5), dc=Pin(6), rst=Pin(7))
    print(display)
    
    display.rect(0, 0, 128, 64, 1)
    display.text("abcdefg", 3, 3, 1)
    display.line(20, 20, 40, 40, 1)
    display.refresh()
    