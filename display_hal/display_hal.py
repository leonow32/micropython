# MicroPython 1.24.1 ESP32-S3 Octal SPIRAM
# MicroPython 1.26.1 ESP32-S3 Octal SPIRAM
# MicroPython 1.26.1 ESP32 Pico
# MicroPython 1.27.0 ESP32 Pico
# MicroPython 1.27.0 Raspberry Pico 2

import framebuf

class DisplayHAL:
    
    @micropython.native
    def __init__(self, display):
        self.display  = display
        self.width    = display.width
        self.height   = display.height
        self._transp  = -1
        self._color_f = 1 if display.mono else 0xFFFF
        self._color_b = 0
        self._palette = framebuf.FrameBuffer(bytearray(4), 2, 1, framebuf.MONO_VLSB if display.mono else framebuf.RGB565)
        self._palette.pixel(1, 0, self._color_f)
        self._palette.pixel(0, 0, 0)
    
    def color_set(self, foreground, background=None):
        self._color_f = foreground
        
        if background is not None:
            self._color_b = background
            
        if self._color_f >= 0 and self._color_b >= 0:
            self._transp = -1
            self._palette.pixel(1, 0, self._color_f)
            self._palette.pixel(0, 0, self._color_b)
        elif self._color_f < 0 and self._color_b >= 0:
            self._transp = 0 if self._color_b else 1
            self._palette.pixel(1, 0, self._transp)
            self._palette.pixel(0, 0, self._color_b)
        elif self._color_f >= 0 and self._color_b < 0:
            self._transp = 0 if self._color_f else 1
            self._palette.pixel(1, 0, self._color_f)
            self._palette.pixel(0, 0, self._transp)
        else:
            self._transp = 0
            self._palette.pixel(1, 0, 0)
            self._palette.pixel(0, 0, 0)
    
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
    def pixel(self, x, y):
        self.display.pixel(x, y, self._color_f)
        
    @micropython.viper
    def line(self, x1, y1, x2, y2):
        self.display.line(x1, y1, x2, y2, self._color_f)
        
    @micropython.viper
    def hline(self, x, y, width):
        self.display.hline(x, y, width, self._color_f)
        
    @micropython.viper
    def vline(self, x, y, height):
        self.display.vline(x, y, h, self._color_f)
        
    @micropython.viper
    def rect(self, x, y, width, height):
        self.display.rect(x, y, width, height, self._color_f)
        
    @micropython.viper
    def fill_rect(self, x, y, width, height):
        self.display.fill_rect(x, y, width, height, self._color_f)
        
    @micropython.viper
    def fill(self):
        self.display.fill(self._color_f)
        
    @micropython.native
    def circle(self, x, y, radius, fill=False):
        self.display.ellipse(x, y, radius, radius, self._color_f, fill)
        
    # FONT 1
#     @micropython.native
#     def char(self, font, char, x, y, color=1):
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
#         if self.display.mono:
#             if color:
#                 buffer = framebuf.FrameBuffer(bitmap[3:], width, height, 0)
#             else:
#                 negative_bitmap = bitmap[:]
#                 for i in range(3, len(bitmap)):
#                     negative_bitmap[i] = ~negative_bitmap[i]
#                 buffer = framebuf.FrameBuffer(negative_bitmap[3:], width, height, 0)
#                 self.display.rect(x-space, y, space, height, 1, True)
#                 self.display.rect(x+width, y, space, height, 1, True)
#             self.display.blit(buffer, x, y)
#         else:
#             buffer = framebuf.FrameBuffer(bitmap[3:], width, height, 0)
#             palette_array = bytearray(4)
#             palette_framebuffer = framebuf.FrameBuffer(palette_array, 2, 1, framebuf.RGB565)
#             palette_framebuffer.pixel(0, 0, self.display.color(0x12, 0x34, 0x56)) # background
#             palette_framebuffer.pixel(1, 0, color) # foreground
#             self.display.blit(buffer, x, y, self.display.color(0x12, 0x34, 0x56), palette_framebuffer)
#             
#         return width + space  
#         
#     @micropython.native
#     def text(self, text, x, y, color, font=None, align="left"):
#         if font:
#             if align == "RIGHT":
#                 width = self.text_width(text, font)
#                 x = self.display.width - width
#             elif align == "CENTER":
#                 width = self.text_width(text, font)
#                 x = self.display.width//2 - width//2
#             elif align == "right":
#                 width = self.text_width(text, font)
#                 x = x - width + 1
#             elif align == "center":
#                 width = self.text_width(text, font)
#                 x = x - width//2
#             
#             for char in text:
#                 x += self.char(font, char, x, y, color)
#         else:
#             self.display.text(text, x, y, color)
#     
#     @micropython.native
#     def text_width(self, text, font):
#         total = 0
#         last_char_space = 0
#         for char in text:
#             bitmap = font.get(ord(char), font[0])
#             total += bitmap[0]
#             total += bitmap[2]
#             last_char_space = bitmap[2]
#         
#         return total - last_char_space
    
    # FONT 2
