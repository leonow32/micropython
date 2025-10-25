# MicroPython 1.24.1 ESP32 Pico

from machine import Pin, SPI
import framebuf

class SH1108(framebuf.FrameBuffer):
    
    @micropython.native
    def __init__(self, spi, cs, dc, flip_x=False, flip_y=False, offset_x=16):
        self.spi = spi
        self.cs  = cs
        self.dc  = dc
        self.cs.init(mode=Pin.OUT, value=1)
        self.dc.init(mode=Pin.OUT, value=1)
        
        self.flip_x   = flip_x
        self.flip_y   = flip_y
        self.offset_x = offset_x
        self.width    = 128
        self.height   = 160
        self.array    = bytearray(self.width * self.height // 8)
        super().__init__(self.array, self.width, self.height, framebuf.MONO_VLSB)

        config = (
            0xAE,       # Display OFF
            
            0x20,       # Set Memory addressing mode = page addressing mode
#             0x21,       # Set Memory addressing mode = page addressing mode
            
            0x81, 0x0F, # Set contrast control
            
#             0xA0,       # Segment remap = down
            0xA1,       # Segment remap = up
            
            0xA6,       # Positive display (not inverted)
            0xA9, 0x02, # Set Display Resolution
            0xAD, 0x80, # Set DC-DC setting = disabled
            
#             0xC0,       # Set Common scan direction (no mirror)
            0xC8,       # Set Common scan direction (mirror)
            
            0xD5, 0xF1, # Divide Ratio/Oscillator Frequency Mode Set
            0xD9, 0x1F, # Set Dis-charge/Pre-charge Period
            0xDB, 0x2B, # Set Vcomh voltage
            0xDC, 0x35, # Set VSEGM Deselect Level
            0x30,       # Set Discharge VSL Level
            0xAF,       # Display ON
        )

        for cmd in config:
            self.cmd_write(cmd)
    
    @micropython.viper
    def __str__(self):
        return f"SH1108(spi={self.spi}, cs={self.cs}, dc={self.dc}, flip_x={self.flip_x}, flip_y={self.flip_y}, offset_x={self.offset_x})"

    def data_write(self, data):
        self.dc(1)
        self.cs(0)
        self.spi.write(bytes([data]))
        self.cs(1)
        
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
    def refresh(self):
        self.cs(0)

        for page in range(20):
            header = bytes([
                0xB0, page,                    # Set page number
                0x00 | (self.offset_x & 0x0F), # Set x cursor, low nibble
                0x10 | (self.offset_x >> 4),   # Set x cursor, high nibble
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
        
    @micropython.native
    def color(self, r: int, g: int, b: int) -> int:
        return 1 if (r | g | b) else 0

if __name__ == "__main__":
    from machine import Pin, SPI
    import mem_used
    import measure_time
#     from image.down_32x32 import *
#     from image.up_32x32 import *
#     from font.extronic16_unicode import *
#     from font.extronic16B_unicode import *

    spi = SPI(1, baudrate=10_000_000, polarity=0, phase=0) # use default pinout
    print(spi)
    
    cs = Pin(4)
    dc = Pin(2)
    
    measure_time.begin()
    display = SH1108(spi, cs, dc, flip_x=True, flip_y=True, offset_x=16)
    measure_time.end("Init")
    
    print("----")

    display.fill_rect(40,  2, 10, 20, display.color(0, 0, 0))
    display.text("Linia tekstu 1",   0,   0, 1)
    display.text("Linia tekstu 2",   0,   8, 1)
    display.text("Linia tekstu 3",   0,  16, 1)
    display.text("Bottom",           0, 160-8, 1)
    display.ellipse(64, 80, 60, 60, 1, 0)
    display.rect(0, 0, 128, 160, 1)
    
#     display.pixel(0, 127, 1)
#     display.fill_rect( 0,  40, 40, 20, display.color(0x00, 0xFF, 0x00))
#     display.fill_rect( 0,  60, 40, 20, display.color(0x00, 0xFF, 0xFF))
#     display.fill_rect( 0,  80, 40, 20, display.color(0x00, 0x00, 0xFF))
#     display.fill_rect( 0, 100, 40, 20, display.color(0xFF, 0x00, 0xFF))
#     
# 
    display.refresh()
    
    
#     hal = DisplayHAL(display)
#     print(hal)
    
#     hal.rect(0, 0, 128, 64, 1)
#     hal.line(2, 2, 125, 61, 1)
#     hal.circle(64, 32, 30, 1)
#     hal.text('abcdefghijklm',  1,  2, 1)
#     hal.text('nopqrstuvwxyz',  1, 10, 1)
#     hal.text("abcdefghijkl",  50, 20, 1,  extronic16_unicode, "center")
#     hal.text("abcdefghijkl",  50, 40, 0, extronic16B_unicode, "center")
#     hal.image(up_32x32,       96,  0, 0)
#     hal.image(down_32x32,     96, 32, 0)
   
    
#     hal.refresh()
#     hal.simulate()

    mem_used.print_ram_used()
