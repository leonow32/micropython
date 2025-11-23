# MicroPython 1.24.1 ESP32 Pico
# MicroPython 1.26.1 ESP32-S3 Octal-SPIRAM

from machine import Pin, SPI
import framebuf

class SSD1363_BW_SPI(framebuf.FrameBuffer):
    
    @micropython.native
    def __init__(self, spi, cs, dc, rotate=0):
        self.spi    = spi
        self.cs     = cs
        self.dc     = dc
        self.cs.init(mode=Pin.OUT, value=1)
        self.dc.init(mode=Pin.OUT, value=1)
        
        self.rotate = rotate
        self.width  = 256
        self.height = 128
        self.mono   = True
        self.array  = bytearray(self.width * self.height // 8)
        super().__init__(self.array, self.width, self.height, framebuf.MONO_VLSB)
        
        self.cmd_write(0xFD) # Command Lock
        self.data_write(0x12)
        
        self.cmd_write(0xAE) # Set Display Off
        
        self.cmd_write(0xC1) # Set Contrast Current
        self.data_write(0xA0)
        
        if rotate:
            self.cmd_write(0xA0) # Set Re-Map & Dual COM Line Mode
            self.data_write(0b00100100)
            self.data_write(0b00000000)
            
            self.cmd_write(0xA2) # Set Display Offset
            self.data_write(0x80)
        
        else:
            self.cmd_write(0xA0) # Set Re-Map & Dual COM Line Mode
            self.data_write(0x32)
            self.data_write(0x00)
            
            self.cmd_write(0xA2) # Set Display Offset
            self.data_write(0x20)
        
        self.cmd_write(0x15)  # Set column range (0...79)
        self.data_write(8)
        self.data_write(71)   # display height (71-8+1)*2 = 128px
        
        self.cmd_write(0x75)  # Set row range (0...159)
        self.data_write(0)
        self.data_write(127)  # display width (127-0+1)*2 = 256px
        
        self.cmd_write(0xCA) # Set Multiplex Ratio
        self.data_write(0x7F)
        
        self.cmd_write(0xAD) # Set IREF (tego nie ma w Creatway i Midas)
        self.data_write(0x90) # Internal
        
        self.cmd_write(0xB3) # Set Display Clock Divide Ratio/Oscillator Frequency
        self.data_write(0x61) # Easy Rising
        
        self.cmd_write(0xB9) # Select Gray Scale Table
        
        self.cmd_write(0xAF) # Set Display On
    
    @micropython.viper
    def __str__(self):
        return f"SSD1363_BW_SPI(spi={self.spi}, cs={self.cs}, dc={self.dc}, rotate={self.rotate})"
    
    @micropython.viper
    def data_write(self, data: uint):
        self.dc(1)
        self.cs(0)
        self.spi.write(bytes([data]))
        self.cs(1)
        
    @micropython.viper
    def cmd_write(self, cmd: uint):
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
    def contrast_set(self, value: uint):        
        self.cmd_write(0xC1) # Set Contrast Current
        self.data_write(value)
        
    @micropython.native
    def color(self, r, g, b):
        return 1 if r | g | b else 0
        
    @micropython.native
    def refresh(self):
        buf = bytearray(self.width * self.height // 2)
        
        @micropython.native
        def pixel_set(x, y):
            col = x % 4
            if col == 0:
                buf[y*128 + x//2 + 1]  = 0x0F
            elif col == 1:
                buf[y*128 + x//2 + 1] |= 0xF0
            elif col == 2:
                buf[y*128 + x//2 - 1]  = 0x0F
            else:
                buf[y*128 + x//2 - 1] |= 0xF0
        
        x = 0
        y = 0
        for byte in self.array:
            if byte & 0b00000001: pixel_set(x, y+0)
            if byte & 0b00000010: pixel_set(x, y+1)
            if byte & 0b00000100: pixel_set(x, y+2)
            if byte & 0b00001000: pixel_set(x, y+3)
            if byte & 0b00010000: pixel_set(x, y+4)
            if byte & 0b00100000: pixel_set(x, y+5)
            if byte & 0b01000000: pixel_set(x, y+6)
            if byte & 0b10000000: pixel_set(x, y+7)
            
            x += 1
            if x == 256:
                x = 0
                y += 8
        
        self.cs(0)
        self.dc(0)
        self.spi.write(bytes([0x5C]))
        self.dc(1)
        self.spi.write(buf)
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
    from machine import Pin, I2C
    import mem_used
    import measure_time
#     from image.down_32x32 import *
#     from image.up_32x32 import *
#     from font.extronic16_unicode import *
#     from font.extronic16B_unicode import *

#     spi = SPI(1, baudrate=1_000_000, polarity=0, phase=0)
    spi = SPI(1, baudrate=1_000_000, polarity=0, phase=0, sck=Pin(4), mosi=Pin(5), miso=None)
    print(spi)
    
#     display = SSD1363_BW_SPI(spi, cs=Pin(9), dc=Pin(10), rotate=0)
    display = SSD1363_BW_SPI(spi, cs=Pin(7), dc=Pin(6), rotate=0)
    print(display)
    
    print("----")

#     display.fill_rect(0, 0, 16, 1, 1)
    display.rect(0, 0, 256, 128, 1)
#     display.rect(1, 1, 255, 127, 1)
    display.ellipse(128, 64, 60, 60, 1)
    display.ellipse(64, 32, 30, 30, 1)
    display.line(0, 0, 255, 127, 1)
#     display.circle(64, 32, 30, 1)
    display.text('abcdefghijklm',  1,  2)
    display.text('nopqrstuvwxyz',  1, 10)
#     hal.text("abcdefghijkl",  50, 20, 1,  extronic16_unicode, "center")
#     hal.text("abcdefghijkl",  50, 40, 0, extronic16B_unicode, "center")
#     hal.image(up_32x32,       96,  0, 0)
#     hal.image(down_32x32,     96, 32, 0)
   
    
    measure_time.begin()
    display.refresh()
    measure_time.end("Refresh time:  ")
    
#     display.simulate()

    mem_used.print_ram_used()
