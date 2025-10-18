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
        
    def pixel(self, x, y, c):
        self.display.pixel(x, y, c)
        
    def line(self, x1, y1, x2, y2, c):
        self.display.line(x1, y1, x2, y2, c)
        
    def hline(self, x, y, w, c):
        self.display.hline(x, y, w, c)
        
    def vline(self, x, y, h, c):
        self.display.vline(x, y, h, c)
        
    def rect(self, x, y, w, h, c):
        self.display.rect(x, y, w, h, c)
        
    def fill_rect(self, x, y, w, h, c):
        self.display.fill_rect(x, y, w, h, c)
        
    def fill(self, c):
        self.display.fill(c)
        
    def text(self, text, x, y, c):
        self.display.text(text, x, y, c)
    
    @micropython.native
    def print_char(self, font, char, x, y, color=1):
        pass
#         try:
#             bitmap = font[ord(char)]
#         except:
#             bitmap = font[0]
#             print(f"Char {char} doesn't exist in font")
#         
#         width  = bitmap[0]
#         height = bitmap[1]
#         space  = bitmap[2]
#         
#         if color:
#             buffer = framebuf.FrameBuffer(bitmap[3:], width, height, 0)
#         else:
#             negative_bitmap = bitmap[:]
#             for i in range(3, len(bitmap)):
#                 negative_bitmap[i] = ~negative_bitmap[i]
#             buffer = framebuf.FrameBuffer(negative_bitmap[3:], width, height, 0)
#             self.rect(x-space, y, space, height, 1, True)
#             self.rect(x+width, y, space, height, 1, True)
#         
#         self.blit(buffer, x, y)
#         return width + space     

    @micropython.native
    def print_text(self, font, text, x, y, align="L", color=1):
        width = self.get_text_width(font, text)
        
        if   align == "R":
            x = WIDTH - width
        elif align == "C":
            x = WIDTH//2 - width//2
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

    i2c = I2C(0) # use default pinout and clock frequency
    print(i2c)   # print pinout and clock frequency

#     display = sh1106.SH1106(i2c, address=0x3D, flip_x=True,  flip_y=True, offset_x=2)
    display = ssd1309.SSD1309(i2c, address=0x3C, flip_x=False, flip_y=False)
    print(display)
    
    hal = DisplayHAL(display)
    print(hal)
    
    hal.rect(0, 0, 128, 64, 1)
    hal.line(2, 2, 125, 61, 1)
    hal.text('abcdefghijklm', 1, 2, 1)
    hal.text('nopqrstuvwxyz', 1, 10, 1)
    hal.refresh()
#     hal.simulate()

    mem_used.print_ram_used()