# MicroPython 1.24.1 ESP32-S3 Octal SPIRAM

from machine import Pin, I2C
import framebuf
import mem_used

class DisplayHAL:
    
    @micropython.native
    def __init__(self, display):
        self.display = display
        
    def __str__(self):
        return f"DisplayHAL(display={self.display})"
    
    @micropython.viper
    def enable(self):
        self.display.enable()
        
    @micropython.viper
    def disable(self):
        self.display.disable()
    
    @micropython.viper
    def contrast(self, value):
        self.display.contrast(value)
    
    @micropython.viper
    def refresh(self):
        self.display.refresh()
        
    @micropython.viper
    def simulate(self):
        self.display.simulate()
        
    def pixel(self, x, y, color):
        self.display.pixel(x, y, color)
        
    def line(self, x1, y1, x2, y2, color):
        self.display.line(x1, y1, x2, y2, color)
        
    def hline(self, x, y, width, color):
        self.display.hline(x, y, width, color)
        
    def vline(self, x, y, height, color):
        self.display.vline(x, y, h, color)
        
    def rect(self, x, y, width, height, color):
        self.display.rect(x, y, width, height, color)
        
    def fill_rect(self, x, y, width, height, color):
        self.display.fill_rect(x, y, width, height, color)
        
    def fill(self, color):
        self.display.fill(color)
        
    def text(self, text, x, y, color):
        self.display.text(text, x, y, color)
        
    def image(self, bitmap, x, y, transparent_color=-1):
        self.display.blit(bitmap, x, y, transparent_color)
    
    @micropython.native
    def print_char(self, font, char, x, y, color=1):
        try:
            bitmap = font[ord(char)]
        except:
            bitmap = font[0]
            print(f"Char {char} doesn't exist in font")
        
        width  = bitmap[0]
        height = bitmap[1]
        space  = bitmap[2]
        
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
        return width + space  
    
    @micropython.native
    def print_text(self, font, text, x, y, align="L", color=1):
        width = self.get_text_width(font, text)
        
        if   align == "R":
            x = self.display.width - width
        elif align == "C":
            x = self.display.width//2 - width//2
        elif align == "r":
            x = x - width + 1
        elif align == "c":
            x = x - width//2
        
        for char in text:
            x += self.print_char(font, char, x, y, color)
    
    @micropython.native
    def get_text_width(self, font, text):
        total = 0
        last_char_space = 0
        for char in text:
            bitmap = font.get(ord(char), font[0])
            total += bitmap[0]
            total += bitmap[2]
            last_char_space = bitmap[2]
        
        return total - last_char_space    

if __name__ == "__main__":
    from machine import Pin, I2C
    import sh1106
    import ssd1309
    import mem_used
    from image.down_32x32 import *
    from image.up_32x32 import *
    from font.squared16_unicode import *
    from font.squared16B_unicode import *

    i2c = I2C(0) # use default pinout and clock frequency

#     display = sh1106.SH1106(i2c, address=0x3D, flip_x=True,  flip_y=True, offset_x=2)
    display = ssd1309.SSD1309(i2c, address=0x3C, flip_x=False, flip_y=False)
    
    hal = DisplayHAL(display)
    print(hal)
    
    hal.rect(0, 0, 128, 64, 1)
    hal.line(2, 2, 125, 61, 1)
    hal.text('abcdefghijklm', 1, 2, 1)
    hal.text('nopqrstuvwxyz', 1, 10, 1)
    hal.image(up_32x32,       96,  0, 0)
    hal.image(down_32x32,     96, 32, 0)
    hal.print_text(squared16_unicode,  "abcdefghijkl", 50, 20, "c")
    hal.print_text(squared16B_unicode, "abcdefghijkl", 50, 40, "c", 0)
    
    hal.refresh()
#     hal.simulate()

    mem_used.print_ram_used()