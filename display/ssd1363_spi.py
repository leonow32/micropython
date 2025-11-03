# MicroPython 1.24.1 ESP32 Pico

from machine import Pin, SPI
import framebuf

class SSD1363_SPI(framebuf.FrameBuffer):
    
    @micropython.native
    def __init__(self, spi, cs, dc, rotate=0,):
        self.spi    = spi
        self.cs     = cs
        self.dc     = dc
        self.cs.init(mode=Pin.OUT, value=1)
        self.dc.init(mode=Pin.OUT, value=1)
        
        self.rotate = rotate
        self.width  = 256
        self.height = 128
#         self.array  = bytearray(self.width * self.height // 8)
#         super().__init__(self.array, self.width, self.height, framebuf.MONO_VLSB)
        
        self.array  = bytearray(self.width * self.height // 2)
        super().__init__(self.array, self.width, self.height, framebuf.GS4_HMSB)
        
        # This works - od lewej do prawej, potem w dół, kolejność pikseli w grypach 4 bajtów jest zamieniona
        self.cmd_write(0xFD) # Command Lock
        self.data_write(0x12)
        
        self.cmd_write(0xAE) # Set Display Off
        
        self.cmd_write(0xC1) # Set Contrast Current
        self.data_write(0xA0)
        
        self.cmd_write(0xA0) # Set Re-Map & Dual COM Line Mode
        self.data_write(0b00110010) # od lewej do prawej, potem w dół
        self.data_write(0b00000000)
        
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
#         self.data_write(0x00)
#         self.data_write(0x61) # Easy Rising
#         self.data_write(0x90) # Creatway
        self.data_write(0x30) # Midas
        
        self.cmd_write(0xB9) # Select Gray Scale Table
        
        self.cmd_write(0xAF) # Set Display On
    
    @micropython.viper
    def __str__(self):
        return f"SSD1363_SPI(spi={self.spi}, cs={self.cs}, dc={self.dc}, rotate={self.rotate})"
    
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
    def contrast(self, value):
        self.cmd_write(0x81)
        self.cmd_write(value)
        
    def test1(self, data):
        self.cmd_write(0x15)  # Set column range (0...79)
        self.data_write(8)
        self.data_write(71)   # display height (71-8+1)*2 = 128px
        
        self.cmd_write(0x75)  # Set row range (0...159)
        self.data_write(0)
        self.data_write(127)  # display width (127-0+1)*2 = 256px
        
        self.cmd_write(0x5C)  # Write RAM
        
        self.cs(0)
        self.dc(1)
        for i in range(16384):
#         for i in range(128*4):
            self.spi.write(bytes([data]))
        self.cs(1)
        
    def test2(self, x, y, data):
        self.cmd_write(0x15)  # Set column range (0...79)
        self.data_write(8+x)
        self.data_write(8+x)   # display height (71-8+1)*2 = 128px
        
        self.cmd_write(0x75)  # Set row range (0...159)
        self.data_write(y)
        self.data_write(y)  # display width (127-0+1)*2 = 256px
        
        self.cmd_write(0x5C)  # Write RAM
        self.cs(0)
        self.dc(1)
        self.spi.write(data)
        self.cs(1)
        
    # 14 ms
    @micropython.native
    def refresh1(self):
        self.cs(0)
        self.dc(0)
        self.spi.write(bytes([0x5C]))
        self.dc(1)
        self.spi.write(self.array)
        self.cs(1)
    
    # 1953 ms
    # Działa na GS4_HMSB ale bardzo wolno
    @micropython.native
    def refresh2(self):
        self.cs(0)
        self.dc(0)
        self.spi.write(bytes([0x5C]))
        self.dc(1)
        
        for i in range(0, 256*128//2, 2):
            buf1 = self.array[i:i+2]
            
            pix0 = (buf1[1] & 0x0F) << 4
            pix1 = (buf1[1] & 0xF0) >> 4
            pix2 = (buf1[0] & 0x0F) << 4
            pix3 = (buf1[0] & 0xF0) >> 4
            
            buf2 = bytearray([pix0 | pix1, pix2 | pix3])
            self.spi.write(buf2)
            
        self.cs(1)
        
    def refresh3(self):
        buf = bytearray(self.width * self.height // 2)
        
        # 256px na linię = 128B na linię
        
        
        x = 0
        p = 0
        for byte in self.array:
            if x%4 == 0:
                if byte & 0b00000001: buf[128*0+1] |= 0x0F
                if byte & 0b00000010: buf[128*1+1] |= 0x0F
                if byte & 0b00000100: buf[128*2+1] |= 0x0F
                if byte & 0b00001000: buf[128*3+1] |= 0x0F
                if byte & 0b00010000: buf[128*4+1] |= 0x0F
                if byte & 0b00100000: buf[128*5+1] |= 0x0F
                if byte & 0b01000000: buf[128*6+1] |= 0x0F
                if byte & 0b10000000: buf[128*7+1] |= 0x0F
            elif x%4 == 1:
                if byte & 0b00000001: buf[128*0+1] |= 0xF0
                if byte & 0b00000010: buf[128*1+1] |= 0xF0
                if byte & 0b00000100: buf[128*2+1] |= 0xF0
                if byte & 0b00001000: buf[128*3+1] |= 0xF0
                if byte & 0b00010000: buf[128*4+1] |= 0xF0
                if byte & 0b00100000: buf[128*5+1] |= 0xF0
                if byte & 0b01000000: buf[128*6+1] |= 0xF0
                if byte & 0b10000000: buf[128*7+1] |= 0xF0
            if x%4 == 2:
                if byte & 0b00000001: buf[128*0] |= 0x0F
                if byte & 0b00000010: buf[128*1] |= 0x0F
                if byte & 0b00000100: buf[128*2] |= 0x0F
                if byte & 0b00001000: buf[128*3] |= 0x0F
                if byte & 0b00010000: buf[128*4] |= 0x0F
                if byte & 0b00100000: buf[128*5] |= 0x0F
                if byte & 0b01000000: buf[128*6] |= 0x0F
                if byte & 0b10000000: buf[128*7] |= 0x0F
            if x%4 == 3:
                if byte & 0b00000001: buf[128*0] |= 0xF0
                if byte & 0b00000010: buf[128*1] |= 0xF0
                if byte & 0b00000100: buf[128*2] |= 0xF0
                if byte & 0b00001000: buf[128*3] |= 0xF0
                if byte & 0b00010000: buf[128*4] |= 0xF0
                if byte & 0b00100000: buf[128*5] |= 0xF0
                if byte & 0b01000000: buf[128*6] |= 0xF0
                if byte & 0b10000000: buf[128*7] |= 0xF0
                
            x += 1
        
    @micropython.native
    def simulate(self):
        pass
#         for y in range(self.height):
#             print(f"{y}\t", end="")
#             for x in range(self.width):
#                 bit  = 1 << (y % 8)
#                 byte = int(self.array[(y // 8) * self.width + x])
#                 pixel = "#" if byte & bit else "."
#                 print(pixel, end="")
#             print("")

if __name__ == "__main__":
    from machine import Pin, I2C
    import mem_used
    import measure_time
#     from image.down_32x32 import *
#     from image.up_32x32 import *
#     from font.extronic16_unicode import *
#     from font.extronic16B_unicode import *

    spi = SPI(1, baudrate=5_000_000, polarity=0, phase=0)
    print(spi)
    
    display = SSD1363_SPI(spi, cs=Pin(9), dc=Pin(10), rotate=0)
    print(display)
    
    print("----")

#     display.fill_rect( 0,   0, 40, 20, display.color(0xFF, 0x00, 0x00))
#     display.fill_rect( 0,  20, 40, 20, display.color(0xFF, 0xFF, 0x00))
#     display.fill_rect( 0,  40, 40, 20, display.color(0x00, 0xFF, 0x00))
#     display.fill_rect( 0,  60, 40, 20, display.color(0x00, 0xFF, 0xFF))
#     display.fill_rect( 0,  80, 40, 20, display.color(0x00, 0x00, 0xFF))
#     display.fill_rect( 0, 100, 40, 20, display.color(0xFF, 0x00, 0xFF))
#     
# 
#     display.refresh()
    
    
#     hal = DisplayHAL(display)
#     print(hal)

#     display.pixel(0, 0, 15)
#     display.pixel(1, 1, 15)
#     display.pixel(2, 2, 15)
#     display.pixel(3, 3, 15)
#     display.pixel(4, 4, 15)
#     display.pixel(5, 5, 15)
#     display.pixel(6, 6, 15)
#     display.pixel(7, 7, 15)
#     display.pixel(255, 0, 15)
    
#     display.fill_rect(0, 0, 7, 7, 15)
    display.rect(0, 0, 256, 128, 15)
#     display.rect(1, 1, 255, 127, 1)
    display.ellipse(128, 64, 64, 64, 15)
    display.ellipse(64, 32, 30, 30, 15)
    display.line(0, 0, 255, 127, 15)
#     display.circle(64, 32, 30, 15)
    display.text('abcdefghijklm',  1,  2, 8)
    display.text('nopqrstuvwxyz',  1, 10, 15)
#     hal.text("abcdefghijkl",  50, 20, 1,  extronic16_unicode, "center")
#     hal.text("abcdefghijkl",  50, 40, 0, extronic16B_unicode, "center")
#     hal.image(up_32x32,       96,  0, 0)
#     hal.image(down_32x32,     96, 32, 0)
   
    
    measure_time.begin()
    display.refresh1()
    measure_time.end("Refresh time:  ")
    
#     hal.simulate()

    mem_used.print_ram_used()