#     @micropython.native
#     def char2(self, font, char, x, y):
#         try:
#             data = font[ord(char)]
#         except:
#             data = font[0]
#             print(f"Char {char} doesn't exist in font")
#         
#         width  = data[0]
#         height = data[1]
#         space  = data[2]
#         bitmap = data[3]
#         
#         self.display.blit(bitmap, x, y, self._transp, self._palette)
#         return width + space  
#         
#     @micropython.native
#     def text2(self, text, x, y, font=None, align="left"):
#         if font:
#             if align == "RIGHT":
#                 width = self.text_width2(text, font)
#                 x = self.display.width - width
#             elif align == "CENTER":
#                 width = self.text_width2(text, font)
#                 x = self.display.width//2 - width//2
#             elif align == "right":
#                 width = self.text_width2(text, font)
#                 x = x - width + 1
#             elif align == "center":
#                 width = self.text_width2(text, font)
#                 x = x - width//2
#             
#             for char in text:
#                 x += self.char2(font, char, x, y)
#         else:
#             self.display.text(text, x, y, self._color_f)
#     
#     @micropython.native
#     def text_width2(self, text, font):
#         total = 0
#         last_char_space = 0
#         for char in text:
#             width, _, space, _= font.get(ord(char), font[0])
#             total += width
#             total += space
#             last_char_space = space
#         
#         return total - last_char_space
    
    # FONT 3
    @micropython.native
    def char3(self, font, char, x, y):
        width, height, space, bitmap = font.get(ord(char), font[0])
        fb = framebuf.FrameBuffer(bitmap, width, height, framebuf.MONO_VLSB)
        self.display.blit(fb, x, y, self._transp, self._palette)
        return width + space  
        
    @micropython.native
    def text3(self, text, x, y, font=None, align="left"):
        if font:
            if align == "RIGHT":
                width = self.text_width3(text, font)
                x = self.display.width - width
            elif align == "CENTER":
                width = self.text_width3(text, font)
                x = self.display.width//2 - width//2
            elif align == "right":
                width = self.text_width3(text, font)
                x = x - width + 1
            elif align == "center":
                width = self.text_width3(text, font)
                x = x - width//2
            
            for char in text:
                x += self.char3(font, char, x, y)
        else:
            self.display.text(text, x, y, self._color_f)
    
    @micropython.native
    def text_width3(self, text, font):
        total = 0
        last_char_space = 0
        for char in text:
            width, _, space, _= font.get(ord(char), font[0])
            total += width
            total += space
            last_char_space = space
        
        return total - last_char_space
            
    @micropython.native
    def image(self, bitmap, x: int, y: int) -> None:
        self.display.blit(bitmap, x, y, self._transp, self._palette)

if __name__ == "__main__":
    import mem_used
    import measure_time
    from machine import Pin, I2C, SPI
    
#     from dem128064e1 import *
    
#     from sh1106 import *
#     from sh1108 import *
    from display_hal.driver.ssd1309 import *
#     from ssd1351 import *
#     from ssd1363_spi import *
#     from ssd1363_spi_bw import *

