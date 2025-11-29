# MicroPython 1.24.1 ESP32-S3 Octal SPIRAM
# MicroPython 1.26.1 ESP32-S3 Octal SPIRAM
# MicroPython 1.26.1 ESP32 Pico

from machine import Pin, I2C
import framebuf
import mem_used

class DisplayHAL:
    
    @micropython.native
    def __init__(self, display):
        self.display = display
        
    @micropython.viper
    def __str__(self):
        return f"DisplayHAL(display={self.display})"
    
    @micropython.viper
    def enable(self):
        self.display.enable()
        
    @micropython.viper
    def disable(self):
        self.display.disable()
    
    @micropython.viper
    def contrast_set(self, value):
        self.display.contrast_set(value)
        
    @micropython.viper
    def color(self, r, g, b):
        return self.display.color(r, g, b)
    
    @micropython.viper
    def refresh(self):
        self.display.refresh()
        
    @micropython.viper
    def simulate(self):
        self.display.simulate()
        
    @micropython.viper
    def pixel(self, x, y, color):
        self.display.pixel(x, y, color)
        
    @micropython.viper
    def line(self, x1, y1, x2, y2, color):
        self.display.line(x1, y1, x2, y2, color)
        
    @micropython.viper
    def hline(self, x, y, width, color):
        self.display.hline(x, y, width, color)
        
    @micropython.viper
    def vline(self, x, y, height, color):
        self.display.vline(x, y, h, color)
        
    @micropython.viper
    def rect(self, x, y, width, height, color):
        self.display.rect(x, y, width, height, color)
        
    @micropython.viper
    def fill_rect(self, x, y, width, height, color):
        self.display.fill_rect(x, y, width, height, color)
        
    @micropython.viper
    def fill(self, color):
        self.display.fill(color)
        
    @micropython.native
    def circle(self, x, y, radius, color, fill=False):
        self.display.ellipse(x, y, radius, radius, color, fill)
        
    @micropython.native
    def char(self, font, char, x, y, color=1):
        try:
            bitmap = font[ord(char)]
        except:
            bitmap = font[0]
            print(f"Char {char} doesn't exist in font")
        
        width  = bitmap[0]
        height = bitmap[1]
        space  = bitmap[2]
        
        if self.display.mono:
            if color:
                buffer = framebuf.FrameBuffer(bitmap[3:], width, height, 0)
            else:
                negative_bitmap = bitmap[:]
                for i in range(3, len(bitmap)):
                    negative_bitmap[i] = ~negative_bitmap[i]
                buffer = framebuf.FrameBuffer(negative_bitmap[3:], width, height, 0)
                self.display.rect(x-space, y, space, height, 1, True)
                self.display.rect(x+width, y, space, height, 1, True)
            self.display.blit(buffer, x, y)
        else:
            buffer = framebuf.FrameBuffer(bitmap[3:], width, height, 0)
            palette_array = bytearray(4)
            palette_framebuffer = framebuf.FrameBuffer(palette_array, 2, 1, framebuf.RGB565)
            palette_framebuffer.pixel(0, 0, self.display.color(0x12, 0x34, 0x56)) # background
            palette_framebuffer.pixel(1, 0, color) # foreground
            self.display.blit(buffer, x, y, self.display.color(0x12, 0x34, 0x56), palette_framebuffer)
            
        return width + space  
        
    @micropython.native
    def text(self, text, x, y, color, font=None, align="left"):
        if font:
            if align == "RIGHT":
                width = self.text_width(text, font)
                x = self.display.width - width
            elif align == "CENTER":
                width = self.text_width(text, font)
                x = self.display.width//2 - width//2
            elif align == "right":
                width = self.text_width(text, font)
                x = x - width + 1
            elif align == "center":
                width = self.text_width(text, font)
                x = x - width//2
            
            for char in text:
                x += self.char(font, char, x, y, color)
        else:
            self.display.text(text, x, y, color)
    
    @micropython.native
    def text_width(self, text, font):
        total = 0
        last_char_space = 0
        for char in text:
            bitmap = font.get(ord(char), font[0])
            total += bitmap[0]
            total += bitmap[2]
            last_char_space = bitmap[2]
        
        return total - last_char_space
    
    @micropython.native
    def image(self, bitmap, x, y, color=-1):
        if self.display.mono:
            self.display.blit(bitmap, x, y, 0)
        else:
            palette_array = bytearray(4)
            palette_framebuffer = framebuf.FrameBuffer(palette_array, 2, 1, framebuf.RGB565)
            palette_framebuffer.pixel(0, 0, self.display.color(0x12, 0x34, 0x56)) # background
            palette_framebuffer.pixel(1, 0, color) # foreground
            self.display.blit(bitmap, x, y, self.display.color(0x12, 0x34, 0x56), palette_framebuffer)

if __name__ == "__main__":
    from machine import Pin, I2C
    from sh1106 import *
    from sh1108 import *
    from ssd1309 import *
    from ssd1351 import *
    from ssd1363_spi import *
    from ssd1363_bw_spi import *
    import mem_used
    import measure_time
    from image.down_32x32 import *
    from image.up_32x32 import *
    from font.extronic16_unicode import *
    from font.extronic16B_unicode import *

#     i2c = I2C(0) # use default pinout and clock frequency
#     display = SH1106(i2c, address=0x3D, rotate=0, offset_x=2)
#     display = SSD1309(i2c, address=0x3C, rotate=0)

#     spi = SPI(1, baudrate=10_000_000, polarity=0, phase=0)
#     display = SH1108(spi, cs=Pin(4), dc=Pin(2), rotate=0, offset_x=16)
#     display = SSD1351(spi, cs=Pin(27), dc=Pin(15), rotate=0)

    spi = SPI(1, baudrate=1_000_000, polarity=0, phase=0, sck=Pin(4), mosi=Pin(5), miso=None)
    display = SSD1363_BW_SPI(spi, cs=Pin(7), dc=Pin(6), rotate=0)
    
    hal = DisplayHAL(display)
    print(hal)
    
    hal.contrast_set(0xFF)
    
    measure_time.begin()
    hal.rect(0, 0, display.width, display.height, hal.color(0xFF, 0xFF, 0xFF))
    hal.line(2, 2, display.width-3, display.height-3, hal.color(0xFF, 0x00, 0x00))
    hal.circle(display.width//2, display.height//2, display.width//4-3, hal.color(0x00, 0xFF, 0x00))
    hal.text('abcdefghijklm',  1,  2, hal.color(0x00, 0xFF, 0xFF))
    hal.text('nopqrstuvwxyz',  1, 10, hal.color(0x00, 0x00, 0xFF))
    hal.text("abcdefghijkl",  50, 20, hal.color(0xFF, 0xFF, 0xFF), extronic16_unicode,  "center")
    hal.text("abcdefghijkl",  50, 40, hal.color(0xFF, 0xFF, 0x00), extronic16B_unicode, "center")
    hal.image(up_32x32,       96,  0, hal.color(0xFF, 0x00, 0x00))
    hal.image(down_32x32,     96, 32, hal.color(0x00, 0xFF, 0x00))
    
    measure_time.end("Rendering time:")
    
    measure_time.begin()
    hal.refresh()
    measure_time.end("Refresh time:  ")
    
#     hal.simulate()

    mem_used.print_ram_used()