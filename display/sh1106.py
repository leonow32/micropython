# MicroPython 1.24.1 ESP32 Pico

from machine import Pin, I2C
import framebuf

class SH1106(framebuf.FrameBuffer):
    
    @micropython.native
    def __init__(self, i2c, address=0x3C, rotate=0, offset_x=2):
        if offset_x > 15:
            raise Exception("offset_x over range")
        """
        - offset_x - max 15px
        """
        self.i2c      = i2c
        self.address  = address
        self.rotate   = rotate
        self.offset_x = offset_x
        self.width    = 128
        self.height   = 64
        self.mono     = True
        self.array    = bytearray((self.width+4) * self.height // 8)
        super().__init__(self.array, (self.width+4), self.height, framebuf.MONO_VLSB)
        
        config = (
            0xAE,                     # Display off
            0x00 | offset_x,          # Column Low Nibble + offset x
            0x10,                     # Column High Nibble = 0
            0xB0,                     # Set Page = 0
            0x40,                     # Set Start Line = 0
            0xA0 if rotate else 0xA1, # Set Remap (flip x)
            0xDA, 0x12,               # Com pins
            0xD3, 0x00,               # Display offset
            0xC0 if rotate else 0xC8, # Scan direction (flip y)
            0xA6,                     # Positive image
            0xA4,                     # Entrie display on
            0x81, 0xFF,               # Contrast = full
            0xA8, 0x3F,               # Multiplex ratio = 1/64 duty
            0xD5, 0x80,               # Display clock divider
            0xD9, 0xF1,               # Charge period
            0xDB, 0x40,               # VCOM select
            0x8D, 0x14,               # Charge pump
            0xAF,                     # Display on
        )
        
        for cmd in config:
            self.cmd_write(cmd)
    
    @micropython.viper
    def __str__(self):
        return f"SH1106(i2c={self.i2c}, address=0x{self.address:02X}, rotate={self.rotate}, offset_x={self.offset_x})"
    
    @micropython.viper
    def data_write(self, data: int):
        self.i2c.writeto(self.address, bytes([0x40, cmd]))
    
    @micropython.viper
    def cmd_write(self, cmd: int):
        self.i2c.writeto(self.address, bytes([0x80, cmd]))
    
    @micropython.viper
    def enable(self):
        self.cmd_write(0xAF)
        
    @micropython.viper
    def disable(self):
        self.cmd_write(0xAE)
    
    @micropython.viper
    def contrast_set(self, value: int):
        self.cmd_write(0x81)
        self.cmd_write(value)
        
    @micropython.native
    def color(self, r, g, b):
        return 1 if r | g | b else 0
    
    @micropython.native
    def refresh(self):
        for page in range(8):
            header = bytes([
                0x80, 0xB0 | page,          # Set page number
                0x80, 0x00 | self.offset_x, # Set x cursor, low nibble
                0x80, 0x10,                 # Set x cursor, high nibble
                0x40                        # The following bytes are graphic data
            ])
            
            self.i2c.writevto(self.address, (header, self.array[page*(self.width+4):(page+1)*(self.width+4)-1]))
        
    @micropython.native
    def simulate(self):
        for y in range(self.height):
            print(f"{y}\t", end="")
            for x in range(self.width):
                bit  = 1 << (y % 8)
                byte = int(self.array[(y // 8) * (self.width+4) + x])
                pixel = "#" if byte & bit else "."
                print(pixel, end="")
            print("")