#     from display_hal.image_mono.down_32x32 import *
#     from display_hal.image_mono.up_32x32 import *
#     from display_hal.image_mono.ball_16x16 import *
#     from display_hal.image_mono.chess_8x8 import *

    i2c = I2C(0) # use default pinout and clock frequency
#     display = SH1106(i2c, address=0x3D, rotate=0, offset_x=2)
    display = SSD1309(i2c, address=0x3C, rotate=0)

#     spi = SPI(1, baudrate=10_000_000, polarity=0, phase=0)
    
#     display = SH1108(spi, cs=Pin(4), dc=Pin(2), rotate=0, offset_x=16)
#     Pin(4, mode=Pin.OUT, value=1)
#     Pin(2, mode=Pin.OUT, value=1)
    
#     display = SSD1351(spi, cs=Pin(27), dc=Pin(15), rotate=0)
#     Pin(27, mode=Pin.OUT, value=1)
#     Pin(15, mode=Pin.OUT, value=1)

#     spi = SPI(1, baudrate=1_000_000, polarity=0, phase=0, sck=Pin(4), mosi=Pin(5), miso=None)
#     display = SSD1363_SPI(spi, cs=Pin(7), dc=Pin(6), rotate=0)
#     display = SSD1363_SPI_BW(spi, cs=Pin(7), dc=Pin(6), rotate=0)
#     display = SSD1363_SPI(spi, cs=Pin(9), dc=Pin(10), rotate=0)

#     spi = SPI(0, baudrate=10_000_000, polarity=0, phase=0, sck=Pin(2), mosi=Pin(3), miso=Pin(4))
#     display = DEM128064E1(spi, cs=Pin(5), dc=Pin(6), rst=Pin(7))
    
#     from display_hal.driver.dem240064b import *
#     spi = SPI(0, baudrate=10_000_000, polarity=0, phase=0, sck=Pin(2), mosi=Pin(3), miso=Pin(4))
#     display = DEM240064B(spi, cs0=Pin(5), cs1=Pin(8), dc=Pin(6), rst=Pin(7))
    
    dihal = DisplayHAL(display)
    print(dihal)
    
#     dihal.contrast_set(0xFF)

    # FONT 1
#     from display_hal.font.console7 import *
#     from display_hal.font.dos8 import *
#     from display_hal.font.galaxy16_digits import *
#     from display_hal.font.mini8 import *
#     from display_hal.font.extronic16_unicode import *
#     from display_hal.font.extronic16B_unicode import *

#     measure_time.begin()
#     dihal.text("-= Font Benchmark =-", 0, 0, 1, console7, "CENTER")
#     dihal.text("abcdefghijklmnopqrstuvwxyz01234", 0, 8, 1, mini8, "CENTER")
#     dihal.text("ąęłćśńóźż", 0, 16, 1, extronic16_unicode, "LEFT")
#     dihal.text("ąęłćśńóźż", 0, 16, 1, extronic16B_unicode, "RIGHT")
#     dihal.text("abcdefghijklmnop", 0, 32, 0, dos8, "CENTER")
#     dihal.text("qrstuvwxyz123345", 0, 40, 0, dos8, "CENTER")
#     dihal.text("0123456789", 0, 49, 1, galaxy16_digits, "CENTER")
#     measure_time.end("Rendering time")

    # FONT 2
