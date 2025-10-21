# MicroPython 1.24.1 ESP32-S3 Octal SPIRAM
# Works also with SSD1306 128x64

from machine import Pin, I2C
import framebuf
import mem_used

class SSD1363(framebuf.FrameBuffer):
    
    @micropython.native
    def __init__(self, i2c, address=0x3C, flip_x=False, flip_y=False):
        self.i2c     = i2c
        self.address = address
        self.flip_x  = flip_x
        self.flip_y  = flip_y
        self.width   = 128
        self.height  = 64
        self.array   = bytearray(self.width * self.height // 8)
        super().__init__(self.array, self.width, self.height, framebuf.MONO_VLSB)
        
        config = (
            0xAE,                     # Display off
            0x20, 0x00,               # Set memory addressing mode to horizontal addressing mode
            0x40,                     # Set display start line to 0
            0xA0 if flip_x else 0xA1, # Set segment remap
            0xA8, 0x3F,               # Set multiplex ratio to 63
            0xC0 if flip_y else 0xC8, # Set COM scan direction
            0xD3, 0x00,               # Set display offset to 0
            0xDA, 0x12,               # Set COM pins hardware config to enable COM left/right remap, sequential COM pin config
            0xD5, 0x80,               # Set clock and oscillator frequency to freq=8, clock=0
            0xD9, 0xF1,               # Set pre-charge period to phase_2=F, phase_1=1
            0xDB, 0x3C,               # Set VCOMH to max
            0x81, 0xFF,               # Set contrast to 255 (max)
            0xA4,                     # Use image in GDDRAM memory
            0xA6,                     # Display not inverted
            0x8D, 0x14,               # SSD1306 only - charge pump enable
            0xAF,                     # Display on
        )
        
        for cmd in config:
            self.write_cmd(cmd)
    
    @micropython.viper
    def __str__(self):
        return f"SSD1363(i2c={self.i2c}, address=0x{self.address:02X}, flip_x={self.flip_x}, flip_y={self.flip_y})"
    
    @micropython.viper
    def write_cmd(self, cmd: int):
        self.i2c.writeto(self.address, bytes([0x80, cmd]))
    
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
        # Set column address range from 0x00 to 0x7F, set page address range from 0x00 to 0x07
        for cmd in (0x21, 0x00, 0x7F, 0x22, 0x00, 0x07):
            self.write_cmd(cmd)
        
        self.i2c.writevto(self.address, (b"\x40", self.array))
        
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