#     from display_hal.font2.console7 import *
#     from display_hal.font2.dos8 import *
#     from display_hal.font2.galaxy16_digits import *
#     from display_hal.font2.mini8 import *
#     from display_hal.font2.extronic16_unicode import *
#     from display_hal.font2.extronic16B_unicode import *
#     
#     measure_time.begin()
#     dihal.text2("-= Font Benchmark =-", 0, 0, console7, "CENTER")
#     dihal.text2("abcdefghijklmnopqrstuvwxyz01234", 0, 8, mini8, "CENTER")
#     dihal.text2("ąęłćśńóźż", 0, 16, extronic16_unicode, "LEFT")
#     dihal.text2("ąęłćśńóźż", 0, 16, extronic16B_unicode, "RIGHT")
#     dihal.color_set(0, 1)
#     dihal.text2("abcdefghijklmnop", 0, 32, dos8, "CENTER")
#     dihal.text2("qrstuvwxyz123345", 0, 40, dos8, "CENTER")
#     dihal.color_set(1, 0)
#     dihal.text2("0123456789", 0, 49, galaxy16_digits, "CENTER")
#     measure_time.end("Rendering time")
    
    # FONT 3
    from display_hal.font3.console7 import *
    from display_hal.font3.dos8 import *
    from display_hal.font3.galaxy16_digits import *
    from display_hal.font3.mini8 import *
    from display_hal.font3.extronic16_unicode import *
    from display_hal.font3.extronic16B_unicode import *
    
    measure_time.begin()
    dihal.text3("-= Font Benchmark =-", 0, 0, console7, "CENTER")
    dihal.text3("abcdefghijklmnopqrstuvwxyz01234", 0, 8, mini8, "CENTER")
    dihal.text3("ąęłćśńóźż", 0, 16, extronic16_unicode, "LEFT")
    dihal.text3("ąęłćśńóźż", 0, 16, extronic16B_unicode, "RIGHT")
    dihal.color_set(0, 1)
    dihal.text3("abcdefghijklmnop", 0, 32, dos8, "CENTER")
    dihal.text3("qrstuvwxyz123345", 0, 40, dos8, "CENTER")
    dihal.color_set(1, 0)
    dihal.text3("0123456789", 0, 49, galaxy16_digits, "CENTER")
    measure_time.end("Rendering time")

    # Image demo
#     from display_hal.image_mono.back_32x32 import *
#     from display_hal.image_mono.book_32x32 import *
#     from display_hal.image_mono.cancel_32x32 import *
#     from display_hal.image_mono.clock_32x32 import *
#     from display_hal.image_mono.down_32x32 import *
#     from display_hal.image_mono.hand_32x32 import *
#     from display_hal.image_mono.light_32x32 import *
#     from display_hal.image_mono.ok_32x32 import *
#     from display_hal.image_mono.settings_32x32 import *
#     from display_hal.image_mono.up_32x32 import *
#     
#     measure_time.begin()
#     dihal.image(ok_32x32,        0,  0)
#     dihal.image(back_32x32,      0, 32)
#     dihal.image(clock_32x32,    32,  0)
#     dihal.image(settings_32x32, 32, 32)
#     dihal.image(book_32x32,     64,  0)
#     dihal.image(light_32x32,    64, 32)
#     dihal.image(up_32x32,       96,  0)
#     dihal.image(down_32x32,     96, 32)
#     measure_time.end("Rendering time:")

#     measure_time.begin()
#     dihal.rect(0, 0, display.width, display.height, dihal.color(0xFF, 0xFF, 0xFF))
#     dihal.line(2, 2, display.width-3, display.height-3, dihal.color(0xFF, 0x00, 0x00))
#     dihal.circle(display.width//2, display.height//2, display.width//4-3, dihal.color(0x00, 0xFF, 0x00))
#     dihal.text('abcdefghijklm',  1,  2, dihal.color(0x00, 0xFF, 0xFF))
#     dihal.text('nopqrstuvwxyz',  1, 10, dihal.color(0x00, 0x00, 0xFF))
#     dihal.text("abcdefghijkl",  50, 20, dihal.color(0xFF, 0xFF, 0xFF), extronic16_unicode,  "center")
#     dihal.text("abcdefghijkl",  50, 40, dihal.color(0xFF, 0xFF, 0x00), extronic16B_unicode, "center")
#     dihal.image(up_32x32,       96,  0, dihal.color(0xFF, 0x00, 0x00))
#     dihal.image(down_32x32,     96, 32, dihal.color(0x00, 0xFF, 0x00))
#     measure_time.end("Rendering time:")
    # Refresh
    measure_time.begin()
    dihal.refresh()
    measure_time.end("Refresh time:  ")
    
#     dihal.simulate()

    mem_used.print_ram_used()
